from django.core.management.base import BaseCommand, CommandError

from subscriptions.feeds import import_all_feeds
from subscriptions.feeds import ContentFeedRecordUpdater
from subscriptions.models import ContentFeedRecord
from subscriptions.models import Subscription


class Command(BaseCommand):
    help = "Update the meta-information for the subscription content feeds."

    def get_records(self):
        records = ContentFeedRecord.objects.all()
        return records

    def handle(self, *args, **options):
        import_all_feeds()

        # Get rid of unused records
        used_record_ids = Subscription.objects.values('feed_record__id').distinct()
        ContentFeedRecord.objects.exclude(id__in=used_record_ids).delete()

        records = self.get_records()
        updater = ContentFeedRecordUpdater()
        updater.update_all(records)
