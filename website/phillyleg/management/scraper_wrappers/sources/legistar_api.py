#import datetime
#import os
#import urllib2


class LegistarApiWrapper (object):
    """
    A wrapper around the Legistar API. This is the best source for up-to-date,
    real-time legislative data. It is responsible for fetching and reading the
    SOAP service that provides this data.
    """

    wsdl_file_name = 'swdata.sqlite3'
    """The local file name of the datastore."""

    wsdl_url = 'http://betasdk.legistar.com/main.asmx?WSDL'
    """The URL of the original WSDL file"""

    def urlopen(self, *args, **kwargs):
        """A facade over urlopen; mainly used for stubbing in tests"""
        return urllib2.urlopen(*args, **kwargs)

    def scrape_legis_file(self, key, cursor):
        """Extract a record from the given document (soup). The key is for the
           sake of record-keeping.  It is the key passed to the site URL."""

        cursor.execute('''select
            id,type,url,status,title,controlling_body,intro_date,final_date,
            version,contact,sponsors from swdata where key=?''', (key,))

        row = cursor.fetchone()
        print row
        lid, ltype, lurl, lstatus, ltitle, lbody, lintro, lfinal, \
        lversion, lcontact, lsponsors = row

        record = {
            'key': key,
            'id': lid,
            'url': lurl,
            'type': ltype,
            'status': lstatus,
            'title': ltitle,
            'controlling_body': lbody,
            'intro_date': self.make_datetime(lintro),
            'final_date': self.make_datetime(lfinal),
            'version': lversion,
            'contact': lcontact,
            'sponsors': lsponsors
        }

        attachments = self.scrape_legis_attachments(key, cursor)
        actions = self.scrape_legis_actions(key, cursor)
        minutes = self.collect_minutes(actions, cursor)

        print record, attachments, actions, minutes
        return record, attachments, actions, minutes

    def collect_minutes(self, actions, cursor):

        action_keys = tuple([action['key'] for action in actions])
        placeholders = ['?'] * len(action_keys)

        cursor.execute('''
          select minutes.url,
                 minutes.fulltext,
                 minutes.date_taken
            from minutes inner join actions
           where minutes.url = actions.minutes_url
             and actions.key in (%s)''' % ','.join(placeholders), action_keys)

        minuteses = []

        for row in cursor:
            minutes = {
                'url': row[0],
                'fulltext': row[1],
                'date_taken': self.make_datetime(row[2][:10]).date(),
            }
            minuteses.append(minutes)

        return minuteses

    def make_datetime(self, dt_str):
        if '-' in dt_str:
            try:
                return datetime.datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                return datetime.datetime.strptime(dt_str, '%Y-%m-%d')
        elif '/' in dt_str:
            return datetime.datetime.strptime(dt_str, '%m/%d/%Y')

    def scrape_legis_attachments(self, key, cursor):

        cursor.execute('''select description,url
            from attachments where key=?''', (key,))

        attachments = []

        for row in cursor:
            attachment = {
                'key': key,
                'description': row[0],
                'url': row[1],
            }
            attachments.append(attachment)

        return attachments

    def scrape_legis_actions(self, key, cursor):

        cursor.execute('''select
            date_taken,acting_body,description,motion,minutes_url,notes
            from actions where key=?''', (key,))

        actions = []

        for action_row in cursor:
            action = {
                'key': key,
                'date_taken': self.make_datetime(action_row[0]),
                'acting_body': action_row[1],
                'description': action_row[2],
                'motion': action_row[3],
                'minutes_url': action_row[4],
                'notes': action_row[5],
            }
            actions.append(action)

        return actions

    def __download_db(self):
        print "Loading the WSDL (this may take a while)..."
        wsdl_file = self.urlopen(self.wsdl_url)
        wsdl = wsdl_file.read()
        outfile = open(self.wsdl_file_name, 'w')
        outfile.write(wsdl)
        outfile.close()

    def __check_db_exists(self):
        if os.path.exists(self.db_file_name):
            print "Local copy of database already exists."
            return True
        else:
            print "No local copy of database exists."
            return False

    def __connect_to_db(self):
        conn = sqlite3.connect(self.db_file_name)
        self.__cursor = conn.cursor()

    def check_for_new_content(self, last_key, force_download=False):
        """Look through the next 10 keys to see if there are any more files.
           10 is arbitrary, but I feel like it's large enough to be safe."""

        if not self.__cursor:
            if force_download or not self.__check_db_exists():
                self.__download_db()
            self.__connect_to_db()

        cursor = self.__cursor

        cursor.execute('''select key
            from swdata
            where key > ?
            order by key''', (last_key,))

        row = cursor.fetchone()
        if row:
            return int(row[0]), cursor

        return last_key, None
