import django.forms
import haystack.forms

class SearchSubscriptionForm (django.forms.Form):
    email = django.forms.EmailField();
    query = django.forms.CharField();
    models = django.forms.MultipleChoiceField(choices=haystack.forms.model_choices())
    updates = django.forms.ChoiceField(choices=((True, 'yes'),(False,'no')), initial=True)
