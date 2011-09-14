from unittest import TestCase
from nose.tools import *

import os
import datetime as dt
import mock
from StringIO import StringIO

from phillyleg.models import *

class Test_LegFile_uniqueWords (TestCase):

    @istest
    def FindsUniqueWordsCorrectly(self):
        legfile = LegFile()
        legfile.title = "Word1 word2 hyphen-word1 word1.      Word2 hyphen-word2... Word3..."

        words = legfile.unique_words()
        assert_equal(words, set(['word1', 'word2', 'word3', 'hyphen-word1', 'hyphen-word2']))


class Test__LegFile_mentionedLegfiles (TestCase):

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
        self.assertEqual(files, set([l123456, l123456aa]))


class Test__LegFile_lastActionDate:

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
