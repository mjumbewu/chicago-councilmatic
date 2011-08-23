import datetime
import pickle
from django.db import models

import django.contrib.auth.models as auth
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import haystack.query as haystack

# Fields

class SerializedObjectField(models.TextField):
    description = "SerializedObject"

    def get_internal_type(self):
        return "TextField"

    def get_prep_value(self, value):
        return pickle.dumps(value)

    def to_python(self, value):
        return pickle.loads(value)

#
# This little bit of magic is here because I tried to migrate with a 
# SerializedObjectField, and got an error that directed me to
# http://south.aeracode.org/wiki/MyFieldsDontWork
#
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^subscriptions\.models\.SerializedObjectField"])


# Content Feeds

class ListQueryStore (models.Model):
    value = SerializedObjectField()
    
    def results(self):
        return iter(self.value)


class ModelQueryStore (models.Model):
    model = SerializedObjectField()
    query = SerializedObjectField()
    
    def results(self):
        qs = self.model.objects.all()
        qs.query = self.query
        return qs


class SearchQueryStore (models.Model):
    query = SerializedObjectField()
    
    def results(self):
        qs = haystack.SearchQuerySet().all()
        qs.query = self.query
        return qs


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
    QUERYTYPE_CHOICES = (('list','model'),
                         ('model','model'),
                         ('search','search'))
    
    querystore_type = models.ForeignKey('contenttypes.ContentType')
    querystore_id = models.PositiveIntegerField()
    querystore = generic.GenericForeignKey('querystore_type', 'querystore_id')
    
    last_updated_calc = SerializedObjectField()
    last_updated = models.DateTimeField(
        default=datetime.datetime(1970, 1, 1, 0, 0, 0))
    
    def get_content(self):
        """Returns the results of the stored query's ``run`` method."""
        queryset = self.querystore.results()
        return queryset
    
    def get_last_updated(self, item):
        """Returns the time that the given item was last updated."""
        last_updated = self.last_updated_calc(item)
        return last_updated
    
    @classmethod
    def factory(cls, queryset, last_updated_calc):
        """Creates a ContentFeed object with a pickled version of the queryset
           and a pickled version of the last_updated_calc. Note that both
           objects must be picklable."""
        feed = cls()
        
        if isinstance(queryset, list):
            feed.querystore = ListQueryStore(value=queryset)
        elif hasattr(queryset, 'model') and hasattr(queryset, 'query'):
            feed.querystore = ModelQueryStore(model=queryset.model,
                                              query=queryset.query)
        elif isinstance(queryset, haystack.SearchQuerySet):
            feed.querystore = SearchQueryStore(query=queryset.query)
        else:
            raise ValueError('Invalid value for queryset: %r' % (queryset,))
        
        feed.last_updated_calc = last_updated_calc
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

