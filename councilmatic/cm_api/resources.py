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

class SubscriptionResource (resources.ModelResource):
    model = Subscription
    fields = ['id', 'name', 'last_updated', 'last_sent']

    def feed_params(self, obj):
        if not hasattr(self, '_feed_params'):
            self._feed_params = {}

        if obj not in self._feed_params:
            if obj.feed_record.feed_name == 'results of a search query':
                self._feed_params = dict([(param.name, param.value) for param in
                                          obj.feed_record.feed_params.all()])
                log.debug(feed_params)
            else:
                self._feed_params = {}

        return self._feed_params[obj]

    def keywords(self, obj):
        fp = self.feed_params
        return '"' + '", "'.join(eval(fp['q'])) + '"'

    def controlling_bodies(self, obj):
        fp = self.feed_params
        return '"' + '", "'.join(eval(fp['controlling_bodies'])) + '"'

    def file_types(self, obj):
        fp = self.feed_params
        return '"' + '", "'.join(eval(fp['file_types'])) + '"'

    def serialize_one(self, obj):
        additional = {}
        self.fields = self.fields[:]
        if obj.feed_record.feed_name == 'results of a search query':
            fp = self.feed_params = dict([(param.name, param.value) for param in
                                          obj.feed_record.feed_params.all()])

            if 'q' in fp:
                self.fields.append('keywords')
            if 'controlling_bodies' in fp:
                self.fields.append('controlling_bodies')
            if 'file_types' in fp:
                self.fields.append('file_types')
            log.debug(self.feed_params)
        
        else:
            for feed_record_param in obj.feed_record.feed_params.all():
                additional[feed_record_param.name] = feed_record_param.value

        obj_dict = super(SubscriptionResource, self).serialize(obj)
        obj_dict.update(additional)
        return obj_dict

    def serialize(self, queryset):
        return [self.serialize_one(obj) for obj in queryset.all()]
        

class BookmarkResource (resources.ModelResource):
    model = Bookmark

    def serialize(self, queryset):
        return [obj.pk for obj in queryset.all()]


class SubscriberResource (resources.ModelResource):
    model = Subscriber
    form = SubscriberForm
    fields = ['username', 'email', 'id', 'url', 
              ('bookmarks', BookmarkResource),
              ('subscriptions', SubscriptionResource)]


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
