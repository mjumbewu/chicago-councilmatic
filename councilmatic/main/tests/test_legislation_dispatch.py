from datetime import (date, datetime, timedelta)
from django.core import mail

from nose.tools import *
from mock import *

from main import feeds

from bookmarks.models import Bookmark
from subscriptions.management.commands import sendfeedupdates
from subscriptions.management.commands import updatefeeds
from subscriptions.models import Subscriber, ContentFeedRecord

from phillyleg.models import LegFile, LegAction


class SubscriptionFlowTesterMixin (object):
    """
    Integration test base class for specific types of subscription feeds
    """

    def create_initial_content(self):
        raise NotImplementedError()

    def create_updated_content(self):
        raise NotImplementedError()

    def get_feed(self):
        raise NotImplementedError()

    def get_initial_dispatch_message(self):
        raise NotImplementedError()

    @istest
    def test_subscription_flow(self):
        Bookmark.objects.all().delete()
        LegFile.objects.all().delete()
        Subscriber.objects.all().delete()
        ContentFeedRecord.objects.all().delete()
        del mail.outbox[:]

        # First, let's get the ContentFeed objects for this package.  One of them
        # should watch this content.
        feeds.library.clear()
        feeds.register_feeds()

        # Then, let's make some content
        self.subscriber = subscriber = Subscriber.objects.create()

        feed = self.get_feed()

        self.create_initial_content()

        # Now we want a subscriber to subscribe to the feed.
        subscription = subscriber.subscribe(feed, library=feeds.library)

        # Assume that we last sent the subscription before the current items.
        subscription.last_sent = date(2011, 11, 11)
        subscription.save()

        # Now, update all the feeds dates/times and send out the updated content.
        update = updatefeeds.Command()
        update.handle()

        send = sendfeedupdates.Command()
        send.handle()

        # Check that we have a message to send.
        assert_equal(len(mail.outbox), 1)
        assert_equal(mail.outbox[0].subject[:19], 'Philly Councilmatic')
        assert_equal(mail.outbox[0].body, self.get_initial_dispatch_message())

        # Cool.  Clear the mailbox.
        del mail.outbox[:]

        # Now, if we update the feed times and send the updated content, there
        # should be nothing to send.
        update = updatefeeds.Command()
        update.handle()

        send = sendfeedupdates.Command()
        send.handle()

        assert_equal(len(mail.outbox), 0)

        # Put something else into the feed.
        self.create_updated_content()

        # Now, update all the feeds dates/times and send out the updated content.
        update = updatefeeds.Command()
        update.handle()

        send = sendfeedupdates.Command()
        send.handle()

        assert_equal(len(mail.outbox), 1)

        # ... and at the end, return to a clean state.
        feeds.library.clear()


class TestNewLegislationFeedDispatching(SubscriptionFlowTesterMixin):
    def create_initial_content(self):
        LegFile.objects.create(key=1, id='a', title="first", intro_date=date(2011, 12, 13), type="Bill")
        LegFile.objects.create(key=2, id='b', title="second", intro_date=date(2011, 12, 13), type="Bill")
        LegFile.objects.create(key=3, id='c', title="third", intro_date=date(2011, 12, 13), type="Bill")

    def create_updated_content(self):
        LegFile.objects.create(key=4, id='d', title="fourth", intro_date=date(2012, 2, 4), type="Bill")

    def get_feed(self):
        return feeds.NewLegislationFeed()

    def get_initial_dispatch_message(self):
        return ('Philadelphia Councilmatic!\n==========================\n\nY'
                'ou are subscribed to the following feeds:\n\n\n* bookmarked'
                ' content\n\n* newly introduced legislation\n\n\n\n---------'
                '-----------------------------------------------------------'
                '------------\n\nBILL a\n\nTitle: first\n\nMore at http://ex'
                'ample.com/legislation/1\n\n\n------------------------------'
                '--------------------------------------------------\n\nBILL '
                'b\n\nTitle: second\n\nMore at http://example.com/legislatio'
                'n/2\n\n\n--------------------------------------------------'
                '------------------------------\n\nBILL c\n\nTitle: third\n'
                '\nMore at http://example.com/legislation/3\n\n')


class TestLegislationUpdatesFeedDispatching(SubscriptionFlowTesterMixin):
    def create_initial_content(self):
        LegFile.objects.create(key=1, id='a', title="first", intro_date=date(2011, 12, 13), type="Bill")

    def create_updated_content(self):
        legfile = LegFile.objects.get(key=1)
        LegAction.objects.create(file=legfile, date_taken=date(2012, 2, 4), description="An Action!")

    def get_feed(self):
        return feeds.LegislationUpdatesFeed(key=1)

    def get_initial_dispatch_message(self):
        return ('Philadelphia Councilmatic!\n==========================\n\nYou '
                'are subscribed to the following feeds:\n\n\n* bookmarked conte'
                'nt\n\n* updates to a piece of legislation\n\n\n\n-------------'
                '--------------------------------------------------------------'
                '-----\n\nBILL a\n\nMore at http://example.com/legislation/1\n'
                '\n')


class TestSearchResultsFeedDispatching(SubscriptionFlowTesterMixin):
    def create_initial_content(self):
        LegFile.objects.create(key=1, id='a', title="first streets", intro_date=date(2011, 12, 11), type="Bill")
        LegFile.objects.create(key=2, id='b', title="second trees", intro_date=date(2011, 12, 12), type="Bill")
        LegFile.objects.create(key=3, id='c', title="third streets", intro_date=date(2011, 12, 13), type="Bill")
        LegFile.objects.create(key=4, id='d', title="fourth streets", intro_date=date(2011, 12, 14), type="Bill")

        from django.core.management import call_command
        call_command('rebuild_index', interactive=False)

    def create_updated_content(self):
        LegFile.objects.create(key=5, id='e', title="streets fifth", intro_date=date(2012, 2, 4), type="Bill")
        LegFile.objects.create(key=6, id='f', title="streets sixth", intro_date=date(2012, 2, 4), type="Communication")
        LegFile.objects.create(key=7, id='g', title="streets seventh", intro_date=date(2011, 12, 13), type="Bill")

        from django.core.management import call_command
        call_command('rebuild_index', interactive=False)

    def get_feed(self):
        return feeds.SearchResultsFeed(search_filter='{"content":"streets", "file_type":["Bill"]}')

    def get_initial_dispatch_message(self):
        return ('Philadelphia Councilmatic!\n==========================\n\nYou '
                'are subscribed to the following feeds:\n\n\n* bookmarked conte'
                'nt\n\n* results of a search query\n\n\n\n---------------------'
                '-----------------------------------------------------------\n'
                '\nNONE phillyleg.legfile.1\n\nTitle: first streets\n\nMore at '
                'http://example.comNone\n\n\n----------------------------------'
                '----------------------------------------------\n\nNONE phillyl'
                'eg.legfile.3\n\nTitle: third streets\n\nMore at http://exampl'
                'e.comNone\n\n\n-----------------------------------------------'
                '---------------------------------\n\nNONE phillyleg.legfile.4'
                '\n\nTitle: fourth streets\n\nMore at http://example.comNone\n'
                '\n')

class TestBookmarkFeedDispatching(SubscriptionFlowTesterMixin):
    def create_initial_content(self):
        LegFile.objects.create(key=1, id='a', title="first", intro_date=date(2011, 12, 13), type="Bill")
        LegFile.objects.create(key=2, id='b', title="second", intro_date=date(2011, 12, 13), type="Bill")
        LegFile.objects.create(key=3, id='c', title="third", intro_date=date(2011, 12, 13), type="Bill")

        legfile = LegFile.objects.get(key=1)
        self.subscriber.bookmarks.add(Bookmark(content=legfile))

    def create_updated_content(self):
        legfile = LegFile.objects.get(key=1)
        LegAction.objects.create(file=legfile, date_taken=date(2012, 2, 4), description="An Action!")

    def get_feed(self):
        return feeds.BookmarkedContentFeed(self.subscriber)

    def get_initial_dispatch_message(self):
        return ('Philadelphia Councilmatic!\n==========================\n\nYou '
                'are subscribed to the following feeds:\n\n\n* bookmarked conte'
                'nt\n\n* bookmarked content\n\n\n\n----------------------------'
                '----------------------------------------------------\n\nBILL a'
                '\n\nMore at http://example.com/legislation/1\n\n')
