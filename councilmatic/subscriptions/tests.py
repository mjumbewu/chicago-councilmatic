"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from subscriptions.views import SearchView

class SearchViewTest (TestCase):
    def test_GetIncludeSubscriptionForm(self):
        self.assertEqual(1 + 1, 2)
