###############################################################################
# This will collect the latest legislative filings released in the city of
# Philadelphia.
###############################################################################

#will send out daily email for users - first will read all keywords
#create text files, then email text files to all each user subscribed.

from django.core.management.base import BaseCommand, CommandError
import django
import optparse
import sys

from phillyleg.management.scraper_wrappers import CouncilmaticDataStoreWrapper
from phillyleg.management.scraper_wrappers import ScraperWikiSourceWrapper
from utils import TooManyGeocodeRequests

class Command(BaseCommand):
    help = "Load new legislative file data from the Legistar city council site."
    option_list = BaseCommand.option_list + (
            optparse.make_option('--forcedownload',
                action='store_true',
                dest='force_download',
                default=False,
                help='Force downloading of data from ScraperWiki even if data is available locally'),
            )

    def handle(self, *args, **options):
        force_download = options['force_download']

        try:
            self._get_updated_files()
            self._get_new_files(force_download)
        except TooManyGeocodeRequests:
            sys.exit(0)

    def _get_updated_files(self):
        pass

    def _get_new_files(self, force_download):
        # Create a datastore wrapper object
        ds = CouncilmaticDataStoreWrapper()
        source = ScraperWikiSourceWrapper()

        # Get the latest filings
        curr_key = ds.get_latest_key()

        while True:
            curr_key, source_obj = source.check_for_new_content(curr_key, force_download)

            if source_obj is None:
                break

            record, attachments, actions, minutes = \
                source.scrape_legis_file(curr_key, source_obj)
            ds.save_legis_file(record, attachments, actions, minutes)
