from django.test import TestCase, Client
from nose.tools import *

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from subscriptions.models import Subscriber

class TestSubscriberPermissions:

    @istest
    def allow_super_user_to_read_modify_and_delete_other_users(self):
        Subscriber.objects.all().delete()
        User.objects.all().delete()

        admin = User.objects.create_superuser('admin', 'x@y.org', 'password')
        other = User.objects.create_user('other', 'x@y.org', 'password')

        client = Client()
        print client.login(username='admin', password='password')

        res = client.get('/api/v2/subscribers/' + str(other.subscriber.pk))
        assert_equal(res.status_code, 200)

        res = client.put('/api/v2/subscribers/' + str(other.subscriber.pk), data={})
        assert_equal(res.status_code, 200, res)
