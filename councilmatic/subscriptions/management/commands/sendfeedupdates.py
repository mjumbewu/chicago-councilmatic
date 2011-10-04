from django.core.management.base import BaseCommand, CommandError

from subscriptions.feeds import SubscriptionDispatcher
from subscriptions.models import Subscriber


class Command(BaseCommand):
    help = "Send a digest of the new items in the users' subscription lists."

    def handle(self, *args, **options):
        # Assuming that the feeds have been updated

        dispatcher = SubscriptionDispatcher()

        subscribers = Subscriber.objects.all()
        for subscriber in subscribers:
            dispatcher.dispatch_subscriptions_for(subscriber)
