import datetime
import pickle
from django.db import models

import django.contrib.auth.models as auth
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Content Feeds

class ContentFeed (models.Model):
    """
    Stores information necessary for retrieving a queryset of content.
    
    The query for the ``ContentFeed`` is stored as a line of python code that
    will actually construct the query. Don't judge me!!! Calling ``get_content``
    on a ``ContentFeed`` will return you the results of the query.
    
    """
    queryset = models.TextField()
    last_updated_calc = models.TextField()
    last_updated = models.DateTimeField(
        default=datetime.datetime(1970, 1, 1, 0, 0, 0))
    
    def get_content(self):
        """Returns the results of the stored query's ``run`` method."""
        queryset = pickle.loads(self.queryset)
        return queryset
    
    def get_last_updated(self, queryset):
        """Returns the time that the most recently updated item in the queryset
           was updated."""
        last_updated_calc = pickle.loads(self.last_updated_calc)
        last_updated = last_updated_calc(queryset)
        return last_updated
    
    @classmethod
    def factory(cls, queryset, last_updated_calc):
        """Creates a ContentFeed object with a pickled version of the queryset
           and a pickled version of the last_updated_calc. Note that both
           objects must be picklable."""
        feed = cls()
        feed.queryset = pickle.dumps(queryset)
        feed.last_updated_calc = pickle.dumps(last_updated_calc)
        return feed

    
# Subscriber

class Subscriber (auth.User):
    def subscribe(self, feed, commit=True):
        """Subscribe the user to a content feed."""
        subscription = Subscription(subscriber=self, feed=feed)
        if commit:
            subscription.save()
        return subscription


class Subscription (models.Model):
    subscriber = models.ForeignKey('Subscriber', related_name='subscriptions')
    feed = models.ForeignKey('ContentFeed')
    last_sent = models.DateTimeField()
    
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

