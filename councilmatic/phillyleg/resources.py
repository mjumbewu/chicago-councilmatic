from djangorestframework import views, permissions

import models

class CouncilMemberListView (views.ListModelView):
    model = models.CouncilMember

class CouncilMemberInstanceView (views.InstanceModelView):
    model = models.CouncilMember
    permissions = [permissions.IsUserOrIsAnonReadOnly]
