from django.conf.urls.defaults import *
from . import views

urlpatterns = patterns(
    'cm',

    url(r'^profile$', views.ProfileAdminView.as_view(),
        name='cm_profile_admin'),
)
