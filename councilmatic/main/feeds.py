import datetime
import logging
from collections import defaultdict
from itertools import chain

from subscriptions.feeds import ContentFeed
from subscriptions.feeds import ContentFeedLibrary
from phillyleg.models import LegFile
from phillyleg.models import LegMinutes
from haystack.query import SearchQuerySet


log = logging.getLogger(__name__)
library = ContentFeedLibrary()

class NewLegislationFeed (ContentFeed):
    def get_content(self):
        return LegFile.objects.all()

    def get_updates_since(self, datetime):
        return self.get_content().filter(intro_date__gt=datetime)

    def get_changes_to(self, legfile, since_datetime):
        if since_datetime.date() <= self.get_last_updated(legfile):
            return {'Title': legfile.title}
        else:
            return {}

    def get_last_updated(self, legfile):
        return legfile.intro_date

    def get_params(self):
        return {}


class LegislationUpdatesFeed (ContentFeed):
    manager = LegFile.objects

    def __init__(self, **selectors):
        self.selectors = selectors

    def get_content(self):
        if self.selectors:
            return self.manager.filter(**self.selectors)
        else:
            return self.manager.all()

    def get_updates_since(self, datetime):
        return [content_item for content_item in self.get_content()
                if self.get_last_updated(content_item) > datetime.date()]

    def get_changes_to(self, legfile, since_datetime):
        changes = defaultdict(unicode)
        for action in legfile.actions.all():
            if action.date_taken > since_datetime.date():
                if 'Actions' in changes:
                    changes['Actions'] += u'\n'
                changes['Actions'] += unicode(action)

        return changes

    def get_last_updated(self, legfile):
        legfile_date = max(legfile.intro_date,
                           legfile.final_date or datetime.date(1970, 1, 1))
        action_dates = [action.date_taken
                        for action in legfile.actions.all()]

        return max([legfile_date] + action_dates)

    def get_params(self):
        return self.selectors


from django.dispatch import receiver
from django.db.models.signals import post_save
from subscriptions.models import Subscriber

@receiver(post_save, sender=Subscriber)
def create_bookmarks_subscription_for_subscriber(sender, **kwargs):
    """
    Create a Subscriber object whenever a user is created.  This is useful so
    that we don't have to patch whatever different registration processes we
    end up using.
    """
    subscriber = kwargs.get('instance')
    created = kwargs.get('created')
    raw = kwargs.get('raw')

    logging.info('subscriber is %r' % subscriber)

    if created and not raw:
        feed = BookmarkedContentFeed(subscriber)
        if subscriber.subscription(feed) is None:
            subscriber.subscribe(feed)
            logging.info('created bookmarks subscription')


class BookmarkedContentFeed (LegislationUpdatesFeed):
    def __init__(self, user):
        if isinstance(user, (int, basestring)):
            self.user = Subscriber.objects.get(pk=user)
        else:
            self.user = user

    def get_content(self):
        # This results in N queries, but could be achieved in 1.
        # Should probably be optimized.
        return [bookmark.content for bookmark in self.user.bookmarks.all()]

    def get_params(self):
        return {'user': self.user.pk}


class SearchResultsFeed (ContentFeed):
    def __init__(self, **search_filter):
        """
        As you'll see in main.SearchView.get_content_feed, we use the value of
        search_view.results.queryset.query.query_filter to store the search.
        I'm not certain, but I'm pretty sure this value is search backend-
        specific.  Just keep that in mind.

        """
        self.filter = search_filter

    def get_content(self):
        return SearchQuerySet().raw_search(self.filter)

    def get_changes_to(self, item, datetime):
        if isinstance(item, LegFile):
            return {'Title': item.title}
        elif isinstance(item, LegMinutes):
            return {'Minutes': str(item)}

    def get_last_updated(self, item):
        if isinstance(item, LegFile):
            return item.intro_date
        elif isinstance(item, LegMinutes):
            return item.date_taken

    def get_params(self):
        return self.filter


library.register(NewLegislationFeed, 'newly introduced legislation')
library.register(LegislationUpdatesFeed, 'updates to a piece of legislation')
library.register(SearchResultsFeed, 'results of a search query')
library.register(BookmarkedContentFeed, 'bookmarked content')
