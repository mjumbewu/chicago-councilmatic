import logging as log
from django.views import generic as view

from main import feeds
import bookmarks.views
import phillyleg.models
import subscriptions.forms
import subscriptions.models
import subscriptions.views


class SearchBarMixin (object):
    def get_searchbar_form(self):
        return subscriptions.forms.SimpleSearchForm()

    def get_context_data(self, **kwargs):
        context_data = super(SearchBarMixin, self).get_context_data(**kwargs)
        context_data.update({'searchbar_form': self.get_searchbar_form()})
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


class LegislationListView (SearchBarMixin, subscriptions.views.SingleSubscriptionMixin, view.ListView):
    model = phillyleg.models.LegFile
    template_name = 'phillyleg/legfile_list.html'
    paginate_by = 20
    feed_data = feeds.NewLegislationFeed

    def get_queryset(self):
        queryset = super(LegislationListView, self).get_queryset()
        return queryset.order_by('-intro_date')


class LegislationDetailView (SearchBarMixin, subscriptions.views.SingleSubscriptionMixin, bookmarks.views.SingleBookmarkedObjectMixin, view.DetailView):
    model = phillyleg.models.LegFile
    template_name = 'phillyleg/legfile_detail.html'
    feed_data = None

    def on_object_gotten(self, legfile):
        # Construct the feed_data factory
#        raise Exception(dir(logging))
        log.debug('Construct the feed data factory for %r' % legfile)
        if not self.feed_data:
            self.feed_data = lambda: feeds.LegislationUpdatesFeed(pk=legfile.pk)

    def get_object(self):
        legfile = super(LegislationDetailView, self).get_object()

        # Intercept the object
        self.on_object_gotten(legfile)

        return legfile
