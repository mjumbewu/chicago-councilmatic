import datetime
import httplib
import re
import urllib2
import utils
from BeautifulSoup import BeautifulSoup

STARTING_KEY = 72 # The highest key was 11001 as of 5 Apr 2011

class PhillyLegistarSiteWrapper (object):
    """
    A facade over the Philadelphia city council legistar site data.  It is
    responsible for scraping data out of the site.  The main external point
    of interaction is scrape_legis_file.
    """

    STARTING_URL = 'http://legislation.phila.gov/detailreport/?key='

    def urlopen(self, *args, **kwargs):
        return urllib2.urlopen(*args, **kwargs)

    def scrape_legis_file(self, key, soup):
        '''Extract a record from the given document (soup). The key is for the
           sake of record-keeping.  It is the key passed to the site URL.'''

        span = soup.find('span', {'id':'lblFileNumberValue'})
        lid = span.text

        span = soup.find('span', {'id':'lblFileTypeValue'})
        ltype = span.text

        span = soup.find('span', {'id':'lblFileStatusValue'})
        lstatus = span.text

        span = soup.find('span', {'id':'lblTitleValue'})
        ltitle = span.text

        span = soup.find('span', {'id':'lblControllingBodyValue'})
        lbody = span.text

        span = soup.find('span', {'id':'lblIntroDateValue'})
        lintro = span.text

        span = soup.find('span', {'id':'lblFinalActionValue'})
        lfinal = span.text

        span = soup.find('span', {'id':'lblVersionValue'})
        lversion = span.text

        span = soup.find('span', {'id':'lblContactValue'})
        lcontact = span.text

        span = soup.find('span', {'id':'lblSponsorsValue'})
        lsponsors = span.text

        record = {
            'key' : key,
            'id' : lid,
            'url' : self.STARTING_URL + str(key),
            'type' : ltype,
            'status' : lstatus,
            'title' : ltitle,
            'controlling_body' : lbody,
            'intro_date' : self.convert_date(lintro),
            'final_date' : self.convert_date(lfinal),
            'version' : lversion,
            'contact' : lcontact,
            'sponsors' : lsponsors
        }

        attachments = self.scrape_legis_attachments(key, soup)
        actions = self.scrape_legis_actions(key, soup)
        minutes = self.collect_minutes(actions)

        print record, attachments, actions, minutes
        return record, attachments, actions, minutes

    def get_minutes_date(self, minutes_url):
        date_match = re.search('_(\d{2})-(\d{2})-(\d{2})_', minutes_url)
        if date_match:
            date_taken = datetime.date(
                year=int('20' + date_match.group(1)),
                month=int(date_match.group(2)),
                day=int(date_match.group(3)),
            )
        else:
            date_taken = ''

        return date_taken

    def get_minutes_doc(self, minutes_url):
        fulltext = self.extract_pdf_text(minutes_url)
        date_taken = self.get_minutes_date(minutes_url)

        minutes_doc = {
            'url' : minutes_url,
            'fulltext' : fulltext,
            'date_taken' : date_taken,
        }

        return minutes_doc

    def collect_minutes(self, actions):
        """
        Given a list of legislative actions, collect the minutes data attached
        to those actions.
        """

        minutes = {}
        for action in actions:
            minutes_url = action['minutes_url']
            if minutes_url.endswith('.pdf'):
                minutes_doc = self.get_minutes_doc(minutes_url)
                minutes[minutes_url] = minutes_doc

        return minutes.values()

    def scrape_legis_attachments(self, key, soup):
        """
        Given a beautiful soup representation of legislative file, return the
        list of attachments.
        """

        attachments = []

        attach_div = soup.find('div', {'id' : 'divAttachmentsValue'})
        for cell in attach_div.findAll('a'):
            url = cell['href']

            if url.endswith('.pdf'):
                fulltext = self.extract_pdf_text(url)
            else:
                fulltext = ''

            attachment = {
                'key' : key,
                'description' : cell.text,
                'url' : url,
                'fulltext' : fulltext,
            }
            attachments.append(attachment)

        return attachments

    def scrape_legis_actions(self, key, soup):
        """
        Given a beautiful soup representation of a legislative file,
        return the actions taken on the file.
        """

        def get_action_cell_text(cell):
            cell_a = cell.find('a')
            if cell_a:
                return cell_a.text
            else:
                return cell.text

        def get_action_cell_resource(cell):
            cell_a = cell.find('a')
            if cell_a:
                return cell_a['href']
            else:
                return ''

        notes = []
        actions = []

        action_div = soup.find('div', {'id': 'divScroll'})
        action_rows = action_div.findAll('tr')

        for action_row in action_rows:
            cells = action_row.findAll('td')

            if len(cells) == 2:
                # Sometimes, there are notes interspersed in the history table.
                # Luckily (?) their rows have only two cells instead of four, so
                # we can easily tell that they're there.
                action = actions[-1]
                action['notes'] = cells[1].text
                continue

            action = {
                'key' : key,
                'date_taken' : self.convert_date(get_action_cell_text(cells[0])),
                'acting_body' : get_action_cell_text(cells[1]),
                'description' : get_action_cell_text(cells[2]),
                'motion' : get_action_cell_text(cells[3]),
                'minutes_url' : get_action_cell_resource(cells[0]),
                'notes' : '',
            }
            actions.append(action)

        return actions

    __pdf_cache = None
    def init_pdf_cache(self):
        self.__pdf_cache = self.__pdf_cache or {}

    def extract_pdf_text(self, pdf_data, tries_left=5):
        """
        Given an http[s] URL, a file URL, or a file-like object containing
        PDF data, return the text from the PDF.  Cache URLs or data that have
        already been seen.
        """

        self.init_pdf_cache()

        pdf_key = pdf_data
        if pdf_key in self.__pdf_cache:
            return self.__pdf_cache[pdf_key]

        if pdf_key.startswith('file://'):
            path = pdf_key[7:]
            pdf_data = open(path).read()
        elif pdf_key.startswith('http://') or pdf_key.startswith('https://'):
            url = pdf_key
            try:
                pdf_data = self.urlopen(url).read()

            # Protect against removed PDFs (ones that result in 404 HTTP
            # response code).  I don't know why they've removed some PDFs
            # but they have.
            except urllib2.HTTPError, err:
                if err.code == 404:
                    self.__pdf_cache[pdf_key] = ''
                    return ''
                else:
                    raise

            # Been getting timeout exceptions every so often, so try again
            # if timed out.
            except urllib2.URLError, err:
                if tries_left:
                    return self.extract_pdf_text(pdf_key, tries_left-1)

        xml_data = utils.pdftoxml(pdf_data)

        self.__pdf_cache[pdf_key] = self.extract_xml_text(xml_data, 'pdf2xml')
        return self.__pdf_cache[pdf_key]

    def extract_xml_text(self, xml_data, root_node_name):
        soup = BeautifulSoup(xml_data)
        xml_text = soup.find(root_node_name).text
        return xml_text

    def convert_date(self, orig_date):
        if orig_date:
            return datetime.datetime.strptime(orig_date, '%m/%d/%Y').date()
        else:
            return ''


    def is_error_page(self, soup):
        '''Check the given soup to see if it represents an error page.'''
        error_p = soup.find('p', 'errorText')

        if error_p is None: return False
        else: return True

    def check_for_new_content(self, last_key):
        '''Look through the next 10 keys to see if there are any more files.
           10 is arbitrary, but I feel like it's large enough to be safe.'''

        curr_key = last_key
        for _ in xrange(10):
            curr_key = curr_key + 1

            url = self.STARTING_URL + str(curr_key)
            more_tries = 10
            while True:
                try:
                    html = self.urlopen(url)
                    break

                # Sometimes the server will respond with a status line that httplib
                # does not understand (an empty status line, in particular).  When
                # this happens, keep trying to access the page.  Give up after 10
                # tries.
                except httplib.BadStatusLine, ex:
                    more_tries -= 1;
                    print 'Received BadStatusLine exception %r for url %r' % (ex, url)
                    if not more_tries:
                        raise

                # Sometimes the server will do things like just take too long to
                # respond.  When it does, try again 10 times.
                except urllib2.URLError, ex:
                    more_tries -= 1;
                    print 'Received URLError exception %r for url %r' % (ex, url)
                    if not more_tries:
                        raise
            soup = BeautifulSoup(html)

            if not self.is_error_page(soup):
                return curr_key, soup

        return curr_key, None
