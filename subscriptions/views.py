import haystack.views
import subscriptions.forms as forms

class SearchView (haystack.views.SearchView):
    def extra_context(self):
        return {
            'subs_form': forms.SearchSubscriptionForm()
        }
        
