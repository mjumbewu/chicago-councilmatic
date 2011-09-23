class SubscriptionDispatcher (object):
    def dispatch(self, subscription):

        # Send the email

        # ...and then...
        subscription.last_sent = subscription.feed.last_updated
