from django.test import TestCase
from nose.tools import *

from activity_log import record
from activity_log.models import Action
from activity_log.models import AffectedContent

class Test__ActionLog_record:

    @istest
    def saves_the_specified_action (self):
        from django.contrib.auth.models import User
        the_user = User.objects.create_user('user', 'password', 'email')

        # ...with no affected items
        record(the_user, 'went overboard')

        the_activity = Action.objects.get(actor=the_user)
        assert_equal(the_activity.description, 'went overboard')

        # ...with affected items
        record(the_user, 'considered', the_activity)

        num_actions = len(Action.objects.filter(actor=the_user))
        num_affects = len(AffectedContent.objects.all())
        assert_equal(num_actions, 2)
        assert_equal(num_affects, 1)
