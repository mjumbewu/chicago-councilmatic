from djangorestframework import views
from djangorestframework.reverse import reverse
from djangorestframework.mixins import PaginatorMixin
from djangorestframework.permissions import IsUserOrIsAnonReadOnly
from . import resources
from . import permissions

class ApiIndexView (views.View):
    """
    This API is definitely a work in progress.  It is a read-only API through
    which you can access council members, districts, and legislation.  If you
    have any issues or suggestions, please file an issue on the [GitHub] page,
    or contact admin@councilmatic.org.

    [GitHub]: https://github.com/codeforamerica/councilmatic
    """
    def get(self, request):
        return {
            'councilmembers': reverse('api_councilmember_list', request=request),
            'districts': reverse('api_district_list', request=request),
            'district_plans': reverse('api_district_plan_list', request=request),
            'legislative_files': reverse('api_legfile_list', request=request)
        }

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

#    def get_description(self):
#        if self.__doc__:
#            return

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
    """
    A district plan represents a particular geographic arrangement of council
    districts.  Each plan has two important fields:

    - `districts`: The list of references to district resources
    - `date`: The date that the district plan went into effect
    """
    resource = resources.CouncilDistrictPlanResource

class CouncilDistrictPlanInstanceView (ROInstanceModelView):
    resource = resources.CouncilDistrictPlanResource

class LegFileListView (PaginatorMixin, ROListModelView):
    resource = resources.LegFileResource

class LegFileInstanceView (ROInstanceModelView):
    resource = resources.LegFileResource
