from django.contrib import admin
from .models import *


class SituationReportAdmin(admin.ModelAdmin):
    list_filter = ['user', 'state', 'created_on',]
    list_display = ['user', 'id', 'video', 'main', 'published', 'total_upvote', 'total_downvote', 'created_on',]
    actions = ['approve_video', 'add_to_main_page']

    def approve_video(self, request, queryset):
        queryset.update(published=True)

    
    def add_to_main_page(self, request, queryset):
        queryset.update(main=True)

admin.site.register(DailyInspiration)
admin.site.register(Candidate)
admin.site.register(SituationReport, SituationReportAdmin)
admin.site.register(HeaderTitle)
admin.site.register(ViewCount)
admin.site.register(State)
