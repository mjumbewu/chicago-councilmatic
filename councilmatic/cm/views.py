import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views import generic as views
from cm_api.resources import SubscriberResource
from phillyleg import models

class ProfileAdminView (views.TemplateView):
    template_name = 'cm/profile_admin.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileAdminView, self).get_context_data(**kwargs)

        subscriber = self.request.user.subscriber
        context['subscriber'] = subscriber

        subscriber_data = SubscriberResource().serialize(subscriber)
        context['subscriber_data'] = json.dumps(
            subscriber_data, cls=DjangoJSONEncoder)

        return context
