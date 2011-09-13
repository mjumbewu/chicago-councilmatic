import logging as log

from django.views import generic as views
from django import http
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

import subscriptions.forms as forms
import subscriptions.models as models

class SingleSubscriptionMixin (object):
    feed_data = None
    """A factory for the feed_data object that describes this content feed"""

    def get_content_feed(self, *args, **kwargs):
        feed_data = self.feed_data(*args, **kwargs)
        return models.ContentFeed.factory(feed_data)

    def get_subscription(self, feed):
        if self.request.user and self.request.user.is_authenticated():
            try:
                subscriber = self.request.user.subscriber

            # If the user doesn't have a subscriber attribute, then they must
            # not be subscribed.
            except models.Subscriber.DoesNotExist:
                return None

            return subscriber.subscription(feed)

        return None

    def get_subscription_form(self, feed):
        if self.request.user and self.request.user.is_authenticated():
            try:
                subscriber = self.request.user.subscriber

            except models.Subscriber.DoesNotExist:
                return None

            if not self.request.user.subscriber.is_subscribed(feed):
                form = forms.SubscriptionForm({'feed': feed,
                                               'subscriber': subscriber})
                return form

        return None

    def get_context_data(self, **kwargs):
        context_data = super(SingleSubscriptionMixin, self).get_context_data(**kwargs)

        feed = self.get_content_feed()
        subscription = self.get_subscription(feed)
        subscription_form = self.get_subscription_form(feed)
        is_subscribed = (subscription is not None)

        context_data.update({'feed': feed,
                             'subscription': subscription,
                             'subscription_form': subscription_form,
                             'is_subscribed': is_subscribed})
        return context_data


class CreateSubscriptionView (views.CreateView):
    model = models.Subscription

    def get_success_url(self):
        return self.request.REQUEST['success']


class DeleteSubscriptionView (views.DeleteView):
    model = models.Subscription

    def get_success_url(self):
        return self.request.REQUEST['success']


class SubscribeToSearchView (views.CreateView):
    model = models.SearchSubscription
    template_name = "subscriptions/searchsubscription_edit.html"


def subscribe(request):
    subscriber = request.user.subscriber
    feed = ContentFeed.object.get(request.REQUEST['feed'])
    redirect_to = request.REQUEST['next']

    subscriber.subscribe(feed)
    return HttpResponseRedirect(redirect_to)


#    def get_subscription_form(self):
#        pass
#
#    def __call__(self, request):
#        if request.method == 'POST':
#
#            subs_form = self.get_subscription_form()
#        else:
#            return super(SubscribeToSearchView, self).__call__(request)
