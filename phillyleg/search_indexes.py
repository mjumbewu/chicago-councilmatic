import datetime
from haystack import indexes
from haystack import site
from phillyleg.models import LegFile


class LegFileIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    
    title = indexes.CharField(model_attr='title')
    file_id = indexes.CharField(model_attr='id')
    status = indexes.CharField(model_attr='status')
    controlling_body = indexes.CharField(model_attr='controlling_body')
    file_type = indexes.CharField(model_attr='type')
    key = indexes.IntegerField(model_attr='key')
    
    sponsors = indexes.CharField()
    
    attachments = indexes.CharField()

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return LegFile.objects.all()


site.register(LegFile, LegFileIndex)
