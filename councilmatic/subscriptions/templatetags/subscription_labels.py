from django import template
from subscriptions.feeds import ContentFeedLibrary

register = template.Library()

@register.filter
def subscription_title(subscription, library=None):
    if library is None:
        library = ContentFeedLibrary()
    
    feed = library.get_feed(subscription.feed_record)
    return feed.get_label()

@register.filter
def has_been_sent(subscription):
    return bool(subscription.dispatches.count())
