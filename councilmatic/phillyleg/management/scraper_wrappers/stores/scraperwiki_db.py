#import scraperwiki

class ScraperWikiDataStoreWrapper (object):
    """
    This is the interface over an arbitrary database where the information is
    being stored.  I'm using it primarily because I want the scraper code to be
    used on both ScraperWiki and in my Django app on my Django models.  For my
    app, I want local access to the data.  But I love ScraperWiki as a central
    place where you can find data about anything you want, so it's important to
    have the data available here as well.
    """
    def get_latest_key(self):
        '''Check the datastore for the key of the most recent filing.'''

        max_key = STARTING_KEY

        try:
            records = scraperwiki.sqlite.select('* from swdata order by key desc limit 1')
            if records:
                record = records[0]
                max_key = record['key']
        except scraperwiki.sqlite.NoSuchTableSqliteError:
            pass

        return int(max_key)

    def get_continuation_key(self):
        scraperwiki.sqlite.get_var('continuation_key', 72)

    def save_continuation_key(self, key):
        scraperwiki.sqlite.save_var('continuation_key', key)

    def save_legis_file(self, record, attachments, actions, minuteses):
        """
        Take a legislative file record and do whatever needs to be
        done to get it into the database.
        """
        # Convert m/d/y dates into date objects.
        scraperwiki.sqlite.save(['key'], record)
        for attachment in attachments:
            scraperwiki.sqlite.save(['key','url'], attachment, table_name='attachments')
        for minutes in minuteses:
            scraperwiki.sqlite.save(['url'], minutes, table_name='minutes')
        for action in actions:
            scraperwiki.sqlite.save(['key','date_taken','description','notes'], action, table_name='actions')

    @property
    def pdf_mapping(self):
        """
        Build a mapping of the URLs and PDF test that already exist in the
        database.
        """
        mapping = {}

        attachments = scraperwiki.sqlite.select('* from attachments')
        for attachment in attachments:
            mapping[attachment['url']] = attachment['fulltext']

        minuteses = scraperwiki.sqlite.select('* from minuteses')
        for minutes in minuteses:
            mapping[minutes['url']] = minutes['fulltext']

        return mapping
