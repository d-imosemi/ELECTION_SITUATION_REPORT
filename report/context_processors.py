from .models import *

def header_context(request):
    return {
        'quote': DailyInspiration.objects.all()[0:1],
        'count' : SituationReport.objects.filter(published=True).count(),
        'users' : User.objects.all().count(),
        'header_title': HeaderTitle.objects.all()[0:1]

    }