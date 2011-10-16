from django.contrib import messages
from django.contrib import contenttypes
from django.http import HttpResponseRedirect
from django.views import generic as views

import bookmarks.forms as forms
import bookmarks.models as models


class BaseBookmarkMixin (object):
    def get_bookmark_data(self, content):
        user = self.request.user
        contenttype = contenttypes.models.ContentType.objects.get_for_model(content)

        if not user.is_authenticated():
            bookmark = None
            is_bookmarked = False
            bookmark_form = None
        else:
            try:
                bookmark = user.bookmarks.get(content_id=content.pk,
                                              content_type=contenttype.pk)
                is_bookmarked = True
                bookmark_form = None

            except models.Bookmark.DoesNotExist:
                bookmark = None
                is_bookmarked = False
                bookmark_form = forms.BookmarkForm({'user': user.pk,
                                                    'content_id': content.pk,
                                                    'content_type': contenttype.pk})

        return bookmark, contenttype, bookmark_form

    def get_bookmarks_data(self, content_list):
        data = [(content,) + self.get_bookmark_data(content)
                for content in content_list]
        return data


class SingleBookmarkedObjectMixin (BaseBookmarkMixin):
    def get_context_data(self, **kwargs):
        context = super(SingleBookmarkedObjectMixin, self).get_context_data(**kwargs)

        bookmark, contenttype, bookmark_form = self.get_bookmark_data(self.object)

        context['bookmark'] = bookmark
        context['is_bookmarked'] = bookmark is not None
        context['content_type'] = contenttype.pk
        context['bookmark_form'] = bookmark_form

        return context


class MultipleBookmarkedObjectsMixin (BaseBookmarkMixin):
    def get_context_data(self, **kwargs):
        context = super(MultipleBookmarkedObjectsMixin, self).get_context_data(**kwargs)

        # Use the object_list from the context; it's already paginated, so it's
        # potentially a small subset of what's available.  Getting bookmark
        # data is relatively expensive.
        object_list = context['object_list']
        context['bookmark_data'] = self.get_bookmarks_data(object_list)

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
