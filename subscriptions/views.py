import django.views.generic
import haystack.views
import subscriptions.forms as forms
from django import http

class SearchView (haystack.views.SearchView):
    def __init__(self, *args, **kwds):
        super(SearchView, self).__init__(form_class=forms.FullSearchForm, *args, **kwds)
    
    def extra_context(self):
        return { 'subs_form': forms.SearchSubscriptionForm() }

class SubscribeToSearchView (django.views.generic.View):
    def post(self, request):
        return http.HttpResponse(str(request));

