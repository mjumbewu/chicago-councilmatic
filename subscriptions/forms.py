import django.forms
import haystack.forms
import haystack.query
import subscriptions.models as models

def legfile_choices(field):
    from phillyleg.models import LegFile
    value_objs = LegFile.objects.values(field).distinct()
    values = [(value_obj[field], value_obj[field]) 
              for value_obj in value_objs]
    return values

def councilmember_choices():
    from phillyleg.models import CouncilMember
    values = [(member.pk, member.name)
              for member in CouncilMember.objects.all()]
    return values


class SimpleSearchForm (haystack.forms.SearchForm):
    pass

class FullSearchForm (haystack.forms.SearchForm):
    statuses = django.forms.MultipleChoiceField(
        choices=legfile_choices('status'), 
        widget=django.forms.CheckboxSelectMultiple(),
        label="Status",
        required=False)
    controlling_bodies = django.forms.MultipleChoiceField(
        choices=legfile_choices('controlling_body'), 
        widget=django.forms.CheckboxSelectMultiple(),
        label="Controlling Body",
        required=False)
    file_types = django.forms.MultipleChoiceField(
        choices=legfile_choices('type'), 
        widget=django.forms.CheckboxSelectMultiple(),
        label="Type of Legislation",
        required=False)
    sponsors = django.forms.MultipleChoiceField(
        choices=councilmember_choices(), 
        widget=django.forms.CheckboxSelectMultiple(),
        label="Sponsors",
        required=False)
    
    def search(self):
        sqs = super(FullSearchForm, self).search()
        
        if self.is_valid():
            query = self.cleaned_data['q']
            statuses = self.cleaned_data['statuses']
            sponsors = [Councilmember.get(pk=sponsor) for sponsor in self.cleaned_data['sponsors']]
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
    
class SearchSubscriptionForm (django.forms.Form):
    email = django.forms.EmailField();
    query = django.forms.CharField();
    models = django.forms.MultipleChoiceField(choices=haystack.forms.model_choices())
    updates = django.forms.ChoiceField(choices=((True, 'yes'),(False,'no')), initial=True)
    
    def __init__(self, instance=None, *args, **kwargs):
        super(SearchSubscriptionForm, self).__init__(*args, **kwargs)
    
    def get_channel(self):
        channel = models.EmailChannel.get_or_create(email=self.email.value())
        return channel
    
    def get_query(self):
        return self.query
    
    def save(self):
        subscription = model.SearchSubscription.objects.create(
            channel=self.get_channel(), query=self.get_query())
        subscription.save()
        

