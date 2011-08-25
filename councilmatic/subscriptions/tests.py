"""
"""

import datetime
import pickle
        
from django.test import TestCase
from mock import Mock
from nose.tools import *

from subscriptions.decorators import serializable
from subscriptions.models import ContentFeed
from subscriptions.models import FeedData
from subscriptions.models import Subscriber
from subscriptions.models import Subscription
from subscriptions.models import SerializedObjectField

from subscriptions.management.feeds import FeedCollector
from subscriptions.management.feeds import FeedUpdater

# Models

class DummyFeedData (FeedData):
    queryset = [1,2,3,4]
    def calc_last_updated(self, item):
        return 2

class Test_ContentFeed_getContent (TestCase):
    
    def test_returns_the_query_results(self):
        feed = ContentFeed()
        feed.data = DummyFeedData()
        
        content = feed.get_content()
        self.assertEqual(content, [1, 2, 3, 4])


#class Test_ContentFeed_factory (TestCase):
#    
#    def test_creates_a_content_feed_object_with_a_ListQueryStore_from_a_list(self):
#        query = []
#        
#        feed = ContentFeed().factory(query, None)
#        
#        self.assertEqual(feed.querystore_type.name, 'list query store')
#    
#    def test_creates_a_content_feed_object_with_a_ModelQueryStore_from_a_QuerySet(self):
#        query = Subscriber.objects.all()
#        
#        feed = ContentFeed().factory(query, None)
#        
#        self.assertEqual(feed.querystore_type.name, 'model query store')
#    
#    def test_creates_a_content_feed_object_with_a_SearchQueryStore_from_a_SearchQuerySet(self):
#        import haystack.query
#        query = haystack.query.SearchQuerySet().all()
#        
#        feed = ContentFeed().factory(query, None)
#        
#        self.assertEqual(feed.querystore_type.name, 'search query store')


class Test_Subscription_save (TestCase):
    
    def setUp(self):
        user = self.user = Subscriber(); user.save()
        feed = self.feed = ContentFeed(); feed.data = FeedData(); feed.save()
        
        sub = self.sub = Subscription(subscriber=user, feed=feed); sub.save()
        
    def test_sets_lastSent_datetime_to_current_time_when_instance_is_new(self):
        subscription = Subscription(subscriber=self.user, feed=self.feed)
        
        before = datetime.datetime.now()
        subscription.save()
        after = datetime.datetime.now()
        
        self.assert_(before <= subscription.last_sent <= after)
        
    def test_doesnt_change_lastSent_datetime_on_instance_thats_already_saved(self):
        subscription = self.sub
        
        before = datetime.datetime.now()
        subscription.save()
        
        self.assert_(subscription.last_sent <= before)
    
    def test_will_retain_its_value_after_being_queryied(self):
        subscriptions = Subscription.objects.all()
        subscription = subscriptions[0]
        
        print subscriptions.query
        print subscription.feed.data
        assert_equal(type(subscription.feed.data), type(self.feed.data))


class Test_Subscriber_subscribe (TestCase):
    
    def setUp(self):
        feed = self.feed = ContentFeed(); feed.data = FeedData(); feed.save()
        subscriber = self.subscriber = Subscriber(); subscriber.save()
    
    def test_creates_a_new_subscription_associating_the_user_and_feed(self):
        subscription = self.subscriber.subscribe(self.feed)
        
        self.assertEqual(subscription.subscriber, self.subscriber)
        self.assertEqual(subscription.feed, self.feed)
        
    def test_doesnt_save_subscription_if_commit_is_false(self):
        subscription = self.subscriber.subscribe(self.feed, commit=False)
        
        self.assertIsNone(subscription.pk)


# Management commands

from phillyleg.models import LegFile
class NewLegFilesData (FeedData):
    queryset = LegFile.objects.all()
    def calc_last_updated(self, legfile):
        return legfile.intro_date
    
class Test_FeedUpdater_update (TestCase):
    
    def setUp(self):
        
        key = 0
        for intro, final in [ (datetime.date(2011, 1, 28), 
                               datetime.date(2011, 1, 29)), 
                              (datetime.date(2010, 7, 28), 
                               datetime.date(2010, 7, 29)), 
                              (datetime.date(2011, 8, 17), 
                               datetime.date(2011, 8, 18)), 
                              (datetime.date(2006, 12, 11), 
                               datetime.date(2006, 12, 12)), 
                              (datetime.date(2006, 12, 12), 
                               datetime.date(2006, 12, 13)) ]:
            LegFile(intro_date=intro, final_date=final, key=key).save()
            key += 1
        
        self.feed = ContentFeed()
        self.feed.data = NewLegFilesData()
    
    def test_changes_the_lastUpdated_of_a_legfiles_feed_to_most_recent_intro_date(self):
        updater = FeedUpdater()
        
        updater.update(self.feed)
        
        self.assertEqual(self.feed.last_updated, datetime.date(2011, 8, 17))


class MyListFeedData (FeedData):
    def __init__(self, l):
        self.queryset = l

class Test_FeedUpdater_updateAll (TestCase):
    
    def setUp(self):
        
        self.feeds = [ ContentFeed.factory(MyListFeedData(['hello'])),
                       ContentFeed.factory(MyListFeedData(['world'])) ]
    
    def test_calls_get_last_updated_on_all_feed_objects(self):
        self.feeds[0].get_last_updated = Mock(return_value=datetime.datetime.now())
        self.feeds[1].get_last_updated = Mock(return_value=datetime.datetime.now())
        
        updater = FeedUpdater()
        
        updater.update_all(self.feeds)
        
        self.feeds[0].get_last_updated.assert_called_with('hello')
        self.feeds[1].get_last_updated.assert_called_with('world')


class Test_FeedCollector_collectNewContent (TestCase):
    
    def test_returns_exactly_those_items_newer_than_the_last_sent_datetime(self):
        feed = Mock()
        feed.get_content = Mock(return_value=[datetime.datetime(2009, 1, 1),
                                              datetime.datetime(2010, 1, 1),
                                              datetime.datetime(2011, 1, 1),
                                              datetime.datetime(2012, 1, 1),])
        feed.get_last_updated = lambda item: item
        last_sent = datetime.datetime(2010, 1, 1)
        
        collector = FeedCollector()
        content = collector.collect_new_content(feed, last_sent)
        
        self.assertEqual(content, [datetime.datetime(2011, 1, 1), 
                                   datetime.datetime(2012, 1, 1),])
    
    def test_converts_dates_to_datetimes_for_comparison(self):
        feed = Mock()
        feed.get_content = Mock(return_value=[False, '1', '2', '3', '4', '5'])
        
        # The last_sent value is compared with feed.get_last_updated(...), so
        # check one direction first...
        feed.get_last_updated = lambda item: datetime.date(2011, 8, 23)
        last_sent = datetime.datetime(2011, 8, 23)
        
        collector = FeedCollector()
        try:
            content = collector.collect_new_content(feed, last_sent)
        except TypeError, e:
            self.fail(e)
        
        # ...then check the other direction.
        feed.get_last_updated = lambda item: datetime.datetime(2011, 8, 23)
        last_sent = datetime.date(2011, 8, 23)
        
        collector = FeedCollector()
        try:
            content = collector.collect_new_content(feed, last_sent)
        except TypeError, e:
            self.fail(e)


class Test_SerializedObjectField_toPython (TestCase):
    
    def test_converts_unicode_strings_to_nonunicode_before_loading(self):
        pickled_list = u'(lp0\n.'
        field = SerializedObjectField()
        
        result = field.to_python(pickled_list)
        
        self.assertEqual(result, [])

class Test_serializable_decorator:

    @istest
    def calls_the_decorated_function_when_called_with_parameters(self):
        def myfunc(arg):
            return arg+5
        serializable_func = serializable(myfunc)
        
        assert serializable_func(5) == 10

    @istest
    def returns_the_decorated_function_when_called_without_parameters(self):
        @serializable
        def myfunc(arg):
            return arg+5
        serializable_func = serializable(myfunc)
        
        assert serializable_func() == myfunc
