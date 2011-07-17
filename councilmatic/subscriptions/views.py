from django.views import generic as views
from django import http
from haystack import views as haystack_views
from django.shortcuts import render_to_response


import subscriptions.forms as forms
import subscriptions.models as models

class SearchView (haystack_views.SearchView):
    def __init__(self, *args, **kwds):
        super(SearchView, self).__init__(form_class=forms.SimpleSearchForm, *args, **kwds)
    
    def get_embedded_subscribe_form(self):
        return forms.SearchSubscriptionForm()
    
    def extra_context(self):
        return { 'subs_form': self.get_embedded_subscribe_form() }
    
    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        (paginator, page) = self.build_page()
        
        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'object_list': [result.object for result in page.object_list],
            'paginator': paginator,
            'suggestion': None,
        }
        
        context.update(self.extra_context())
        return render_to_response(self.template, context, context_instance=self.context_class(self.request))
    

class SubscribeToSearchView (views.CreateView):
    model = models.SearchSubscription
    template_name = "subscriptions/searchsubscription_edit.html"
    
#    def get_subscription_form(self):
#        pass
#    
#    def __call__(self, request):
#        if request.method == 'POST':
#            
#            subs_form = self.get_subscription_form()
#        else:
#            return super(SubscribeToSearchView, self).__call__(request)
