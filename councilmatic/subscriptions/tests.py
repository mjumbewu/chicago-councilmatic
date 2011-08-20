"""
"""

import datetime

from django.test import TestCase
from mock import Mock

from subscriptions.models import ContentFeed
from subscriptions.models import StoredQuery
from subscriptions.models import Subscriber
from subscriptions.models import Subscription

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


class Test_Subscription_save (TestCase):
    
    def setUp(self):
        query = StoredQuery(code='query code'); query.save()
        
        user = self.user = Subscriber(); user.save()
        feed = self.feed = ContentFeed(query=query); feed.save()
        
        sub = self.sub = Subscription(user=user, feed=feed); sub.save()
        
    def test_sets_lastSent_datetime_to_current_time_when_instance_is_new(self):
        subscription = Subscription(user=self.user, feed=self.feed)
        
        before = datetime.datetime.now()
        subscription.save()
        after = datetime.datetime.now()
        
        self.assert_(before <= subscription.last_sent <= after)
        
    def test_doesnt_change_lastSent_datetime_on_instance_thats_already_saved(self):
        subscription = self.sub
        
        before = datetime.datetime.now()
        subscription.save()
        
        self.assert_(subscription.last_sent <= before)


class Test_Subscriber_subscribe (TestCase):
    
    def setUp(self):
        query = StoredQuery(code='query code'); query.save()
        feed = self.feed = ContentFeed(query=query); feed.save()
        subscriber = self.subscriber = Subscriber(); subscriber.save()
    
    def test_creates_a_new_subscription_associating_the_user_and_feed(self):
        subscription = self.subscriber.subscribe(self.feed)
        
        self.assertEqual(subscription.user, self.subscriber)
        self.assertEqual(subscription.feed, self.feed)
        
    def test_doesnt_save_subscription_if_commit_is_false(self):
        subscription = self.subscriber.subscribe(self.feed, commit=False)
        
        self.assertIsNone(subscription.pk)

