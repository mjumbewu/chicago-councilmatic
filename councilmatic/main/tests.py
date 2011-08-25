from django.test.client import Client
from nose.tools import *

class Test_legislation_index_GET:
    
    @istest
    def has_new_legislation_list_feed_in_context(self):
        from subscriptions.models import ContentFeed
        from main.feeds import NewLegislationFeed
        
        # Make the request.
        client = Client()
        response = client.get('/legislation/')
        
        # Check that the context feed is the same as the stock feed.
        assert_equal(type(response.context['feed'].data), NewLegislationFeed)

    @istest
    def has_isSubscribed_set_to_true_when_current_user_is_subscribed(self):
        from django.contrib.auth.models import User
        from subscriptions.models import ContentFeed, Subscriber, Subscription
        from main.feeds import NewLegislationFeed
        
        subscriber = Subscriber(username="hello")
        subscriber.set_password("world")
        subscriber.save()
        
        feed = ContentFeed.factory(data=NewLegislationFeed())
        feed.save()
        
        subscriber.subscribe(feed)
        subscriber.save()
        
        # Make the request.
        client = Client()
        assert client.login(username="hello", password="world")
        response = client.get('/legislation/')
        
        # Check the context
        assert response.context['is_subscribed']

