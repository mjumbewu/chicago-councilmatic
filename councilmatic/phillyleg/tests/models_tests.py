from unittest import TestCase
from nose.tools import *

import os
import datetime as dt
import mock
from StringIO import StringIO

from phillyleg.management.scraper_wrappers import PhillyLegistarSiteWrapper
from phillyleg.models import *

class Test_LegFile_uniqueWords:

    @istest
    def FindsUniqueWordsCorrectly(self):
        legfile = LegFile()
        legfile.title = "Word1 word2 hyphen-word1 word1.      Word2 hyphen-word2... Word3..."

        words = legfile.unique_words()
        assert_equal(words, set(['word1', 'word2', 'word3', 'hyphen-word1', 'hyphen-word2']))


class Test__LegFile_mentionedLegfiles:

    def setup(self):
        LegFile.objects.all().delete()

    @istest
    def FindsMentionedLegfilesCorrectly(self):
        l123456 = LegFile(id='123456', key=1)
        l123456.save()

        l123456a = LegFile(id='123456-A', key=2)
        l123456a.save()

        l123456aa = LegFile(id='123456-AA', key=3)
        l123456aa.save()

        legfile = LegFile(title='This legfile mentions files 123456, 123457, and 123456-AA.')

        files = set(legfile.mentioned_legfiles())
        assert_equal(files, set([l123456, l123456aa]))


class Test__LegFile_lastActionDate:

    def setup(self):
        LegFile.objects.all().delete()

    @istest
    def is_none_when_legfile_has_no_actions (self):
        legfile = LegFile()

        assert_is_none(legfile.last_action_date)

    @istest
    def is_last_action_dateTaken (self):
        legfile = LegFile(id='123456', key=1)
        legfile.save()
        legfile.actions.add(LegAction(date_taken=dt.date(2011, 8, 11)))
        legfile.actions.add(LegAction(date_taken=dt.date(2011, 8, 19)))
        legfile.actions.add(LegAction(date_taken=dt.date(2011, 8, 12)))

        assert_equal(legfile.last_action_date, dt.date(2011, 8, 19))


class Test__LegFile_timeline:

    def setup(self):
        LegFile.objects.all().delete()

    @istest
    def is_empty_when_legfile_has_no_actions (self):
        legfile = LegFile(id='123456', key=1)
        legfile.save()

        assert_equal(len(legfile.timeline), 0)

    @istest
    def collects_actions_by_date_taken (self):
        legfile = LegFile(id='123456', key=1)
        legfile.save()
        legfile.actions.add(LegAction(date_taken=dt.date(2011, 8, 11), description='a'))
        legfile.actions.add(LegAction(date_taken=dt.date(2011, 8, 11), description='b'))
        legfile.actions.add(LegAction(date_taken=dt.date(2011, 8, 12), description='c'))
        legfile.save()

        assert_equal(len(legfile.timeline), 2)
        assert_equal(len(legfile.timeline[dt.date(2011, 8, 11)]), 2)
        assert_equal(len(legfile.timeline[dt.date(2011, 8, 12)]), 1)

    @istest
    def always_iterates_through_keys_sorted (self):
        legfile = LegFile(id='123456', key=1)
        legfile.save()
        legfile.actions.add(LegAction(date_taken=dt.date(2011, 8, 11), description='a'))
        legfile.actions.add(LegAction(date_taken=dt.date(2011, 8, 12), description='b'))
        legfile.actions.add(LegAction(date_taken=dt.date(2011, 8, 10), description='c'))
        legfile.actions.add(LegAction(date_taken=dt.date(2011, 8, 15), description='d'))
        legfile.actions.add(LegAction(date_taken=dt.date(2011, 8, 13), description='e'))
        legfile.save()

        dates = [date for date in legfile.timeline]
        assert_equal(dates, [dt.date(2011, 8, 10),
                             dt.date(2011, 8, 11),
                             dt.date(2011, 8, 12),
                             dt.date(2011, 8, 13),
                             dt.date(2011, 8, 15)])


class Test__LegFile_refresh:

    def setUp(self):
        self.legfiles_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'testlegfiles')
        class PhillyLegistarFileWrapper (PhillyLegistarSiteWrapper):
            def urlopen(wrapper, *args, **kwargs):
                return self.open_legfile(73)
        self.PhillyLegistarFileWrapper = PhillyLegistarFileWrapper

    def open_legfile(self, key):
        return open(os.path.join(self.legfiles_dir, 'key%s.html' % key))

    @istest
    def updates_file_if_data_is_stale(self):
        last_update_time = dt.datetime.now() - dt.timedelta(days=1, hours=1)
        legfile = LegFile(id='123456', key=73, updated_datetime=last_update_time, title='abcde')

        legfile.get_data_source = lambda: self.PhillyLegistarFileWrapper()

        legfile.refresh()
        assert_equal(legfile.title, '''Providing for the approval by the Council of the City of Philadelphia of a Revised Five Year Financial Plan for the City of Philadelphia covering Fiscal Years 2001 through 2005, and incorporating proposed changes with respect to Fiscal Year 2000, which is to be submitted by the Mayor to the Pennsylvania Intergovernmental Cooperation Authority (the "Authority") pursuant to the Intergovernmental Cooperation Agreement, authorized by an ordinance of this Council approved by the Mayor on January 3, 1992 (Bill No. 1563-A), by and between the City and the Authority.''')

    @istest
    def updates_file_if_data_is_stale(self):
        last_update_time = dt.datetime.now() - dt.timedelta(hours=23)
        legfile = LegFile(id='123456', key=73, updated_datetime=last_update_time, title='abcde')

        legfile.get_data_source = lambda: self.PhillyLegistarFileWrapper()

        legfile.refresh()
        assert_equal(legfile.title, '''abcde''')
