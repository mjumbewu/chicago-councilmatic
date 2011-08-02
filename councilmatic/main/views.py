# Create your views here.
from django.views import generic as view

import phillyleg.models
import subscriptions.forms

class AppDashboardView (view.TemplateView):

    template_name = 'main/app_dashboard.html'
    
    def get_context_data(self, **kwargs):
        legfiles = phillyleg.models.LegFile.objects.all().order_by('-key')[:8]
        searchform = subscriptions.forms.SimpleSearchForm()
        
        context_data = super(AppDashboardView, self).get_context_data(
            **kwargs)
        context_data.update({'legfiles': legfiles, 
                             'searchform': searchform,
                             'simple_search_form': searchform})
                       
        return context_data
            
