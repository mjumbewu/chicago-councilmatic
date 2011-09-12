import datetime
import logging
from django.db import models

import django.contrib.auth.models as auth
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import haystack.query as haystack

from subscriptions.fields import SerializedObjectField

# Content Feeds

class FeedData (object):
    queryset = None
    def calc_last_updated(self, item):
        raise NotImplementedError()


#class ListQueryStore (models.Model):
#    value = SerializedObjectField()
#
#    def is_the_same_as(self, querystore):
#        return type(querystore) is type(self) \
#            and querystore.value == self.value
#
#    def results(self):
#        return iter(self.value)


#class ModelQueryStore (models.Model):
#    model = SerializedObjectField()
#    query = SerializedObjectField()
#
#    def is_the_same_as(self, querystore):
#        return type(querystore) is type(self) \
#            and querystore.query == self.query \
#            and querystore.model == self.model
#
#    def results(self):
#        print self.model
#        qs = self.model.objects.all()
#        qs.query = self.query
#        return qs


#class SearchQueryStore (models.Model):
#    query = SerializedObjectField()
#
#    def is_the_same_as(self, querystore):
#        return type(querystore) == type(self) \
#            and querystore.query == self.query
#
#    def results(self):
#        qs = haystack.SearchQuerySet().all()
#        qs.query = self.query
#        return qs


class ContentFeed (models.Model):
    """
    Stores information necessary for retrieving a queryset of content.

    The query for the ``ContentFeed`` is stored as a pickled iterable object.
    Don't judge me!!! Calling ``get_content`` on a ``ContentFeed`` will return
    you the results of the query. Calling ``get_last_updated`` will return you
    the last time the given set of content was updated.

    To create a ``ContentFeed`` object, use the ``factory`` method. This will
    take your parameters and pickle them for you, returning a valid
    ``ContentFeed`` object. you must specify a last_updated_calc callable,
    because each set of content may have a different way of determining when it
    was last updated.

    """

    data = SerializedObjectField()
    """An object that contains the queryset and the last_updated function"""

    last_updated = models.DateTimeField(
        default=datetime.datetime(1970, 1, 1, 0, 0, 0))
    """The stored value of the last time content in the feed was updated."""


    def __unicode__(self):
        return u'a %s feed' % (self.data,)

    def get_content(self):
        """Returns the results of the stored query's ``run`` method."""
        queryset = self.data.queryset
        return queryset

    def get_last_updated(self, item):
        """Returns the time that the given item was last updated."""
        last_updated = self.data.calc_last_updated(item)
        return last_updated

    @classmethod
    def factory(cls, data):
        feed = cls()
        feed.data = data
        return feed


# Subscriber

class Subscriber (auth.User):

    # subscriptions (backref)
    """The set of subscriptions for this user"""

    def subscribe(self, feed, commit=True):
        """Subscribe the user to a content feed."""
        subscription = Subscription(subscriber=self, feed=feed)
        if commit:
            subscription.save()
        return subscription

    def subscription(self, content_feed):
        """Returns the subscription to the given content feed."""
        try:
            sub = self.subscriptions.get(feed__data=content_feed.data)
            return sub
        except Subscription.DoesNotExist:
            return None

    def is_subscribed(self, content_feed):
        """Returns the set of subscriptions that have the same data as the given
           content feed.  If there are none, this evaluates to False."""
        return (self.subscription(content_feed) is not None)


from django.dispatch import receiver
from django.db.models.signals import post_save
@receiver(post_save, sender=auth.User)
def create_subscriber_for_user(sender, **kwargs):
    user = kwargs.get('instance')
    created = kwargs.get('created')
    raw = kwargs.get('raw')

    logging.debug('user is %r' % user)

    if created and not raw:
        if not hasattr(user, 'subscriber') or user.subscriber is None:
            user.subscriber = Subscriber()
            user.subscriber.save()
            logging.debug('created subscriber')


class Subscription (models.Model):
    subscriber = models.ForeignKey('Subscriber', related_name='subscriptions')
    feed = models.ForeignKey('ContentFeed')
    last_sent = models.DateTimeField()

    def __unicode__(self):
        return u"%s's subscription to %s" % (self.subscriber, self.feed)

    def save(self, *args, **kwargs):
        """
        Sets the last_sent datetime to the current time when instance is new.
        Doesn't change the last_sent datetime on instance if it's already
        saved.

        """
        # We could use Django's built-in ability to make this an auto_now_add
        # field, but then we couldn't change the value when we want.
        if not self.id:
            self.last_sent = datetime.datetime.now()
        super(Subscription, self).save(*args, **kwargs)


class DistributionChannel (models.Model):
    recipient = models.ForeignKey(auth.User, null=True)

    class Meta:
        abstract = True

class EmailChannel (DistributionChannel):
    email = models.CharField(max_length=256)

    def __unicode__(self):
        return "Email to %s" % self.email

class RssChannel (DistributionChannel):
    pass

class SmsChannel (DistributionChannel):
    number = models.CharField(max_length=32)
    carrier = models.CharField(max_length=32)

    def __unitcode__(self):
        return "Send SMS to %s number %s" % (self.carrier, self.number)

class SearchSubscription (Subscription):
    query = models.TextField()

    def __unicode__(self):
        return self.query
