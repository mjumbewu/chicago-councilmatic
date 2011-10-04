from django.contrib import admin
from subscriptions import models

#class KeywordInline(admin.StackedInline):
#    model = KeywordSubscription
#    extra = 3

#class CouncilmemberInline(admin.StackedInline):
#    model = CouncilMemberSubscription
#    extra = 3

#class SubscriptionAdmin(admin.ModelAdmin):
#    inlines = [KeywordInline, CouncilmemberInline]

#class LegActionInline(admin.StackedInline):
#    model = LegAction
#    extra = 1

#class LegFileAttachmentInline(admin.StackedInline):
#    model = LegFileAttachment
#    extra = 1

#class LegFileAdmin(admin.ModelAdmin):
#    inlines = [LegActionInline, LegFileAttachmentInline]

#class LegMinutesAdmin(admin.ModelAdmin):
#    inlines = [LegActionInline]


admin.site.register(models.Subscription)
admin.site.register(models.Subscriber)
admin.site.register(models.ContentFeedRecord)

#admin.site.register(models.SearchSubscription)
#admin.site.register(models.EmailChannel)
#admin.site.register(models.RssChannel)
#admin.site.register(models.SmsChannel)
