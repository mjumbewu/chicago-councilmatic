###############################################################################
# This will collect the latest legislative filings released in the city of
# Philadelphia.
###############################################################################

#will send out daily email for users - first will read all keywords
#create text files, then email text files to all each user subscribed.

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
import django
import logging
import optparse
import sys

from phillyleg.management.scraper_wrappers import CouncilmaticDataStoreWrapper
from phillyleg.management.scraper_wrappers import PhillyLegistarSiteWrapper
from utils import TooManyGeocodeRequests

def import_leg_files(start_key, source, ds, save_key=False):
    """
    Imports the legislative filings starting at the given key, and going either
    until there it reaches the end of the available records, or the script times
    out.
    """
    curr_key = start_key
    while True:
        curr_key, source_obj = source.check_for_new_content(curr_key)

        if source_obj is None:
            break

        record, attachments, actions, minutes = \
            source.scrape_legis_file(curr_key, source_obj)
        ds.save_legis_file(record, attachments, actions, minutes)
        if save_key:
            ds.save_continuation_key(curr_key)


def load_scraper():
    scraper_name = settings.LEGISLATION['SCRAPER']
    module, attr = scraper_name.rsplit('.', 1)

    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured('Error importing legislation scraper %s: "%s"' % (scraper_name, e))

    try:
        ScraperWrapper = getattr(mod, attr)
    except AttributeError as e:
        raise ImproperlyConfigured('Error importing legislation scraper %s: "%s"' % (scraper_name, e))

    options = settings.LEGISLATION['SCRAPER_OPTIONS']
    return ScraperWrapper(**options)


class Command(BaseCommand):
    help = "Load new legislative file data from the Legistar city council site."
    option_list = BaseCommand.option_list + (
            optparse.make_option('--update',
                action='store_true',
                dest='update_files',
                default=False,
                help='Update existing files as well'),
            )


    def handle(self, *args, **options):
        log = logging.getLogger()
        log.setLevel(logging.INFO)

        # Create a datastore wrapper object
        ds = self.ds = CouncilmaticDataStoreWrapper()
        source = self.source = load_scraper()

        # Seed the PDF cache with already-downloaded content.
        #
        # Downloading and parsing PDF content really slows down the scraping
        # process.  If we had to redownload all of them every time we scraped,
        # it would take a really long time to refresh all of the old stuff.  So
        # that PDFs that have already been downloaded won't be again, seed the
        # source cache with that data.
        #
        # Hopefully this won't be too much of a burden on memory :).
        source.init_pdf_cache(ds.pdf_mapping)

        update_files = options['update_files']

        try:
            self._get_new_files()
            if update_files:
                self._get_updated_files()
        except TooManyGeocodeRequests:
            sys.exit(0)

    def _get_updated_files(self):
        ds = self.ds
        source = self.source

        # Continue updating the entire datastore
        cont_key = ds.get_continuation_key()
        import_leg_files(cont_key, source, ds, save_key=True)

        # If we've made it here, then we have all the latest filings, and we have gone
        # through and updated the entire datastore.  Now, reset the continuation key to
        # get ready for the next go-around.
#        ds.save_continuation_key(72)
        cont_key = ds.get_continuation_key()
        ds.save_continuation_key(cont_key - 1000) # This should be a configurable value

    def _get_new_files(self):
        ds = self.ds
        source = self.source

        # Get the latest filings
        curr_key = ds.get_latest_key()
        import_leg_files(curr_key, source, ds)
