import datetime
from haystack import indexes
from phillyleg.models import LegFile, LegMinutes


class LegislationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    file_id = indexes.CharField(model_attr='id')
    topics = indexes.MultiValueField()
    status = indexes.CharField(model_attr='status')
    controlling_body = indexes.CharField(model_attr='controlling_body')
    file_type = indexes.CharField(model_attr='type')
    key = indexes.IntegerField(model_attr='key')
    sponsors = indexes.MultiValueField()

    order_date = indexes.DateField(model_attr='intro_date')

    def get_model(self):
        return LegFile

    def prepare_sponsors(self, leg):
        return [sponsor.name for sponsor in leg.sponsors.all()]

    def prepare_topics(self, leg):
	return [topic.topic for topic in leg.metadata.topics.all()]

    def get_updated_field(self):
        return 'updated_datetime'


class MinutesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='fulltext')
    date_taken = indexes.DateField(null=True)

    order_date = indexes.DateField(model_attr='date_taken')

    def get_model(self):
        return LegMinutes

    def get_updated_field(self):
        return 'updated_datetime'
