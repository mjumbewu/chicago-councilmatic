import json
import logging as log
from django.contrib.syndication.views import Feed as DjangoFeed
from django.shortcuts import get_object_or_404
from django.views import generic as views
from haystack.query import SearchQuerySet

from cm_api.resources import SubscriberResource
from main import feeds
from main import forms

import haystack.views
import bookmarks.views
import opinions.views
import phillyleg.models
import subscriptions.forms
import subscriptions.models
import subscriptions.views


class NewLegislationFeed (DjangoFeed):
    title = u'New Legislation'
    link = 'http://localhost:8000'
    description = u'Newly introduced legislation'
    max_items = 100

    def items(self):
        return phillyleg.models.LegFile.objects.all()[:self.max_items]

    def item_title(self, legfile):
        return u'{0.type} {0.id}'.format(legfile)

    def item_pubdate(self, legfile):
        import datetime
        d = legfile.intro_date
        current = datetime.datetime(d.year, d.month, d.day)
        return current


class CustomContentFeedView (DjangoFeed):
    def get_object(self, request, subscription_id):
        return get_object_or_404(subscription.models.Subscription,
                                 pk=subscription_id)

    def title(self, sub):
        return unicode(sub)

    def link(self, sub):
#        return sub.get_absolute_url()
        return u'http://localhost:8000/'

    def description(self, sub):
        return unicode(sub)


class SearchBarMixin (object):
    def get_searchbar_form(self):
        return forms.SimpleSearchForm()

    def get_context_data(self, **kwargs):
        context_data = super(SearchBarMixin, self).get_context_data(**kwargs)
        context_data.update({'searchbar_form': self.get_searchbar_form()})
        return context_data


class AppDashboardView (SearchBarMixin,
                        bookmarks.views.BaseBookmarkMixin,
                        views.TemplateView):
    template_name = 'main/app_dashboard.html'

    def get_recent_locations(self):
        return list(phillyleg.models.MetaData_Location.objects.\
                       all().order_by('-pk')[:10])

    def get_recent_legislation(self):
        return list(phillyleg.models.LegFile.objects.\
                        all().order_by('-key')[:3])

    def get_context_data(self, **kwargs):
        search_form = forms.FullSearchForm()

        legfiles = self.get_recent_legislation()
        bookmark_data = self.get_bookmarks_data(legfiles)
        locations = self.get_recent_locations()

        context_data = super(AppDashboardView, self).get_context_data(
            **kwargs)
        context_data.update({
            'legfiles': legfiles,
            'bookmark_data': bookmark_data,
            'search_form': search_form,
            'locations': locations
        })

        return context_data


class SearcherMixin (object):
    def _init_haystack_searchview(self, request):
        # Construct and run a haystack SearchView so that we can use the
        # resulting values.
        self.search_view = haystack.views.SearchView(form_class=forms.FullSearchForm, searchqueryset=SearchQuerySet().order_by('-order_date'))
        self.search_view.request = request

        self.search_view.form = self.search_view.build_form()
        self.search_view.query = self.search_view.get_query()
        self.search_view.results = self.search_view.get_results()

    def _get_search_results(self, query_params):
        if len(query_params) == 0:
            search_queryset = phillyleg.models.LegFile.objects.all().order_by('-key')

        else:
            class SQSProxy (object):
                """
                Make a SearchQuerySet look enough like a QuerySet for a ListView
                not to notice the difference.
                """
                def __init__(self, sqs):
                    self.sqs = sqs
                def __len__(self):
                    return len(self.sqs)
                def __iter__(self):
                    return (result.object for result in self.sqs)
                def __getitem__(self, key):
                    if isinstance(key, slice):
                        return [result.object for result in self.sqs[key] if result is not None]
                    else:
                        return self.sqs[key].object

            search_queryset = SQSProxy(self.search_view.results)
        return search_queryset


class LegFileListFeedView (SearcherMixin, DjangoFeed):
    def get_object(self, request, *args, **kwargs):
        self._init_haystack_searchview(request)
        query_params = request.GET.copy()
        search_queryset = self._get_search_results(query_params)
        return search_queryset

    def items(self, obj):
        return obj[:100]

    def title(self, obj):
        'testing'

    def link(self):
        return 'http://www.google.com/'


class SearchView (SearcherMixin,
                  SearchBarMixin,
                  subscriptions.views.SingleSubscriptionMixin,
                  views.ListView):
    template_name = 'search/search.html'
    paginate_by = 20
    feed_data = None

    def dispatch(self, request, *args, **kwargs):
        self._init_haystack_searchview(request)
        return super(SearchView, self).dispatch(request, *args, **kwargs)

    def get_content_feed(self):
        search_params = self.request.GET
        return feeds.SearchResultsFeed(**search_params)

    def get_queryset(self):
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        search_queryset = self._get_search_results(query_params)
        return search_queryset

    def get_context_data(self, **kwargs):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        context = super(SearchView, self).get_context_data(**kwargs)
        context['form'] = self.search_view.form

        page_obj = context.get('page_obj', None)
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']

        if page_obj and page_obj.has_next():
            context['next_url'] = (
                self.request.path + '?' +
                'page={0}'.format(page_obj.next_page_number())
            )
            if query_params:
                context['next_url'] += '&' + query_params.urlencode()

        if page_obj and page_obj.has_previous():
            context['previous_url'] = (
                self.request.path + '?' +
                'page={0}'.format(page_obj.previous_page_number())
            )
            if query_params:
                context['previous_url'] += '&' + query_params.urlencode()

        log.debug(context)
        return context


class LegislationStatsMixin (object):
    def get_queryset(self):
        queryset = super(LegislationStatsMixin, self).get_queryset()

        now = datetime.date.today()
        four_weeks = datetime.timedelta(days=28)
        queryset = queryset.filter(intro_date__gte=now-four_weeks)
        return queryset


class LegislationListView (SearchBarMixin,
                           subscriptions.views.SingleSubscriptionMixin,
                           bookmarks.views.MultipleBookmarkedObjectsMixin,
                           views.ListView):
    model = phillyleg.models.LegFile
    template_name = 'phillyleg/legfile_list.html'
    paginate_by = 10

    def get_content_feed(self):
        return feeds.NewLegislationFeed()

    def get_queryset(self):
        queryset = super(LegislationListView, self).get_queryset()
        return queryset.order_by('-intro_date', '-key')


class LegislationDetailView (SearchBarMixin,
                             subscriptions.views.SingleSubscriptionMixin,
                             bookmarks.views.SingleBookmarkedObjectMixin,
                             opinions.views.SingleOpinionTargetMixin,
                             views.DetailView):
    model = phillyleg.models.LegFile
    template_name = 'phillyleg/legfile_detail.html'

    def get_content_feed(self):
        legfile = self.object
        return feeds.LegislationUpdatesFeed(pk=legfile.pk)

#    def on_object_gotten(self, legfile):
#        # Construct the feed_data factory
#        if not self.feed_data:
#            self.feed_data = lambda: feeds.LegislationUpdatesFeed(pk=legfile.pk)

#    def get_object(self):
#        legfile = super(LegislationDetailView, self).get_object()

#        # Intercept the object
#        self.on_object_gotten(legfile)

#        return legfile


class BookmarkListView (SearchBarMixin,
                        views.ListView):
    template_name = 'main/bookmark_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated():
            return [bm.content for bm in user.bookmarks.all()]
        else:
            return []


class SubscriptionManagementView (SearchBarMixin,
                                  views.TemplateView):
    template_name = 'cm/profile_admin.html'

    def get_context_data(self, **kwargs):
        context = super(SubscriptionManagementView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated() and self.request.user.subscriber:
            subscriber_data = SubscriberResource().serialize(self.request.user.subscriber)
            subscriber_data['logged_in'] = True
            context['subscriber_data'] = json.dumps(subscriber_data)

        return context
