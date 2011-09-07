from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

import models

class BookmarkForm (forms.ModelForm):
    user = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=User.objects.all())
    content_type = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=ContentType.objects.all())
    content_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = models.Bookmark
