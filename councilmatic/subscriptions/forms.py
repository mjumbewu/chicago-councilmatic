import django.forms
from django.contrib import auth

import subscriptions.models as models


class SubscriptionForm (django.forms.ModelForm):
    feed = django.forms.HiddenInput()
    subscriber = django.forms.HiddenInput()

    class Meta:
        model = models.Subscription
