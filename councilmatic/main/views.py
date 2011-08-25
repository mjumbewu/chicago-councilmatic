# Create your views here.
from django.views import generic as view

from main import feeds
import phillyleg.models
import subscriptions.forms
import subscriptions.models


class SearchBarMixin (object):
    def get_searchbar_form(self):
        return subscriptions.forms.SimpleSearchForm()
    
    def get_context_data(self, **kwargs):
        context_data = super(SearchBarMixin, self).get_context_data(**kwargs)
        context_data.update({'searchbar_form': self.get_searchbar_form()})
        return context_data


class ContentFeedMixin (object):
    def get_content_feed(self, *args, **kwargs):
        feed_data = self.feed_data(*args, **kwargs)
        return subscriptions.models.ContentFeed.factory(feed_data)
    
    def get_is_subscribed(self, feed):
        if self.request.user:
            try:
                subscriber = self.request.user.subscriber
            except AttributeError:
                return False
            except subscriptions.models.Subscriber.DoesNotExist:
                return False
            
            for subscription in subscriber.subscriptions.all():
                print feed.data, subscription.feed.data
                if type(feed.data) == type(subscription.feed.data):
                    return True
        
        return False
    
    def get_context_data(self, **kwargs):
        context_data = super(ContentFeedMixin, self).get_context_data(**kwargs)
        
        feed = self.get_content_feed()
        is_subscribed = self.get_is_subscribed(feed)
        
        context_data.update({'feed': feed,
                             'is_subscribed': is_subscribed})
        return context_data


class AppDashboardView (SearchBarMixin, view.TemplateView):
    template_name = 'main/app_dashboard.html'
    
    def get_context_data(self, **kwargs):
        search_form = subscriptions.forms.FullSearchForm()
        
        legfiles = phillyleg.models.LegFile.objects.all()[:8]
        
        context_data = super(AppDashboardView, self).get_context_data(
            **kwargs)
        context_data.update({'legfiles': legfiles, 'search_form': search_form})
                       
        return context_data


class LegislationListView (SearchBarMixin, ContentFeedMixin, view.ListView):
    model = phillyleg.models.LegFile
    template_name = 'phillyleg/legfile_list.html'
    paginate_by = 20
    feed_data = feeds.NewLegislationFeed
    

class LegislationDetailView (SearchBarMixin, view.DetailView):
    model = phillyleg.models.LegFile
    template_name = 'phillyleg/legfile_detail.html'
