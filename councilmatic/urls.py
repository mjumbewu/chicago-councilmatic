from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic import ListView, DetailView
import phillyleg.models

import main.views
import phillyleg.views
import subscriptions.views
import haystack.views

urlpatterns = patterns('',
    # Example:
    #(r'^philly_legislative/', include('philly_legislative.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
    
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

    url(r'^minutes/(?P<pk>\d+)$', DetailView.as_view(
        model=phillyleg.models.LegMinutes,
        template_name='phillyleg/legminutes_detail.html'),
        name='minutes_detail'),
    
    url(r'^search/$', subscriptions.views.SearchView(),
        name='legfile_search'),
    url(r'^subscribe$', subscriptions.views.SubscribeToSearchView.as_view()),
    url(r'^(?P<subscription_id>\d+)/$', 'phillyleg.views.dashboard'),
#    url(r'^search/', include('haystack.urls')),
    
    # Older views.  Work with them.
    url(r'^subs/$', 'phillyleg.views.subscribe'),
    url(r'^subs/create/$', 'phillyleg.views.create'),
    url(r'^subs/unsubscribe/$', 'phillyleg.views.unsubscribe'),
    #url(r'^subs/(?P<subscription_id>\d+)/$', 'phillyleg.views.edit'),
    url(r'^subs/delete/$', 'phillyleg.views.delete'),
)
