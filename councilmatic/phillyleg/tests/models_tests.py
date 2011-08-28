from unittest import TestCase
import os
import datetime as dt
import mock
from StringIO import StringIO

from phillyleg.models import *

class Tests_describing_LegFileTests (TestCase):
    
    def setUp(self):
        pass
    
    
    def test_FindsUniqueWordsCorrectly(self):
        legfile = LegFile()
        legfile.title = "Word1 word2 hyphen-word1 word1.      Word2 hyphen-word2... Word3..."
        words = legfile.unique_words()
        self.assertEqual(words, set(['word1', 'word2', 'word3', 'hyphen-word1', 'hyphen-word2']))
    
    
    def test_FindsMentionedLegfilesCorrectly(self):
        l123456 = LegFile(id='123456', key=1)
        l123456.save()
        
        l123456a = LegFile(id='123456-A', key=2)
        l123456a.save()
        
        l123456aa = LegFile(id='123456-AA', key=3)
        l123456aa.save()
        
        legfile = LegFile(title='This legfile mentions files 123456, 123457, and 123456-AA.')
        files = set(legfile.mentioned_legfiles())
        self.assertEqual(files, set([l123456, l123456aa]))
        
