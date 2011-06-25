from django.views import generic as views
from django import http
from haystack import views as haystack_views

import subscriptions.forms as forms
import subscriptions.models as models

class SearchView (haystack_views.SearchView):
    def __init__(self, *args, **kwds):
        super(SearchView, self).__init__(form_class=forms.SimpleSearchForm, *args, **kwds)
    
    def get_embedded_subscribe_form(self):
        return forms.SearchSubscriptionForm()
    
    def extra_context(self):
        return { 'subs_form': self.get_embedded_subscribe_form() }


class SubscribeToSearchView (SearchView, views.ProcessFormView):
    def get_subscription_form(self):
    
    def __call__(self, request);
        if request.method == 'POST':
            
            subs_form = self.get_subscription_form()
        else:
            return super(SubscribeToSearchView, self).__call__(request)
