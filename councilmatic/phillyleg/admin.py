from django.contrib.gis import admin
from django.db.models import Max
from phillyleg.models import *

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

class LocationAdmin (admin.GeoModelAdmin):
    model = MetaData_Location
    search_fields = ['address']

class TopicAdmin (admin.ModelAdmin):
    model = MetaData_Topic
    extra = 0
    ordering = ('topic',)

class CouncilDistrictInline(admin.TabularInline):
    model = CouncilDistrict
    extra = 0

class CouncilDistrictPlanAdmin (admin.GeoModelAdmin):
    inlines = [CouncilDistrictInline]

class CouncilMemberTenureInline (admin.TabularInline):
    model = CouncilMemberTenure
    extra = 1

class CouncilMemberAdmin (admin.ModelAdmin):
    inlines = [CouncilMemberTenureInline]
    list_display = ('name', 'tenure_begin')

    def queryset(self, request):
        qs = super(CouncilMemberAdmin, self).queryset(request)
        qs = qs.annotate(tenure_begin=Max('tenures__begin'))
        return qs

    def tenure_begin(self, instance):
        return instance.tenure_begin
    tenure_begin.short_description = 'Began tenure...'



admin.site.register(LegFile, LegFileAdmin)
admin.site.register(LegMinutes, LegMinutesAdmin)
admin.site.register(CouncilMember, CouncilMemberAdmin)
admin.site.register(MetaData_Word, WordAdmin)
admin.site.register(MetaData_Location, LocationAdmin)
admin.site.register(MetaData_Topic, TopicAdmin)
admin.site.register(LegFileMetaData)
admin.site.register(CouncilDistrict, admin.GeoModelAdmin)
admin.site.register(CouncilDistrictPlan, CouncilDistrictPlanAdmin)
