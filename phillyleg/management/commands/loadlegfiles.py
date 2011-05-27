###############################################################################
# This will collect the latest legislative filings released in the city of
# Philadelphia.
###############################################################################

#will send out daily email for users - first will read all keywords
#create text files, then email text files to all each user subscribed.

from django.core.management.base import BaseCommand, CommandError
import django

from phillyleg.management.scraper_wrappers import CouncilmaticDataStoreWrapper
from phillyleg.management.scraper_wrappers import ScraperWikiSourceWrapper

class Command(BaseCommand):
    help = "Load new legislative file data from the Legistar city council site."
    
    def handle(self, *args, **options):
        self._get_updated_files()
        self._get_new_files()
    
    def _get_updated_files(self):
        pass
    
    def _get_new_files(self):
        # Create a datastore wrapper object
        ds = CouncilmaticDataStoreWrapper()
        source = ScraperWikiSourceWrapper()

        # Get the latest filings
        curr_key = ds.get_latest_key()

        while True:
            curr_key, source_obj = source.check_for_new_content(curr_key)
            
            if source_obj is None:
                break
            
            record, attachments, actions, minutes = \
                source.scrape_legis_file(curr_key, source_obj)
            ds.save_legis_file(record, attachments, actions, minutes)
            

