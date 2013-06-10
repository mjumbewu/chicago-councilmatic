from django.core.urlresolvers import reverse
import django.forms
import haystack.forms
import haystack.query
import uni_form.helpers as helpers


def legfile_choices(field):
    from phillyleg.models import LegFile
    value_objs = LegFile.objects.values(field).distinct().order_by(field)
    values = [(value_obj[field], value_obj[field])
              for value_obj in value_objs]
    return values


def councilmember_choices():
    from phillyleg.models import CouncilMember
    values = [(member.name, member.name)
              for member in CouncilMember.objects.all().order_by('name')]
    return values

def topic_choices():
    from phillyleg.models import MetaData_Topic
    values = [(topic.topic, topic.topic)
              for topic in MetaData_Topic.objects.all().order_by('topic')]
    return values


class SimpleSearchForm (haystack.forms.SearchForm):
    q = django.forms.CharField(label='Keywords')

    @property
    def helper(self):
        """We call this as a method/property so we don't make the form helper
           a singleton. """

        # instantiate the form helper object
        helper = helpers.FormHelper()

        # add in some input controls (a.k.a. buttons)
        submit = helpers.Submit('submit', 'Search')
        helper.add_input(submit)

        # define the form action
        helper.form_action = reverse('search')
        helper.form_method = 'GET'
        return helper

    def search(self):
        from phillyleg.models import LegFile
        sqs = super(SimpleSearchForm, self).search().models(LegFile)
        return sqs

class FullSearchForm (haystack.forms.SearchForm):
    topics = django.forms.MultipleChoiceField(
        choices=topic_choices(),
        widget=django.forms.CheckboxSelectMultiple(),
        label="Narrow by topics &raquo;",
        required=False)
    statuses = django.forms.MultipleChoiceField(
        choices=legfile_choices('status'),
        widget=django.forms.CheckboxSelectMultiple(),
        label="Narrow by status &raquo;",
        required=False)
    controlling_bodies = django.forms.MultipleChoiceField(
        choices=legfile_choices('controlling_body'),
        widget=django.forms.CheckboxSelectMultiple(),
        label="Narrow by controlling body &raquo;",
        required=False)
    file_types = django.forms.MultipleChoiceField(
        choices=legfile_choices('type'),
        widget=django.forms.CheckboxSelectMultiple(),
        label="Narrow by type of legislation &raquo;",
        required=False)
    sponsors = django.forms.MultipleChoiceField(
        choices=councilmember_choices(),
        widget=django.forms.CheckboxSelectMultiple(),
        label="Narrow by sponsors &raquo;",
        required=False)

    @property
    def helper(self):
        """We call this as a method/property so we don't make the form helper
           a singleton. """

        # instantiate the form helper object
        helper = helpers.FormHelper()

        # add in some input controls (a.k.a. buttons)
        submit = helpers.Submit('submit', 'Search')
        helper.add_input(submit)

        # define the form action
        helper.form_action = reverse('search')
        helper.form_method = 'GET'
        return helper

    def search(self):
        from phillyleg.models import LegFile
        sqs = super(FullSearchForm, self).search().models(LegFile)

        if self.is_valid():
            query = self.cleaned_data['q']
            topics = self.cleaned_data['topics']
            statuses = self.cleaned_data['statuses']
            sponsor_names = self.cleaned_data['sponsors']
            file_types = self.cleaned_data['file_types']
            controlling_bodies = self.cleaned_data['controlling_bodies']

            if not query:
                sqs = haystack.query.SearchQuerySet().all()

            if topics:
                sqs = sqs.filter(topics__in=topics)

            if statuses:
                sqs = sqs.filter(status__in=statuses)

            if sponsor_names:
                sqs = sqs.filter(sponsors__in=sponsor_names)

            if file_types:
                sqs = sqs.filter(file_type__in=file_types)

            if controlling_bodies:
                sqs = sqs.filter(controlling_body__in=controlling_bodies)

        return sqs
