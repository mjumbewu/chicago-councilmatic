from djangorestframework import permissions
from djangorestframework import status
from djangorestframework.response import ErrorResponse

class IsRequestingOwnInfoOrReadOnly (permissions.BasePermission):
    """
    This is meant to be used only in cases where self.view.get_instance().user
    resolves to a user object. The request is read-only unless the user is
    a superuser, or is authenticated and is the user attached to the view's
    instance.
    """

    @staticmethod
    def get_view_model_instance(view):
        """
        For the given view, get the arguments for the instance, and then get
        the instance, raising a 404 if no such instance exists.

        """
        model = view.resource.model
        query_kwargs = view.get_query_kwargs(
            view.request,
            *view.args,
            **view.kwargs)

        try:
            model_instance = view.get_instance(**query_kwargs)
        except model.DoesNotExist:
            raise ErrorResponse(
                status.HTTP_404_NOT_FOUND,
                {'detail': ('No object matching those parameters exists.')})

        return model_instance

    def raise_forbidden(self):
        """
        Raise a 403 forbidden HTTP error.

        """
        raise ErrorResponse(
            status.HTTP_403_FORBIDDEN,
            {'detail': ('You do not have permission to access this '
                        'resource. You may need to login or otherwise '
                        'authenticate the request.')})

    def check_permission(self, user):
        if user.is_superuser:
            return

        if self.view.method in ('GET', 'HEAD'):
            return

        if not user.is_authenticated():
            self.raise_forbidden()

        model_instance = self.get_view_model_instance(self.view)
        if user == model_instance.user:
            return

        else:
            self.raise_forbidden()
