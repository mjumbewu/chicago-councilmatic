from django.core.management.base import BaseCommand, CommandError
from phillyleg.models import LegFile, LegFileMetaData, MetaData_Topic


class Command(BaseCommand):
    help = "python manage.py reclassify"
    def handle(self,  *args, **options):
        legs = LegFile.objects.all()
        for i, leg in enumerate(legs) :
            if i % 100 == 0 :
                print i
            metadata = LegFileMetaData.objects.get_or_create(legfile=leg)[0]
            metadata.topics.clear()

            for topic in leg.topics():
                t = MetaData_Topic.objects.get_or_create(topic=topic)[0]
                metadata.topics.add(t)

            metadata.save()
