import datetime
import httplib
import logging
import re
import urllib2
import utils
from collections import defaultdict
import pdb

from legistar.scraper import LegistarScraper
from legistar.config import Config, DEFAULT_CONFIG

log = logging.getLogger(__name__)


class HostedLegistarSiteWrapper (object):
    """
    A facade over the Philadelphia city council legistar site data.  It is
    responsible for scraping data out of the site.  The main external point
    of interaction is scrape_legis_file.

    requires: BeautifulSoup, mechanize
    """

    def __init__(self, **options):
        self.scraper = LegistarScraper(options)

    def scrape_legis_file(self, key, summary):
        '''Extract a record from the given document (soup). The key is for the
           sake of record-keeping.  It is the key passed to the site URL.'''

        legislation_attrs, legislation_history = self.scraper.expandLegislationSummary(summary)

        record = {
            'key' : key,
            'id' : summary['Record #'],
            'url' : summary['URL'],
            'type' : summary['Type'],
            'status' : summary['Status'],
            'title' : summary['Title'],
            'controlling_body' : legislation_attrs['Current Controlling Legislative Body'],
            'intro_date' : self.convert_date(summary['Intro Date']),
            'final_date' : self.convert_date(summary['Final Date']),
            'version' : summary['Version'],
            'contact' : None,
            'sponsors' : legislation_attrs['Sponsors']
        }

        try:
            attachments = legislation_attrs['Attachments']
        except KeyEror:
            attachments = None

        actions = []
        for act in legislation_history :
            act_details, act_votes = self.scraper.expandHistorySummary(act)
            action = {
                'key' : key,
                'date_taken' : act['Date'],
                'acting_body' : act['Action By']['label'],
                'motion' : act['Result'],
                'status' : act['Status']
            }
            actions.append(action)


        minutes = None

        log.info('Scraped legfile with key %r' % (key,))
        log.debug("%r %r %r %r" % (record, attachments, actions, minutes))
        return record, attachments, actions, minutes

    def convert_date(self, orig_date):
        if orig_date:
            return datetime.datetime.strptime(orig_date, '%m/%d/%Y').date()
        else:
            return ''


    def check_for_new_content(self, last_key):
        '''Grab the next legislation summary row. Doesn't use the last_key
           parameter; just starts at the beginning for each instance of the
           scraper.
        '''
        next_summary = defaultdict(str)

        self.legislation_summaries =  self.scraper.searchLegislation('')

        try:
            next_summary.update(self.legislation_summaries.next())
            return 0, next_summary
        except StopIteration:
            return None, None

    def init_pdf_cache(self, pdf_mapping) :
        pass
        
    
