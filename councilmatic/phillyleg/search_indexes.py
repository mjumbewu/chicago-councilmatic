import datetime
from haystack import indexes
from haystack import site
from phillyleg.models import LegFile, LegMinutes


class LegislationIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)

    file_id = indexes.CharField(model_attr='id')
    status = indexes.CharField(model_attr='status')
    controlling_body = indexes.CharField(model_attr='controlling_body')
    file_type = indexes.CharField(model_attr='type')
    key = indexes.IntegerField(model_attr='key')
    sponsors = indexes.MultiValueField()

    order_date = indexes.DateField(model_attr='intro_date')

    def prepare_sponsors(self, leg):
        return [sponsor.name for sponsor in leg.sponsors.all()]


class MinutesIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, model_attr='fulltext')
    date_taken = indexes.DateField(null=True)

    order_date = indexes.DateField(model_attr='date_taken')


site.register(LegFile, LegislationIndex)
site.register(LegMinutes, MinutesIndex)
