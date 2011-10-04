from django.test.client import Client
from nose.tools import *
from mock import *

class Tests_legislation_index_GET:

    @istest
    def has_new_legislation_list_feed_in_context(self):
        from main.feeds import NewLegislationFeed

        # Make the request.
        client = Client()
        response = client.get('/legislation/')

        # Check that the context feed is the same as the stock feed.
        assert_equal(type(response.context['feed']), NewLegislationFeed)

    @istest
    def sorts_legislation_by_date_introduced(self):

        from phillyleg.models import LegFile
        from datetime import date

        LegFile(key=1, intro_date=date(2011,8,23)).save()
        LegFile(key=2, intro_date=date(2011,8,21)).save()
        LegFile(key=3, intro_date=date(2011,8,24)).save()
        LegFile(key=4, intro_date=date(2011,8,21)).save()

        # Make the request.
        client = Client()
        response = client.get('/legislation/')

        # Check that the context feed is the same as the stock feed.
        intro_dates = [obj.intro_date for obj in response.context['object_list']]
        assert_equal(intro_dates, [date(2011,8,24),
                                   date(2011,8,23),
                                   date(2011,8,21),
                                   date(2011,8,21)])

    @istest
    def has_isSubscribed_set_to_true_when_current_user_is_subscribed(self):
        from django.contrib.auth.models import User
        from subscriptions.models import Subscriber, Subscription
        from subscriptions.feeds import ContentFeedLibrary
        from main.feeds import NewLegislationFeed

        subscriber = Subscriber(username="hello")
        subscriber.set_password("world")
        subscriber.save()

        library = ContentFeedLibrary()
        library.register(NewLegislationFeed, 'blah blah')

        feed = NewLegislationFeed()
        subscription = subscriber.subscribe(feed)
        subscriber.save()

        # Make the request.
        client = Client()
        assert client.login(username="hello", password="world")
        response = client.get('/legislation/')

        # Check the context
        assert response.context['is_subscribed']
        assert_equal(response.context['subscription'], subscription)
