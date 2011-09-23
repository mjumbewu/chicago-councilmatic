import datetime
from itertools import chain

from subscriptions.models import FeedData
from phillyleg.models import LegFile
from phillyleg.models import LegMinutes
from haystack.query import SearchQuerySet


class NewLegislationFeed (FeedData):
    queryset = LegFile.objects.all()

    def calc_last_updated(self, legfile):
        return legfile.intro_date


class LegislationUpdatesFeed (FeedData):
    manager = LegFile.objects

    def __init__(self, **selectors):
        self.selectors = selectors

    @property
    def queryset(self):
        if self.selectors:
            return self.manager.filter(**self.selectors)
        else:
            return self.manager.all()

    def calc_last_updated(self, legfile):
        legfile_date = max(legfile.intro_date,
                           legfile.final_date or datetime.date(1970, 1, 1))
        action_dates = [action.date_taken
                        for action in legfile.actions.all()]

        return max([legfile_date] + action_dates)


class SearchResultsFeed (FeedData):
    def __init__(self, search_filter):
        self.filter = search_filter

    @property
    def queryset(self):
        return SearchQuerySet().filter(self.filter)

    def calc_last_updated(self, item):
        if isinstance(item, LegFile):
            return item.intro_date
        elif isinstance(item, LegMinutes):
            return item.date_taken
