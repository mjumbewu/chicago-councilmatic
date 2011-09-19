import logging as log
from django.views import generic as view

from main import feeds
from main import forms

import haystack.views
import bookmarks.views
import opinions.views
import phillyleg.models
import subscriptions.forms
import subscriptions.models
import subscriptions.views


class SearchBarMixin (object):
    def get_searchbar_form(self):
        return forms.SimpleSearchForm()

    def get_context_data(self, **kwargs):
        context_data = super(SearchBarMixin, self).get_context_data(**kwargs)
        context_data.update({'searchbar_form': self.get_searchbar_form()})
        return context_data


class AppDashboardView (SearchBarMixin, view.TemplateView):
    template_name = 'main/app_dashboard.html'

    def get_context_data(self, **kwargs):
        search_form = forms.FullSearchForm()

        legfiles = phillyleg.models.LegFile.objects.all()[:8]

        context_data = super(AppDashboardView, self).get_context_data(
            **kwargs)
        context_data.update({'legfiles': legfiles, 'search_form': search_form})

        return context_data


class SearchView (SearchBarMixin,
                  subscriptions.views.SingleSubscriptionMixin,
                  view.ListView):
    template_name = 'search/search.html'
    paginate_by = 20
    feed_data = None

    def dispatch(self, request, *args, **kwargs):
        # Construct and run a haystack SearchView so that we can use the
        # resulting values.
        self.search_view = haystack.views.SearchView(form_class=forms.SimpleSearchForm)
        self.search_view.request = request

        self.search_view.form = self.search_view.build_form()
        self.search_view.query = self.search_view.get_query()
        self.search_view.results = self.search_view.get_results()

        # The, continue with the dispatch
        return super(SearchView, self).dispatch(request, *args, **kwargs)

    def on_queryset_gotten(self, queryset):
        # Construct the feed data
        if self.feed_data is None:
            self.feed_data = lambda: feeds.SearchResultsFeed(self.search_view.results.query.query_filter)

    def get_queryset(self):
        queryset = self.search_view.results
        self.on_queryset_gotten(queryset)
        return [result.object for result in queryset]

    def get_context_data(self, **kwargs):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        context = super(SearchView, self).get_context_data(**kwargs)
        context['form'] = self.search_view.form
        log.debug(context)
        return context


class LegislationListView (SearchBarMixin,
                           subscriptions.views.SingleSubscriptionMixin,
                           view.ListView):
    model = phillyleg.models.LegFile
    template_name = 'phillyleg/legfile_list.html'
    paginate_by = 20
    feed_data = feeds.NewLegislationFeed

    def get_queryset(self):
        queryset = super(LegislationListView, self).get_queryset()
        return queryset.order_by('-intro_date')


class LegislationDetailView (SearchBarMixin,
                             subscriptions.views.SingleSubscriptionMixin,
                             bookmarks.views.SingleBookmarkedObjectMixin,
                             opinions.views.SingleOpinionTargetMixin,
                             view.DetailView):
    model = phillyleg.models.LegFile
    template_name = 'phillyleg/legfile_detail.html'
    feed_data = None

    def on_object_gotten(self, legfile):
        # Construct the feed_data factory
        if not self.feed_data:
            self.feed_data = lambda: feeds.LegislationUpdatesFeed(pk=legfile.pk)

    def get_object(self):
        legfile = super(LegislationDetailView, self).get_object()

        # Intercept the object
        self.on_object_gotten(legfile)

        return legfile


class BookmarkListView (SearchBarMixin,
                        view.ListView):
    template_name = 'main/bookmark_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated():
            return [bm.content for bm in user.bookmarks.all()]
        else:
            return []
