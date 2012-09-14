import datetime
import logging
from collections import defaultdict
from itertools import chain
from itertools import product

from subscriptions.feeds import ContentFeed
from subscriptions.feeds import ContentFeedLibrary
from phillyleg.models import LegFile
from phillyleg.models import LegMinutes
from haystack.query import SearchQuerySet


log = logging.getLogger(__name__)
library = ContentFeedLibrary()

class NewLegislationFeed (ContentFeed):
    def get_content(self):
        return LegFile.objects.all().order_by('-intro_date')

    def get_updates_since(self, datetime):
        return self.get_content().filter(intro_date__gt=datetime)

    def get_changes_to(self, legfile, since_datetime):
        if since_datetime.date() <= legfile.intro_date:
            return {'Title': legfile.title}
        else:
            return {}

    def get_last_updated_time(self):
        legfiles = self.get_content()
        return legfiles[0].intro_date

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
                if self.get_last_updated_time_for_file(content_item) > datetime.date()]

    def get_changes_to(self, legfile, since_datetime):
        changes = defaultdict(unicode)
        for action in legfile.actions.all():
            if action.date_taken > since_datetime.date():
                if 'Actions' in changes:
                    changes['Actions'] += u'\n'
                changes['Actions'] += unicode(action)

        return changes

    def get_last_updated_time(self):
        dates = set()
        for legfile in self.get_content():
            dates.add(self.get_last_updated_time_for_file(legfile))

        return max(dates)

    def get_last_updated_time_for_file(self, legfile):
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
            try:
                self.user = Subscriber.objects.get(pk=user)
            except Subscriber.DoesNotExist, e:
                raise self.IsObsolete(e)
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

    @property
    def _exploded_filter(self):
        """
        Take the filter as provided and explode it into a number of filters fit
        for disjoining.  For example:

          filter = {content: 'street', type: ['Bill', 'Resolution']}

        becomes:

          exploded_filter = [{content: 'street', type: 'Bill'},  # or
                             {content: 'street', type: 'Resolution'}]
        """
        keys = self.filter.keys()
        values = self.filter.values()

        # Make everything a list
        value_lists = [value if isinstance(value, list) else [value]
                       for value in values]

        # Take the cartesian product and use each resulting tuple as a
        # disjointed set of values
        return [dict(zip(keys, values)) for values in product(*value_lists)]

    def get_content(self):
        filters = self._exploded_filter

        qs = SearchQuerySet()
        for _filter in filters:
            qs = qs.filter_or(**_filter)

        return qs

    def get_changes_to(self, item, datetime):
        if item.model_name == 'legfile':
            return {'Title': item.object.title}
        elif item.model_name == 'legminutes':
            return {'Minutes': str(item.object)}

    def get_last_updated_time(self):
        content = self.get_content()
        return content[0].order_date

    def get_updates_since(self, datetime):
        return self.get_content().filter(order_date__gt=datetime)

    def get_params(self):
        return self.filter


def register_feeds():
    library.register(NewLegislationFeed, 'newly introduced legislation')
    library.register(LegislationUpdatesFeed, 'updates to a piece of legislation')
    library.register(SearchResultsFeed, 'results of a search query')
    library.register(BookmarkedContentFeed, 'bookmarked content')

register_feeds()
