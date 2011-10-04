from django.core.management.base import BaseCommand, CommandError

from subscriptions.feeds import ContentFeedRecordUpdater
from subscriptions.models import ContentFeedRecord


class Command(BaseCommand):
    help = "Update the meta-information for the subscription content feeds."

    def get_records(self):
        records = ContentFeedRecord.objects.all()
        return feeds

    def handle(self, *args, **options):
        records = self.get_records()
        updater = ContentFeedRecordUpdater()
        updater.update_all(records)
