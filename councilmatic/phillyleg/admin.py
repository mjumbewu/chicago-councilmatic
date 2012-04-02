from django.contrib.gis import admin
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

class LegActionInline(admin.StackedInline):
    model = LegAction
    extra = 1

class LegFileAttachmentInline(admin.StackedInline):
    model = LegFileAttachment
    extra = 1

class LegFileAdmin(admin.ModelAdmin):
    inlines = [LegActionInline, LegFileAttachmentInline]

class LegMinutesAdmin(admin.ModelAdmin):
    inlines = [LegActionInline]

class LegFileInline (admin.TabularInline):
    model = LegFile
    fields = ['id', 'title']
    extra = 1

class LegFileWordInline(admin.TabularInline):
    model = LegFileMetaData.words.through
    extra = 1

class WordAdmin (admin.ModelAdmin):
    model = MetaData_Word
    inlines = [LegFileWordInline]

class LegFileLocationInline(admin.TabularInline):
    model = LegFileMetaData.locations.through
    extra = 1

class LocationAdmin (admin.GeoModelAdmin):
    model = MetaData_Location
    inlines = [LegFileLocationInline]


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(LegFile, LegFileAdmin)
admin.site.register(LegMinutes, LegMinutesAdmin)
admin.site.register(CouncilMember)
admin.site.register(MetaData_Word, WordAdmin)
admin.site.register(MetaData_Location, LocationAdmin)
admin.site.register(LegFileMetaData)
