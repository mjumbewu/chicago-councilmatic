"""
"""

import datetime
import pickle
        
from django.test import TestCase
from mock import Mock

from subscriptions.models import ContentFeed
from subscriptions.models import Subscriber
from subscriptions.models import Subscription

from subscriptions.management.feeds import FeedUpdater

# Models

class Test_ContentFeed_getContent (TestCase):
    
    def test_returns_the_unpickled_queryset(self):
        feed = ContentFeed()
        feed.queryset = pickle.dumps([1, 2])
        
        content = feed.get_content()
        self.assertEqual(content, [1,2])


class Test_ContentFeed_factory (TestCase):
    
    def test_creates_a_content_feed_object_with_pickled_queryset_and_updated_calculator(self):
        feed = ContentFeed().factory('hello', 'world')
        
        self.assertEqual(pickle.loads(feed.queryset), 'hello')
        self.assertEqual(pickle.loads(feed.last_updated_calc), 'world')


class Test_Subscription_save (TestCase):
    
    def setUp(self):
        user = self.user = Subscriber(); user.save()
        feed = self.feed = ContentFeed.factory([], []); feed.save()
        
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


class Test_Subscriber_subscribe (TestCase):
    
    def setUp(self):
        feed = self.feed = ContentFeed.factory([], int); feed.save()
        subscriber = self.subscriber = Subscriber(); subscriber.save()
    
    def test_creates_a_new_subscription_associating_the_user_and_feed(self):
        subscription = self.subscriber.subscribe(self.feed)
        
        self.assertEqual(subscription.subscriber, self.subscriber)
        self.assertEqual(subscription.feed, self.feed)
        
    def test_doesnt_save_subscription_if_commit_is_false(self):
        subscription = self.subscriber.subscribe(self.feed, commit=False)
        
        self.assertIsNone(subscription.pk)


# Management commands

import phillyleg.models as phillyleg
def _get_latest_legfile_datetime(legfiles):
    return max([legfile.intro_date for legfile in legfiles])

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
            phillyleg.LegFile(
                intro_date=intro, 
                final_date=final,
                key=key).save()
            key += 1
        
        self.feed = ContentFeed.factory(
            phillyleg.LegFile.objects.all(), 
            _get_latest_legfile_datetime)
    
    def test_changes_the_lastUpdated_of_a_legfiles_feed_to_most_recent_intro_date(self):
        updater = FeedUpdater()
        
        updater.update(self.feed)
        
        self.assertEqual(self.feed.last_updated, datetime.date(2011, 8, 17))


class Test_FeedUpdater_updateAll (TestCase):
    
    def setUp(self):
        self.feeds = [ ContentFeed.factory('hello', None),
                       ContentFeed.factory('world', None) ]
    
    def test_calls_get_last_updated_on_all_feed_objects(self):
        self.feeds[0].get_last_updated = Mock(return_value=datetime.datetime.now())
        self.feeds[1].get_last_updated = Mock(return_value=datetime.datetime.now())
        
        updater = FeedUpdater()
        
        updater.update_all(self.feeds)
        
        self.feeds[0].get_last_updated.assert_called_with('hello')
        self.feeds[1].get_last_updated.assert_called_with('world')

