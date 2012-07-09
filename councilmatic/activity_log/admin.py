from django.contrib import admin
from activity_log.models import (Action, AffectedContent)

class AffectedContentInline(admin.StackedInline):
    model = AffectedContent

class ActionAdmin(admin.ModelAdmin):
    inlines = [AffectedContentInline]

admin.site.register(Action, ActionAdmin)
