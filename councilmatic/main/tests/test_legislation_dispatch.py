from datetime import (date, datetime, timedelta)
from django.core import mail

from nose.tools import *
from mock import *

from subscriptions.management.commands import sendfeedupdates
from subscriptions.management.commands import updatefeeds
from subscriptions.models import Subscriber

from phillyleg.models import LegFile


@istest
def test_subscription_flow():
    LegFile.objects.all().delete()

    # First, let's make some content
    LegFile.objects.create(key=1, id='a', title="first", intro_date=date(2011, 12, 13), type="Bill")
    LegFile.objects.create(key=2, id='b', title="second", intro_date=date(2011, 12, 13), type="Bill")
    LegFile.objects.create(key=3, id='c', title="third", intro_date=date(2011, 12, 13), type="Bill")

    # Then, let's get the ContentFeed objects for this package.  One of them
    # should watch this content.
    from main import feeds
    feed = feeds.NewLegislationFeed()

    # Now we want a subscriber to subscribe to the feed.
    subscriber = Subscriber.objects.create()
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
    assert_equal(mail.outbox[0].body,
                 ('Philadelphia Councilmatic!\n==========================\n\nY'
                  'ou are subscribed to the following feeds:\n\n\n* bookmarked'
                  ' content\n\n* newly introduced legislation\n\n\n\n---------'
                  '-----------------------------------------------------------'
                  '------------\n\nBILL a\n\nTitle: first\n\nMore at http://ex'
                  'ample.com/legislation/1\n\n\n------------------------------'
                  '--------------------------------------------------\n\nBILL '
                  'b\n\nTitle: second\n\nMore at http://example.com/legislatio'
                  'n/2\n\n\n--------------------------------------------------'
                  '------------------------------\n\nBILL c\n\nTitle: third\n'
                  '\nMore at http://example.com/legislation/3\n\n'))

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
    LegFile.objects.create(key=4, id='d', title="fourth", intro_date=date(2012, 2, 4), type="Bill")

    # Now, update all the feeds dates/times and send out the updated content.
    update = updatefeeds.Command()
    update.handle()

    send = sendfeedupdates.Command()
    send.handle()

    assert_equal(len(mail.outbox), 1)

    # ... and at the end, return to a clean state.
    feeds.library.clear()
