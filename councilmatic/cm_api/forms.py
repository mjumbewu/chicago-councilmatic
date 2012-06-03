from django import forms
from subscriptions.models import Subscriber, Subscription

class SubscriberForm (forms.Form):
    subscriptions = forms.ModelMultipleChoiceField(queryset=Subscription.objects.all(), required=False)
