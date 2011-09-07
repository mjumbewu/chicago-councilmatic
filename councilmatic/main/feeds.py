import datetime
from itertools import chain

from subscriptions.models import FeedData
from phillyleg.models import LegFile


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
        return max(chain(
            [legfile.intro_date, legfile.final_date or datetime.date(1970,1,1)],
            [action.date_taken for action in legfile.actions.all()]))
