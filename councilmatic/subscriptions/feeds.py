import smtplib

from datetime import date
from email.mime.text import MIMEText
from logging import getLogger

from django.db.models.manager import Manager
from django.template import Context
from django.template.loader import get_template

from models import ContentFeedRecord
from models import ContentFeedParameter

log = getLogger(__name__)


class ContentFeed (object):
    def get_content(self):
        """
        Returns the content items that appear in this feed.
        """
        raise NotImplementedError()

    def all(self):
        return self.get_content()

    def get_params(self):
        """
        Return a dictionary of keyword arguments that can be used to construct
        a feed identical to this one.  The values in the dictionary should be
        strings only.
        """
        raise NotImplementedError()

    def get_updated_since(self, previous):
        """
        Return the content items that have been updated since the given time.
        """
        raise NotImplementedError()

    def get_changes_to(self, item):
        """
        Returns a dictionary representing the changes to the item.  The nature
        of this dictionary may vary depending on the item type.
        """
        raise NotImplementedError()

    def get_last_updated_time(self):
        """
        Return the latest time that any content in the feed was updated.
        """
        raise NotImplementedError()

    class NotFound (Exception):
        pass


class ContentFeedLibrary (object):

    feeds = {}
    """Map of { feed_name : ContentFeedClass }"""

    _reverse = {}
    """Map of { ContentFeedClass : feed_name }. For reverse-lookup"""

    def __init__(self, shared=True):
        if not shared:
            self.feeds = {}
            self._reverse = {}

    def register(self, ContentFeedClass, name):
        """Add the given manager class to the registry by the given name."""
        self.feeds[name] = ContentFeedClass
        self._reverse[ContentFeedClass] = name

    def get_feed(self, record):
        """Retrieve a feed based on the given record."""
        ContentFeedClass = self.feeds[record.feed_name]
        kwargs = dict([(param.name, param.value)
                       for param in record.feed_params.all()])
        feed = ContentFeedClass(**kwargs)

        log.debug('The record %r represents the feed %r' % (record, feed))

        return feed

    def get_record(self, feed):
        """Retrieve a record describing the given feed."""
        ContentFeedClass = feed.__class__
        try:
            name = self._reverse[ContentFeedClass]
        except KeyError:
            log.debug('%s is not registered in the library: %s' %
                (feed.__class__.__name__, self.feeds))
            raise ContentFeedClass.NotFound(
                '%s is not registered in the library' %
                (feed.__class__.__name__,))

        record = ContentFeedRecord()
        record.feed_name = name
        record.save()

        for param_name, param_value in feed.get_params().items():
            param = ContentFeedParameter()
            param.name = param_name
            param.value = param_value
            record.feed_params.add(param)
            param.save()

        return record


class ContentFeedRecordUpdater (object):
    """Responsible for updating the metadata in a content feed"""

    def update(self, record, library=None):
        """
        Changes the last_updated of a legfiles feed to most recent intro date.

        Iterate through each item (page) in the feed (book) and check when it
        was last updated.  Be careful and don't use this as a matter of normal
        course; it may be slow.
        """
        if library is None:
            library = ContentFeedLibrary()

        feed = library.get_feed(record)

        all_content = feed.get_content()
        latest = max(feed.get_last_updated(item) for item in all_content)
        record.last_updated = latest
        record.save()

    def update_all(self, records, library=None):
        """Updates all the feeds in a collection (yes, it's just a for loop)"""
        for record in records:
            self.update(record, library)


class SubscriptionDispatcher (object):
    """
    The ``SubscriptionDispatcher`` gets new feed content from the library for
    you. You could go and get the feeds yourself, but the dispatcher will just
    go and grab anything new each day.

    The dispatcher will actually not deliver the content to you from one feed at
    a time. Instead it will take into account all the feeds that you're
    subscribed to and coallate the content. When the dispatcher gets the same
    content from two different managers, it'll make sure to deliver that content
    only once.
    """

    template_name = None
    """The file name of the template used to render the dispatch delivery
       "message"."""

    feed_updated_times = {}
    """A variable (essentialy global) mapping feeds to the last time that they
       were updated. Used as a cache."""

    def get_content_updates_for(self, subscriptions, library):
        """
        Check the library for the manager of each subscription feed. Check the
        managers for content that has been updated.

        Return a map of {piece_of_content: updates_as_dict} containing each
        piece of updated content and its updates as a dictionary.
        """
        log.debug('Checking for updates to %s in %s' % (subscriptions, library))

        content_changes = {}

        for subscription in subscriptions:
            feed = library.get_feed(subscription.feed_record)

            # Check whether the feed has been updated since the subscription
            # was last sent (this assumes that the feed_record has been
            # updated to accurately represent the feed).
            if subscription.last_sent < subscription.feed_record.last_updated:
                new_contents = feed.get_updates_since(subscription.last_sent)

                for item in new_contents:
                    changes = feed.get_changes_to(item)
                    content_changes[item].update(changes)

        log.debug('What changed: %s' % (content_changes,))

        return content_changes

    def render(self, subscriber, subscriptions, content_updates):
        """
        Render the given content updates to a template for the subscriber.
        """
        template = get_template(self.template_name)
        context = Context({'subscriber':subscriber,
                           'subscriptions': subscriptions,
                           'content':content_updates})
        return template.render(context)

    def deliver_to(self, subscriber, delivery_text):
        """
        Send the delivery_text to the subscriber by whatever method is
        appropriate for the dispatcher
        """
        raise NotImplementedError()

    def update_subscriptions(self, subscriptions):
        """
        Update the last_sent property of the subscriptions to the values found
        in feed_updated_times dictionary.  These times should have been cached
        during the get_content_updates_for step.
        """
        log.debug('Updating the subscriptions in %s' % (subscriptions))

        for subscription in subscriptions:
            if subscription.last_sent != subscription.feed_record.last_updated:
                subscription.last_sent = subscription.feed_record.last_updated
                subscription.save()

    def dispatch_subscriptions_for(self, subscriber, library=None):
        log.debug('Dispatching subscriptions for %s' % (subscriber))

        if library is None:
            library = ContentFeedLibrary()

        subscriptions = subscriber.subscriptions.all()

        content_updates = self.get_content_updates_for(subscriptions, library)
        delivery = self.render(subscriber, subscriptions, content_updates)
        self.deliver_to(subscriber, delivery)
        self.update_subscriptions(subscriptions)


class SubscriptionEmailer (SubscriptionDispatcher):
    template_name = 'subscriptions/email.txt'
    EMAIL_TITLE = "Philly Councilmatic %{date}s"

    def send_email(self, you, emailbody, emailsubject=None):
        smtphost = "smtp.gmail.com"
        smtpport = '465'
        me =  'philly.legislative.list'
        msg = MIMEText(smart_str(emailbody))
        msg['Subject'] = emailsubject or self.EMAIL_TITLE % {date: date.today()}
        msg['From'] = me
        msg['To'] = you
        s = smtplib.SMTP_SSL(smtphost, smtpport)
        s.login(me, 'phillydatacamp')
        s.sendmail(me, [you], msg.as_string())
        s.quit()

    def deliver_to(self, subscriber, delivery_text):
        """
        Send an email to the subscriber with the delivery_text
        """
        email_addr = subscriber.email
        email_body = delivery_text
