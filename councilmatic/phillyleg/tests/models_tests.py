from unittest import TestCase
from nose.tools import *

import os
import datetime as dt
import mock
from StringIO import StringIO

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
        legfile.actions.add(LegAction(date_taken=dt.datetime(2011, 8, 11)))
        legfile.actions.add(LegAction(date_taken=dt.datetime(2011, 8, 19)))
        legfile.actions.add(LegAction(date_taken=dt.datetime(2011, 8, 12)))

        assert_equal(legfile.last_action_date, dt.datetime(2011, 8, 19))


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
        legfile.actions.add(LegAction(date_taken=dt.datetime(2011, 8, 11), description='a'))
        legfile.actions.add(LegAction(date_taken=dt.datetime(2011, 8, 11), description='b'))
        legfile.actions.add(LegAction(date_taken=dt.datetime(2011, 8, 12), description='c'))
        legfile.save()

        assert_equal(len(legfile.timeline), 2)
        assert_equal(len(legfile.timeline[dt.datetime(2011, 8, 11)]), 2)
        assert_equal(len(legfile.timeline[dt.datetime(2011, 8, 12)]), 1)
