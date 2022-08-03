from django.shortcuts import get_object_or_404
from .models import *

def header_context(request):
    return {
        'quote': DailyInspiration.objects.all()[0:1],
        'count' : SituationReport.objects.filter(published=True).count(),
        'users' : User.objects.all().count(),
        'header_title': HeaderTitle.objects.all()[0:1],
        'candidate' : Candidate.objects.all()[0:4],
        'vid_state' : SituationReport.objects.filter(published=True),
    }
