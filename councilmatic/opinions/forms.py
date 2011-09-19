from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from opinions import models


class OpinionStatementForm (forms.Form):
    POSITION_CHOICES = (
        ('support', 'Support'),
        ('oppose', 'Oppose'),
        ('abstain', 'Abstain'),
    )

    opiner = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    target_type = forms.ModelChoiceField(queryset=ContentType.objects.all(), widget=forms.HiddenInput)
    target_id = forms.IntegerField(min_value=0, widget=forms.HiddenInput)
    position = forms.ChoiceField(choices=POSITION_CHOICES, widget=forms.RadioSelect)
    statement = forms.CharField(widget=forms.Textarea)

    def save(self, commit=True):
        opiner = self.cleaned_data['opiner']
        target_type = self.cleaned_data['target_type']
        target_id = self.cleaned_data['target_id']
        target = target_type.get_object_for_this_type(pk=target_id)
        statement = self.cleaned_data['statement']
        position = self.cleaned_data['position']

        voice = models.Voice(opiner)

        try:
            opinion = opiner.opinions.get(
                target_id=target_id,
                target_type=target_type)
            voice.revise(
                opinion,
                statement=statement,
                position=position,
                commit=commit)

        except models.Opinion.DoesNotExist:
            opinion = voice.express_opinion_about(
                target,
                statement=statement,
                position=position,
                commit=commit)

        if not commit:
            self.save_m2m = voice.save_revision

        return opinion
