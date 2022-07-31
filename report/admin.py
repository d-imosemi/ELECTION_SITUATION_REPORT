from django.contrib import admin
from .models import *


class SituationReportAdmin(admin.ModelAdmin):
    list_filter = ['user', 'state', 'created_on',]
    list_display = ['user', 'video', 'published', 'total_downvote', 'created_on']


admin.site.register(DailyInspiration)
admin.site.register(Candidate)
admin.site.register(SituationReport, SituationReportAdmin)
admin.site.register(HeaderTitle)