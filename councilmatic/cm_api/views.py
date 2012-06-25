from djangorestframework import views
from djangorestframework.mixins import PaginatorMixin
from djangorestframework.permissions import IsUserOrIsAnonReadOnly
from . import resources
from . import permissions

class SubscriberView (views.InstanceModelView):
    resource = resources.SubscriberResource
    permissions = [permissions.IsRequestingOwnInfoOrReadOnly]
    allowed_methods = ['GET']

class SubscriberListView (views.ListOrCreateModelView):
    resource = resources.SubscriberResource

class SubscriptionView (views.InstanceModelView):
    resource = resources.SubscriptionResource

class SubscriptionListView (views.ListOrCreateModelView):
    resource = resources.SubscriptionResource

class ROListModelView (views.ListModelView):
    allowed_methods = ['GET']

    def get_query_kwargs(self, *args, **kwargs):
        pk_list = kwargs.pop('pk_list', None)
        qargs = super(ROListModelView, self).get_query_kwargs(*args, **kwargs)

        if pk_list:
            pk_list = pk_list.split(',')
            qargs['pk__in'] = pk_list

        return qargs

class ROInstanceModelView (views.InstanceModelView):
    allowed_methods = ['GET']

class CouncilMemberListView (ROListModelView):
    resource = resources.CouncilMemberResource

class CouncilMemberInstanceView (ROInstanceModelView):
    resource = resources.CouncilMemberResource
    permissions = [IsUserOrIsAnonReadOnly]

class CouncilDistrictListView (ROListModelView):
    resource = resources.CouncilDistrictResource

class CouncilDistrictInstanceView (ROInstanceModelView):
    resource = resources.CouncilDistrictResource

class CouncilDistrictPlanListView (ROListModelView):
    resource = resources.CouncilDistrictPlanResource

class CouncilDistrictPlanInstanceView (ROInstanceModelView):
    resource = resources.CouncilDistrictPlanResource

class LegFileListView (PaginatorMixin, ROListModelView):
    resource = resources.LegFileResource

class LegFileInstanceView (ROInstanceModelView):
    resource = resources.LegFileResource
