from subscriptions.models import FeedData
from phillyleg.models import LegFile


class NewLegislationFeed (FeedData):
    queryset = LegFile.objects.all()
    def calc_last_updated(self, legfile):
        return legfile.intro_date


class LegislationUpdatesFeed (FeedData):
    def __init__(self, **selector):
        self.queryset = LegFile.objects.all().filter(**selector)
    
    def calc_last_updated(self, legfile):
        return max(chain(
            [legfile.intro_date, legfile.final_date or datetime.date(1970,1,1)],
            [action.date_taken for action in legfile.legaction_set.all()]))


