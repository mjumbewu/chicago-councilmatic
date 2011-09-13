from django.contrib import messages
from django.contrib import contenttypes
from django.http import HttpResponseRedirect
from django.views import generic as views

import bookmarks.forms as forms
import bookmarks.models as models


class SingleBookmarkedObjectMixin (object):
    def get_context_data(self, **kwargs):
        context = super(SingleBookmarkedObjectMixin, self).get_context_data(**kwargs)

        user = self.request.user
        contenttype = contenttypes.models.ContentType.objects.get_for_model(self.object)

        if not user.is_authenticated():
            bookmark = None
            is_bookmarked = False
            bookmark_form = None
        else:
            try:
                bookmark = user.bookmarks.get(content_id=self.object.pk,
                                              content_type=contenttype.pk)
                is_bookmarked = True
                bookmark_form = None

            except models.Bookmark.DoesNotExist:
                bookmark = None
                is_bookmarked = False
                bookmark_form = forms.BookmarkForm({'user': self.request.user.pk,
                                                    'content_id': self.object.pk,
                                                    'content_type': contenttype.pk})

        context['bookmark'] = bookmark
        context['is_bookmarked'] = is_bookmarked
        context['content_type'] = contenttype.pk
        context['bookmark_form'] = bookmark_form

        return context


class CreateBookmarkView (views.CreateView):
    form_class = forms.BookmarkForm
    http_method_names = ['post']

    def form_invalid(self, form):
        messages.add_message(request, messages.ERROR, 'Could not bookmark content')
        messages.add_message(request, messages.DEBUG, form.errors)
        return HttpResponseRedirect(self.request.POST['next'])

    def get_success_url(self):
        return self.request.POST['next']


class DeleteBookmarkView (views.DeleteView):
    model = models.Bookmark
    http_method_names = ['post']

    def get_success_url(self):
        return self.request.POST['next']
