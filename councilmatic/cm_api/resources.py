import json

from django.core.urlresolvers import reverse
from djangorestframework import resources
from .forms import SubscriberForm

from subscriptions.models import (Subscriber, Subscription)
from bookmarks.models import Bookmark
from phillyleg.models import (CouncilDistrict, CouncilDistrictPlan,
                              CouncilMember, LegFile)

import logging
log = logging.getLogger(__name__)

class SubscriberResource (resources.ModelResource):
    model = Subscriber
    form = SubscriberForm
    exclude = ['user_ptr', 'password']
    include = ['url', 'subscriptions', 'bookmarks']

    def serialize(self, obj):
        if isinstance(obj, Subscriber):
            return {
                'username': obj.username,
                'email': obj.email,
                'subscriptions': [self.serialize(subscription) for
                                  subscription in obj.subscriptions.all()],
                'bookmarks': [self.serialize(bookmark) for
                              bookmark in obj.bookmarks.all()],
                'id': obj.id,
                'url': self.url(obj),
            }

        elif isinstance(obj, Subscription):
            obj_dict = {
                'id': obj.id,
                'name': obj.feed_record.feed_name,
                'last_updated': obj.feed_record.last_updated.isoformat(),
                'last_sent': obj.last_sent.isoformat(),
            }

            if obj.feed_record.feed_name == 'results of a search query':
                feed_params = dict([(param.name, param.value) for param in
                                     obj.feed_record.feed_params.all()])

                log.debug(feed_params)

                if 'q' in feed_params:
                    obj_dict['keywords'] = '"' + '", "'.join(eval(feed_params['q'])) + '"'
                if 'controlling_bodies' in feed_params:
                    obj_dict['controlling_bodies'] = '"' + '", "'.join(eval(feed_params['controlling_bodies'])) + '"'
                if 'file_types' in feed_params:
                    obj_dict['file_types'] = '"' + '", "'.join(eval(feed_params['file_types'])) + '"'

            else:
                for feed_record_param in obj.feed_record.feed_params.all():
                    obj_dict[feed_record_param.name] = feed_record_param.value

            return obj_dict

        elif isinstance(obj, Bookmark):
            return obj.pk

        else:
            return super(SubscriberResource, self).serialize(obj)


class SimpleRefSerializer (resources.Resource):
    def serialize(self, obj):
        if hasattr(obj, 'id'):
            return obj.id

        return super(SimpleRefSerializer, self).serialize(obj)

class CouncilMemberResource (resources.ModelResource):
    model = CouncilMember
    queryset = model.objects.all().select_related('tenures').prefetch_related('tenures__district')
    exclude = ['districts']
    include = ['district', 'url', 'is_active', 'is_president', 'is_at_large']
    related_serializer = SimpleRefSerializer

#    def at_large(self, cm):
#        return cm.tenure
#    president = models.BooleanField(default=False)
#    begin = models.DateField(blank=True)
#    end = models.DateField(null=True, blank=True)

#    def serialize(self, obj):
#        self.related_serializer = CouncilMemberResource
#        if isinstance(obj, CouncilDistrict):
#            return NestedCouncilDistrictResource().serialize(obj)

#        return super(CouncilMemberResource, self).serialize(obj)


class CouncilDistrictResource (resources.ModelResource):
    model = CouncilDistrict
    queryset = model.objects.all().select_related('plan', 'tenures').prefetch_related('tenures__councilmember')
    include = ['representative', 'url']
    related_serializer = SimpleRefSerializer

    def shape(self, d):
        return d.shape.json


class CouncilDistrictPlanResource (resources.ModelResource):
    model = CouncilDistrictPlan
    queryset = model.objects.all().prefetch_related('districts')
    include = ['districts', 'url']
    related_serializer = SimpleRefSerializer

    def shape(self, d):
        return json.loads(d.shape.json)


class LegFileResource (resources.ModelResource):
    model = LegFile
    queryset = model.objects.all().select_related('metadata').prefetch_related('sponsors', 'metadata__locations')
    include = ['url', 'locations']
    related_serializer = SimpleRefSerializer

    def locations(self, f):
        return [{
            'geo': location.geom.json,
            'address': location.address
        } for location in f.metadata.locations.all()]
