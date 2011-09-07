from nose.tools import *
from mock import *

from main.feeds import *

class Test_NewLegislationFeed_calcLastUpdated:

    @istest
    def returns_the_intro_date_of_a_piece_of_legislation (self):
        legislation = Mock()
        legislation.intro_date = 5

        feed_data = NewLegislationFeed()
        last_updated = feed_data.calc_last_updated(legislation)

        assert_equal(last_updated, 5)


class Test_LegislationUpdatesFeed_queryset:

    @istest
    def uses_all_when_no_keywords_are_supplied_to_init (self):
        feed_data = LegislationUpdatesFeed()
        feed_data.qs_base = Mock()

        qs = feed_data.get_queryset()

        assert_equal(feed_data.qs_base.all.call_count, 1)
        assert_equal(feed_data.qs_base.filter.call_count, 0)

    @istest
    def uses_filter_when_keywords_are_supplied_to_init (self):
        feed_data = LegislationUpdatesFeed(a=1, b=2)
        feed_data.qs_base = Mock()

        qs = feed_data.get_queryset()

        assert_equal(feed_data.qs_base.all.call_count, 0)
        assert_equal(feed_data.qs_base.filter.call_count, 1)
        feed_data.qs_base.filter.assert_called_with(a=1,b=2)

class Test_LegislationUpdatesFeed_calcLastUpdated:

    @istest
    def returns_the_intro_date_if_has_no_actions_or_final_date (self):
        legislation = Mock()
        legislation.intro_date = 5
        legislation.final_date = None
        legislation.actions.all = Mock(return_value=[])

        feed_data = LegislationUpdatesFeed()
