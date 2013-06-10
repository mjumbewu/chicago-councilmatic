from unittest import TestCase
import os
import bs4 as bs
import datetime as dt
import mock
from StringIO import StringIO

from phillyleg.management.scraper_wrappers import PhillyLegistarSiteWrapper
from phillyleg.management.scraper_wrappers import LegistarApiWrapper
from phillyleg.management.scraper_wrappers import CouncilmaticDataStoreWrapper

class LegistarTests (TestCase):

    def setUp(self):
        self.legfiles_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'testlegfiles'
        )
        self.pdfs_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'pdfs'
        )

    def open_legfile(self, key):
        return open(os.path.join(self.legfiles_dir, 'key%s.html' % key))

    def test_RecognizeNotesRow(self):
        # The history on some filings (like key=73) have notes.  These need to
        # be detected.
        html = self.open_legfile('73').read()
        soup = bs.BeautifulSoup(html)

        wrapper = PhillyLegistarSiteWrapper(root_url='')
        file_record, attachment_records, action_records, minutes_records = \
            wrapper.scrape_legis_file(73, soup)

        self.assertEqual(
            len([act_rec for act_rec in action_records
                 if act_rec['notes']]), 2)

    def test_ResolutionPdfParsesCorrectly(self):
        wrapper = PhillyLegistarSiteWrapper(root_url='')
        expected_text = """\n\n\n\n\n\n\n\n\nCity of Philadelphia \n \n \n \n \nCity of Philadelphia \n- 1 - \n \n \n \nCity Council \nChief Clerk's Office \n402 City Hall \nPhiladelphia, PA 19107 \nRESOLUTION NO. 110406 \n \n \nIntroduced May 12, 2011 \n \n \nCouncilmember DiCicco \n \n \nReferred to the \nCommittee of the Whole   \n \n \nRESOLUTION \n \nAppointing David Campoli to the Board of Directors of the Center City District. \n \n \n \nRESOLVED, BY THE COUNCIL OF THE CITY OF PHILADELPHIA, \nTHAT David Campoli is hereby appointed as a member of the Board of Directors of the \nCenter City District, to serve in a term ending December 31, 2012. \n \n \n\n\n\nCity of Philadelphia \n \nRESOLUTION NO. 110406 continued \n \n \n \n \n \nCity of Philadelphia \n- 2 - \n \n \n \n \n\n"""

        # Raw stream
        resolution_pdf = open(os.path.join(self.pdfs_dir, '11530.pdf')).read()
        resolution_text = wrapper.extract_pdf_text(resolution_pdf)
        self.assertEqual(resolution_text, expected_text)

        # File URL
        resolution_pdf = 'file://' + os.path.join(self.pdfs_dir, '11530.pdf')
        resolution_text = wrapper.extract_pdf_text(resolution_pdf)
        self.assertEqual(resolution_text, expected_text)

        # Web URL -- This will only work if you're online.
        resolution_pdf = 'http://legislation.phila.gov/attachments/11530.pdf'
        resolution_text = wrapper.extract_pdf_text(resolution_pdf)
        self.assertEqual(resolution_text, expected_text)

    def test_DealsWith404PdfAddressesCorrectly(self):
        # I don't know why they'd be deleting these files, but when they do (and
        # they do) we have to handle it.
        wrapper = PhillyLegistarSiteWrapper(root_url='')
        expected_text = ''

        attachment_pdf = 'http://legislation.phila.gov/attachments/115954.pdf'
        attachment_text = wrapper.extract_pdf_text(attachment_pdf)
        self.assertEqual(attachment_text, expected_text)

    def test_MinutesDateParsedCorrectly(self):
        wrapper = PhillyLegistarSiteWrapper(root_url='')

        expected_date = dt.date(2083, 12, 6) # They learned nothing from Y2K
        taken_date = wrapper.get_minutes_date('http://www.bogus.com/path/mydoc_83-12-06_bill.pdf')

        self.assertEqual(taken_date, expected_date)

    def test_MinutesDocumentConstructedCorrectly(self):
        wrapper = PhillyLegistarSiteWrapper(root_url='')
        wrapper.get_minutes_date = mock.Mock(return_value=dt.date(2083, 12, 6))
        wrapper.extract_pdf_text = mock.Mock(return_value='This is the text')

        expected_doc = {'url': 'http://www.example.com/doc.pdf',
                        'fulltext': 'This is the text',
                        'date_taken': dt.date(2083, 12, 6)}
        minutes_doc = wrapper.get_minutes_doc('http://www.example.com/doc.pdf')

        self.assertEqual(minutes_doc, expected_doc)

    def test_PdfDataIsCached(self):
        wrapper = PhillyLegistarSiteWrapper(root_url='')
        wrapper.urlopen = mock.Mock(return_value=StringIO('<doc><pdf2xml></pdf2xml></doc>'))
        wrapper.extract_xml_text = mock.Mock()

        actions = [{'minutes_url': 'http://www.sample.com/file.pdf'},
                   {'minutes_url': 'http://www.sample.com/file.pdf'},
                   {'minutes_url': 'http://www.sample.com/other/file.pdf'}]
        minutes = wrapper.collect_minutes(actions)

        self.assertEqual(wrapper.urlopen.call_count, 2)

    def test_ConvertDateIsEmptyWhenNoDateGiven(self):
        wrapper = PhillyLegistarSiteWrapper(root_url='')

        self.assertEqual(wrapper.convert_date(None), '')

    def test_detectsErrorsCorrectly(self):
        wrapper = PhillyLegistarSiteWrapper(root_url='')

        soup = bs.BeautifulSoup(self.open_legfile('12000').read())
        self.assertTrue(wrapper.is_error_page(soup))

        soup = bs.BeautifulSoup(self.open_legfile('73').read())
        self.assertTrue(not wrapper.is_error_page(soup))

    def test_ExitsSilentlyOnNoNewContent(self):
        wrapper = PhillyLegistarSiteWrapper(root_url='')
        error_page = self.open_legfile('12000').read()
        wrapper.urlopen = mock.Mock(
            side_effect=lambda *a, **k: StringIO(error_page))

        wrapper.check_for_new_content(73)
        # Check that we've tried 100 additional items
        self.assertEqual(wrapper.urlopen.call_count, 100)

    def test_RaisesErrorOnTooMany404(self):
        from httplib import BadStatusLine
        wrapper = PhillyLegistarSiteWrapper(root_url='')
        wrapper.urlopen = mock.Mock(
            side_effect=BadStatusLine(500))

        self.assertRaises(BadStatusLine, wrapper.check_for_new_content, 73)
        # Check that we've retried the URL 10 items
        self.assertEqual(wrapper.urlopen.call_count, 10)


class OrmStoreTests (TestCase):
    def test_RecoversGracefullyAfterIntegrityError (self):
        from phillyleg.models import LegFile
        from django.db.utils import DatabaseError

        LegFile.objects.all().delete()
        LegFile.objects.create(title='testing', key=123)

        ds = CouncilmaticDataStoreWrapper()
        try:
            ds._save_or_ignore(LegFile, {'title':'testing', 'key':123})
            ds._save_or_ignore(LegFile, {'title':'testing', 'key':123})
        except DatabaseError:
            self.fail('Shouldn\'t have raised a DatabaseError')
        else:
            pass
