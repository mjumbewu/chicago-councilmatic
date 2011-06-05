import django.forms
import haystack.forms
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

    
class FullSearchForm (haystack.forms.SearchForm):
    statuses = django.forms.MultipleChoiceField(choices=legfile_choices('status'), required=False)
    controlling_bodies = django.forms.MultipleChoiceField(choices=legfile_choices('controlling_body'), required=False)
    file_types = django.forms.MultipleChoiceField(choices=legfile_choices('type'), required=False)
    sponsors = django.forms.MultipleChoiceField(choices=councilmember_choices(), required=False)
    
    def search(self):
        sqs = super(FullSearchForm, self).search()
        
        if self.is_valid():
            statuses = self.cleaned_data['statuses']
            
            if statuses:
                sqs = sqs.filter(status__in=statuses)
        
        return sqs
    
class SearchSubscriptionForm (django.forms.Form):
    email = django.forms.EmailField();
    query = django.forms.CharField();
    models = django.forms.MultipleChoiceField(choices=haystack.forms.model_choices())
    updates = django.forms.ChoiceField(choices=((True, 'yes'),(False,'no')), initial=True)
    
    def save(self):
        subscriber = models.Subscriber.get_or_create(email=self.email.value())

