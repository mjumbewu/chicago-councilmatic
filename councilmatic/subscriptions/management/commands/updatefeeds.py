from django.core.management.base import BaseCommand, CommandError

from subscriptions.management.feeds import FeedUpdater
from subscriptions.models import ContentFeed


class Command(BaseCommand):
    help = "Update the meta-information in subscription feeds."
    
    def get_feeds(self):
        feeds = ContentFeed.objects.all()
        return feeds
    
    def handle(self, *args, **options):
        feeds = self.get_feeds()
        updater = FeedUpdater()
        updater.update_all(feeds)

