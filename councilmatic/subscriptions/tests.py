"""
"""

from django.test import TestCase
from mock import Mock

from subscriptions.models import ContentFeed
from subscriptions.models import StoredQuery

class Test_StoredQuery_run (TestCase):
    
    def setUp(self):
        StoredQuery(code='a').save()
        StoredQuery(code='b').save()
        StoredQuery(code='c').save()
    
    def test_returns_the_results_of_the_stored_query(self):
        query = StoredQuery()
        query.code = 'StoredQuery.objects.all()'
        
        queryset = query.run()
        self.assertEqual(list(queryset), list(StoredQuery.objects.all()))


class Test_ContentFeed_getContent (TestCase):
    
    def test_returns_the_results_of_the_stored_querys_run_method(self):
        feed = ContentFeed()
        feed.query = StoredQuery()
        feed.query.run = Mock(return_value='value')
        
        content = feed.get_content()
        self.assertEqual(content, 'value')

