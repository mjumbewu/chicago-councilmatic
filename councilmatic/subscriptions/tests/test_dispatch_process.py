import datetime
from django.core import mail
from nose.tools import *
from subscriptions.feeds import ContentFeed
from subscriptions.feeds import ContentFeedLibrary
from subscriptions.management.commands import sendfeedupdates
from subscriptions.management.commands import updatefeeds
from subscriptions.models import Subscriber, ContentFeedRecord


@istest
def test_subscription_flow():
    Subscriber.objects.all().delete()
    ContentFeedRecord.objects.all().delete()
    del mail.outbox[:]
    
    library = ContentFeedLibrary(shared=True)

    # First, let's make some content
    content = [
        (datetime.date(2011, 12, 13), 1),
        (datetime.date(2011, 12, 13), 2),
        (datetime.date(2011, 12, 13), 3),
        (datetime.date(2011, 12, 13), 4),
        (datetime.date(2011, 12, 13), 5)
    ]

    # Then, let's make a ContentFeed that watches it.
    class EasyContentFeed (ContentFeed):
        def get_content(self):
            return content

        def get_params(self):
            return {}

        def get_updates_since(self, previous):
            return [t for t in content if t[0] > previous.date()]

        def get_last_updated_time(self):
            return max([t[0] for t in content])

        def get_changes_to(self, item, since):
            if since.date() < item[0]:
                return {'value': item[1]}, datetime.datetime(2011, 12, 13, 14, 15)
        
        def get_label(self):
            return 'Easy...'

    library.register(EasyContentFeed, 'easy')
    feed = EasyContentFeed()

    # Now we want a subscriber to subscribe to the feed.
    subscriber = Subscriber.objects.create()
    subscription = subscriber.subscribe(feed, library=library)

    # Assume that we last sent the subscription before the current items.
    subscription.last_sent = datetime.date(2011, 11, 11)
    subscription.save()

    # Now, update all the feeds dates/times and send out the updated content.
    update = updatefeeds.Command()
    update.handle()

    send = sendfeedupdates.Command()
    send.handle()

    # Check that we have a message to send.
    assert_equal(len(mail.outbox), 1)
    assert_equal(mail.outbox[0].subject[:19], 'Philly Councilmatic')
    assert_equal(mail.outbox[0].body,
                 ('\n\nPhiladelphia Councilmatic!\n==========================\n\nYou are subscribed to the following feeds:\n\n\n* Easy...\n\n\n--------------------------------------------------------------------------------\n\n \n\nvalue: 5\n\nMore at http://example.com\n\n\n--------------------------------------------------------------------------------\n\n \n\nvalue: 2\n\nMore at http://example.com\n\n\n--------------------------------------------------------------------------------\n\n \n\nvalue: 4\n\nMore at http://example.com\n\n\n--------------------------------------------------------------------------------\n\n \n\nvalue: 1\n\nMore at http://example.com\n\n\n--------------------------------------------------------------------------------\n\n \n\nvalue: 3\n\nMore at http://example.com\n\n\n\nTo manage your subscriptions, visit http://example.com/subscriptions/\n'))

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
    content.append((datetime.date(2012, 2, 4), 6))

    # Now, update all the feeds dates/times and send out the updated content.
    update = updatefeeds.Command()
    update.handle()

    send = sendfeedupdates.Command()
    send.handle()

    assert_equal(len(mail.outbox), 1)
