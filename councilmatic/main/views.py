# Create your views here.
from django.views import generic as view

import phillyleg.models
import subscriptions.forms

class SearchBarMixin (object):
    def get_searchbar_form(self):
        return subscriptions.forms.SimpleSearchForm()
    
    
    def get_context_data(self, **kwargs):
        context_data = super(SearchBarMixin, self).get_context_data(
            **kwargs)
        context_data.update({'searchbar_form': self.get_searchbar_form()})
        
        return context_data


class AppDashboardView (SearchBarMixin, view.TemplateView):
    template_name = 'main/app_dashboard.html'
    
    def get_context_data(self, **kwargs):
        legfiles = phillyleg.models.LegFile.objects.all()[:8]
        
        context_data = super(AppDashboardView, self).get_context_data(
            **kwargs)
        context_data.update({'legfiles': legfiles})
                       
        return context_data


class LegislationListView (SearchBarMixin, view.ListView):
    model = phillyleg.models.LegFile
    template_name = 'phillyleg/legfile_list.html'
    paginate_by = 20
    

class LegislationDetailView (SearchBarMixin, view.DetailView):
    model = phillyleg.models.LegFile
    template_name = 'phillyleg/legfile_detail.html'
