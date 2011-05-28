import datetime
from haystack import indexes
from haystack import site
from phillyleg.models import LegFile


class LegFileIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    
    file_id = indexes.CharField(model_attr='id')
    status = indexes.CharField(model_attr='status')
    controlling_body = indexes.CharField(model_attr='controlling_body')
    file_type = indexes.CharField(model_attr='type')
    key = indexes.IntegerField(model_attr='key')
    sponsors = indexes.MultiValueField()
    
    def prepare_sponsors(self, leg):
        return [sponsor.name for sponsor in leg.sponsors.all()]


    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return LegFile.objects.all()


site.register(LegFile, LegFileIndex)
