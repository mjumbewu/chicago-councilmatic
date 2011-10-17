from datetime import (date, datetime, timedelta)

from nose.tools import *
from mock import *

from main.feeds import (NewLegislationFeed, LegislationUpdatesFeed, SearchResultsFeed)
from subscriptions.models import (ContentFeedRecord, Subscriber, Subscription)
from subscriptions.feeds import (import_all_feeds, ContentFeedRecordUpdater, SubscriptionDispatcher)

class Test_NewLegislationFeed_getLastUpdated:

    @istest
    def returns_the_intro_date_of_a_piece_of_legislation (self):
        legislation = Mock()
        legislation.intro_date = 5

        feed_data = NewLegislationFeed()
        last_updated = feed_data.get_last_updated(legislation)

        assert_equal(last_updated, 5)


class Test_NewLegislationFeed_getChangesTo:

    @istest
    def returns_the_title_if_introduced_since_given_time (self):
        legislation = Mock()
        legislation.intro_date = date.today()
        legislation.title = 'Hello, world!'

        feed_data = NewLegislationFeed()
        changes = feed_data.get_changes_to(legislation, datetime.min)

        assert_equal(changes, {'Title': 'Hello, world!'})

    @istest
    def returns_an_empty_dict_if_introduced_before_given_time (self):
        legislation = Mock()
        legislation.intro_date = date.min
        legislation.title = 'Hello, world!'

        feed_data = NewLegislationFeed()
        changes = feed_data.get_changes_to(legislation, datetime.now())

        assert_equal(changes, {})


class Test_SearchResultsFeed_getLastUpdated:

    @istest
    def returns_the_intro_date_of_a_piece_of_legislation (self):
        from phillyleg.models import LegFile
        legislation = LegFile()
        legislation.intro_date = date(2011,8,22)

        feed_data = SearchResultsFeed(None)
        last_updated = feed_data.get_last_updated(legislation)

        assert_equal(last_updated, date(2011,8,22))

    @istest
    def returns_the_date_taken_of_a_minutes_document (self):
        from phillyleg.models import LegMinutes
        minutes = LegMinutes()
        minutes.date_taken = date(2011,8,23)

        feed_data = SearchResultsFeed(None)
        last_updated = feed_data.get_last_updated(minutes)

        assert_equal(last_updated, date(2011,8,23))


class Test_LegislationUpdatesFeed_getContent:

    @istest
    def uses_all_when_no_keywords_are_supplied_to_init (self):
        feed_data = LegislationUpdatesFeed()
        feed_data.manager = Mock()
        feed_data.manager.all = Mock(return_value=[5])

        qs = feed_data.get_content()

        assert_equal(feed_data.manager.all.call_count, 1)
        assert_equal(qs, [5])

    @istest
    def uses_filter_when_keywords_are_supplied_to_init (self):
        feed_data = LegislationUpdatesFeed(a=1, b=2)
        feed_data.manager = Mock()
        feed_data.manager.filter = Mock(return_value=[5])

        qs = feed_data.get_content()

        assert_equal(feed_data.manager.filter.call_count, 1)
        feed_data.manager.filter.assert_called_with(a=1,b=2)
        assert_equal(qs, [5])

class Test_LegislationUpdatesFeed_getLastUpdated:

    @istest
    def returns_the_intro_date_if_has_no_actions_or_final_date (self):
        legislation = Mock()
        legislation.intro_date = date(2011, 8, 5)
        legislation.final_date = None
        legislation.actions.all = Mock(return_value=[])
        feed_data = LegislationUpdatesFeed()

        last_updated = feed_data.get_last_updated(legislation)

        assert_equal(last_updated, date(2011, 8, 5))

    @istest
    def returns_the_final_date_if_available (self):
        legislation = Mock()
        legislation.intro_date = date(2011, 8, 5)
        legislation.final_date = date(2011, 8, 10)
        legislation.actions.all = Mock(return_value=[])
        feed_data = LegislationUpdatesFeed()

        last_updated = feed_data.get_last_updated(legislation)

        assert_equal(last_updated, date(2011, 8, 10))

    @istest
    def returns_the_latest_action_date_if_has_no_final_date (self):
        legislation = Mock()
        legislation.intro_date = date(2011, 8, 5)
        legislation.final_date = None
        action1 = Mock(); action1.date_taken = date(2011, 8, 6)
        action2 = Mock(); action2.date_taken = date(2011, 8, 7)
        action3 = Mock(); action3.date_taken = date(2011, 8, 8)
        legislation.actions.all = Mock(return_value=[action1, action2, action3])
        feed_data = LegislationUpdatesFeed()

        last_updated = feed_data.get_last_updated(legislation)

        assert_equal(last_updated, date(2011, 8, 8))

    @istest
    def returns_the_lasest_action_date_final_date (self):
        legislation = Mock()
        legislation.intro_date = date(2011, 8, 5)
        legislation.final_date = date(2011, 8, 10)
        action1 = Mock(); action1.date_taken = date(2011, 8, 7)
        action2 = Mock(); action2.date_taken = date(2011, 8, 9)
        action3 = Mock(); action3.date_taken = date(2011, 8, 11)
        legislation.actions.all = Mock(return_value=[action1, action2, action3])
        feed_data = LegislationUpdatesFeed()

        last_updated = feed_data.get_last_updated(legislation)

        assert_equal(last_updated, date(2011, 8, 11))


class Test_Dispatching_feed_subscriptions:

    def setup (self):
        Subscriber.objects.all().delete()
        Subscription.objects.all().delete()
        ContentFeedRecord.objects.all().delete()

        import_all_feeds()

        subscriber = Subscriber.objects.create(email='bob@123.com')
        updater = ContentFeedRecordUpdater()
        dispatcher = SubscriptionDispatcher()
        dispatcher.deliver_to = Mock()
        dispatcher.render = Mock()

        self.subscriber = Mock(wraps=subscriber)
        self.updater = Mock(wraps=updater)
        self.dispatcher = Mock(wraps=dispatcher)

    def _dispatch_for_feed(self, feed):
        self.subscriber.subscribe(feed)
        self.subscriber.last_sent = datetime.now() - timedelta(days=180)
        self.updater.update_all(ContentFeedRecord.objects.all())
        self.dispatcher.dispatch_subscriptions_for(self.subscriber)

    @istest
    def works_for_NewLegislationFeeds (self):
        feed = NewLegislationFeed()
        self._dispatch_for_feed(feed)

    @istest
    def works_for_SearchResultsFeed (self):
        feed = SearchResultsFeed("(AND: ('content', u'smoking'), ('type__in', [u'Bill']))")
        self._dispatch_for_feed(feed)

    @istest
    def works_for_LegislationUpdatesFeed (self):
        feed = LegislationUpdatesFeed(pk="12345")
        self._dispatch_for_feed(feed)
