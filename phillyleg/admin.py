from django.contrib import admin
from phillyleg.models import Subscription
from phillyleg.models import *

class KeywordInline(admin.StackedInline):
    model = KeywordSubscription
    extra = 3

class CouncilmemberInline(admin.StackedInline):
    model = CouncilMemberSubscription
    extra = 3

class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [KeywordInline, CouncilmemberInline]    


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(LegFile)
admin.site.register(CouncilMember)
