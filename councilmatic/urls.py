from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic import ListView, DetailView, TemplateView
import phillyleg.models

import main.views
import phillyleg.views
import subscriptions.views
import bookmarks.views
import haystack.views

urlpatterns = patterns('',
    # Example:
    #(r'^philly_legislative/', include('philly_legislative.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login', name='registration_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='registration_logout'),
#    url(r'', include('social_auth.urls')),
    url(r'', include('registration.backends.default.urls')),

    url(r'^subscribe/$', subscriptions.views.CreateSubscriptionView.as_view(), name='subscribe'),
    url(r'^unsubscribe/(?P<pk>\d+)/$', subscriptions.views.DeleteSubscriptionView.as_view(), name='unsubscribe'),

    url(r'^bookmark/$', bookmarks.views.CreateBookmarkView.as_view(), name='bookmark'),
    url(r'^unbookmark/(?P<pk>\d+)/$', bookmarks.views.DeleteBookmarkView.as_view(), name='unbookmark'),

    url(r'^$',
        main.views.AppDashboardView.as_view(),
        name='main_dashboard'),

    url(r'^legislation/$',
        main.views.LegislationListView.as_view(),
        name='legislation_list'),
    url(r'^legislation/(?P<pk>\d+)$',
        main.views.LegislationDetailView.as_view(),
        name='legislation_detail'),
   url(r'^legislation/(?P<pk>\d+)/add_bookmark$',
        phillyleg.views.add_bookmark,
        name='add_bookmark'),

    url(r'^minutes/$', ListView.as_view(
        model=phillyleg.models.LegMinutes,
        template_name='phillyleg/legminutes_list.html'),
        name='minutes_list'),
    url(r'^minutes/(?P<pk>\d+)$', DetailView.as_view(
        model=phillyleg.models.LegMinutes,
        template_name='phillyleg/legminutes_detail.html'),
        name='minutes_detail'),

    url(r'^search/$', main.views.SearchView.as_view(),
        name='search'),

    url(r'^(?P<user_pk>\d+)/subscriptions/$', TemplateView.as_view(template_name='base.html'), name='user_subscriptions'),
    url(r'^(?P<user_pk>\d+)/subscriptions/(?P<bookmark_pk>\d+)/$', TemplateView.as_view(template_name='base.html'), name='user_subscription'),

#    url(r'^subscribe$', subscriptions.views.SubscribeToSearchView.as_view()),
#    url(r'^(?P<subscription_id>\d+)/$', 'phillyleg.views.dashboard'),
#    url(r'^search/', include('haystack.urls')),

    # Older views.  Work with them.
    url(r'^subs/$', 'phillyleg.views.subscribe'),
    url(r'^subs/create/$', 'phillyleg.views.create'),
    url(r'^subs/unsubscribe/$', 'phillyleg.views.unsubscribe'),
    #url(r'^subs/(?P<subscription_id>\d+)/$', 'phillyleg.views.edit'),
    url(r'^subs/delete/$', 'phillyleg.views.delete'),
)
