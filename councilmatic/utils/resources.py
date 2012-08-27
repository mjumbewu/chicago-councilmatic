import json
from djangorestframework import resources

class GeoModelMixin (object):
    """
    A mixin for serializing objects build around geometry fields.
    """

    geometry_field = None

    def get_fields(self, *args, **kwargs):
        fields = super(GeoModelMixin, self).get_fields(*args, **kwargs)
        fields.remove(self.geometry_field)
        return fields

    def serialize_iter(self, obj):
        features = super(GeoModelMixin, self).serialize_iter(obj)
        return {
            'type': 'FeatureCollection',
            'features': features
        }

    def serialize_model(self, obj):
        geometry_obj = getattr(obj, self.geometry_field)
        geometry = self.serialize_geometry(geometry_obj)
        properties = super(GeoModelMixin, self).serialize_model(obj)
        return {
            'type': 'Feature',
            'geometry': geometry,
            'properties': properties
        }

    def serialize_geometry(self, obj):
        return json.loads(obj.json)
