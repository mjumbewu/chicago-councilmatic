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
        feed_data.manager = Mock()
        feed_data.manager.all = Mock(return_value=[5])

        qs = feed_data.queryset

        assert_equal(feed_data.manager.all.call_count, 1)
        assert_equal(qs, [5])

    @istest
    def uses_filter_when_keywords_are_supplied_to_init (self):
        feed_data = LegislationUpdatesFeed(a=1, b=2)
        feed_data.manager = Mock()
        feed_data.manager.filter = Mock(return_value=[5])

        qs = feed_data.queryset

        assert_equal(feed_data.manager.filter.call_count, 1)
        feed_data.manager.filter.assert_called_with(a=1,b=2)
        assert_equal(qs, [5])

class Test_LegislationUpdatesFeed_calcLastUpdated:

    @istest
    def returns_the_intro_date_if_has_no_actions_or_final_date (self):
        from datetime import date
        legislation = Mock()
        legislation.intro_date = date(2011, 8, 5)
        legislation.final_date = None
        legislation.actions.all = Mock(return_value=[])
        feed_data = LegislationUpdatesFeed()

        last_updated = feed_data.calc_last_updated(legislation)

        assert_equal(last_updated, date(2011, 8, 5))

    @istest
    def returns_the_final_date_if_available (self):
        from datetime import date
        legislation = Mock()
        legislation.intro_date = date(2011, 8, 5)
        legislation.final_date = date(2011, 8, 10)
        legislation.actions.all = Mock(return_value=[])
        feed_data = LegislationUpdatesFeed()

        last_updated = feed_data.calc_last_updated(legislation)

        assert_equal(last_updated, date(2011, 8, 10))

    @istest
    def returns_the_latest_action_date_if_has_no_final_date (self):
        from datetime import date
        legislation = Mock()
        legislation.intro_date = date(2011, 8, 5)
        legislation.final_date = None
        action1 = Mock(); action1.date_taken = date(2011, 8, 6)
        action2 = Mock(); action2.date_taken = date(2011, 8, 7)
        action3 = Mock(); action3.date_taken = date(2011, 8, 8)
        legislation.actions.all = Mock(return_value=[action1, action2, action3])
        feed_data = LegislationUpdatesFeed()

        last_updated = feed_data.calc_last_updated(legislation)

        assert_equal(last_updated, date(2011, 8, 8))

    @istest
    def returns_the_lasest_action_date_final_date (self):
        from datetime import date
        legislation = Mock()
        legislation.intro_date = date(2011, 8, 5)
        legislation.final_date = date(2011, 8, 10)
        action1 = Mock(); action1.date_taken = date(2011, 8, 7)
        action2 = Mock(); action2.date_taken = date(2011, 8, 9)
        action3 = Mock(); action3.date_taken = date(2011, 8, 11)
        legislation.actions.all = Mock(return_value=[action1, action2, action3])
        feed_data = LegislationUpdatesFeed()

        last_updated = feed_data.calc_last_updated(legislation)

        assert_equal(last_updated, date(2011, 8, 11))
