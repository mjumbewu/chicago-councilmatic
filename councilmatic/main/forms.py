from django.core.urlresolvers import reverse
import django.forms
import haystack.forms
import haystack.query
import uni_form.helpers as helpers


def legfile_choices(field):
    from phillyleg.models import LegFile
    value_objs = LegFile.objects.values(field).distinct()
    values = set((value_obj[field], value_obj[field])
              for value_obj in value_objs)
    return values


def councilmember_choices():
    from phillyleg.models import CouncilMember
    values = set((member.pk, member.name)
              for member in CouncilMember.objects.all())
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


class FullSearchForm (haystack.forms.SearchForm):
    statuses = django.forms.MultipleChoiceField(
        choices=legfile_choices('status'),
        widget=django.forms.CheckboxSelectMultiple(),
        label="Narrow by Status",
        required=False)
    controlling_bodies = django.forms.MultipleChoiceField(
        choices=legfile_choices('controlling_body'),
        widget=django.forms.CheckboxSelectMultiple(),
        label="Narrow by Controlling Body",
        required=False)
    file_types = django.forms.MultipleChoiceField(
        choices=legfile_choices('type'),
        widget=django.forms.CheckboxSelectMultiple(),
        label="Narrow by Type of Legislation",
        required=False)
    sponsors = django.forms.MultipleChoiceField(
        choices=councilmember_choices(),
        widget=django.forms.CheckboxSelectMultiple(),
        label="Narrow by Sponsors",
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
        sqs = super(FullSearchForm, self).search()

        if self.is_valid():
            query = self.cleaned_data['q']
            statuses = self.cleaned_data['statuses']
            sponsors = [Councilmember.get(pk=sponsor)
                        for sponsor in self.cleaned_data['sponsors']]
            file_types = self.cleaned_data['file_types']
            controlling_bodies = self.cleaned_data['controlling_bodies']

            if not query:
                sqs = haystack.query.SearchQuerySet().all()

            if statuses:
                sqs = sqs.filter(status__in=statuses)

            if sponsors:
                sqs = sqs.filter(sponsor__in=sponsors)

            if file_types:
                sqs = sqs.filter(type__in=file_types)

            if controlling_bodies:
                sqs = sqs.filter(controlling_body__in=controlling_bodies)

        return sqs
