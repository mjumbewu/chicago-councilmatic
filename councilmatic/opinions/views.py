from django.contrib import messages
from django.contrib import contenttypes
from django.http import HttpResponseRedirect
from django.views import generic as views

import opinions.forms as forms
import opinions.models as models


class SingleOpinionTargetMixin (object):
    def get_context_data(self, **kwargs):
        context = super(SingleOpinionTargetMixin, self).get_context_data(**kwargs)

        user = self.request.user
        contenttype = contenttypes.models.ContentType.objects.get_for_model(self.object)

        if not user.is_authenticated():
            opinion = None
            is_opined = False
            opinion_form = None
        else:
            initial_data = {
                'opiner': user.pk,
                'target_type': contenttype.pk,
                'target_id': self.object.pk,
            }

            try:
                opinion = user.opinions.get(target_id=self.object.pk,
                                            target_type=contenttype.pk)
                initial_data.update({
                    'statement': opinion.latest.statement,
                    'position': opinion.latest.position,
                })

            except models.Opinion.DoesNotExist:
                opinion = None

            opinion_form = forms.OpinionStatementForm(initial=initial_data)

        context['opinion'] = opinion
        context['contenttype'] = contenttype
        context['is_opined'] = opinion is not None
        context['opinion_form'] = opinion_form

        return context


class ExpressOpinionView (views.CreateView):
    form_class = forms.OpinionStatementForm
    http_method_names = ['post']

    def form_invalid(self, form):
        request = self.request
        messages.add_message(request, messages.ERROR, 'Could express opinion')
        messages.add_message(request, messages.DEBUG, form.errors)
        return HttpResponseRedirect(self.request.POST['next'])

    def get_success_url(self):
        return self.request.POST['next']


class ReviseOpinionView (views.UpdateView):
    model = models.Opinion
    form_class = forms.OpinionStatementForm
    http_method_names = ['post']

    def form_invalid(self, form):
        messages.add_message(request, messages.ERROR, 'Could revise opinion')
        messages.add_message(request, messages.DEBUG, form.errors)
        return HttpResponseRedirect(self.request.POST['next'])

    def get_success_url(self):
        return self.request.POST['next']
