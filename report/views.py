from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q


from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from report.models import *


# Create your views here.


def index(request):
    report = SituationReport.objects.filter(published=True)
    quote = DailyInspiration.objects.all()[0:1]
    header_title = HeaderTitle.objects.all()[0:1]
    candidate = Candidate.objects.all()[0:4]
    count =  SituationReport.objects.filter(published=True).count()
    users = User.objects.all().count()
    context = {
        'report': report,
        'quote' : quote,
        'header_title' : header_title,
        'candidate' : candidate,
        'count' : count,
        'users' : users,
    }
    return render(request, 'index.html', context)


class AllReports(ListView):
    model: SituationReport
    paginate_by = 20
    template_name = 'all_reports.html'

    def get_queryset(self):
        object_list = SituationReport.objects.filter(published=True)
        return object_list



@method_decorator(login_required, name='dispatch')
class AddVideo(CreateView):
    model = SituationReport
    fields = ('state', 'lga', 'ward', 'polling_unit', 'video', 'brief_description',)
    queryset: SituationReport.objects.filter(published=False)
    template_name = "dashboard.html"

    def get_success_url(self):
        messages.success(
            self.request, 'Video Uploaded, Wait for 10-30 mins for Approval')
        return reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user=self.request.user
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)



#SEARCH----VIEW
class SearchResultsView(ListView):
    model = SituationReport
    template_name = 'search_results.html'
   

    def get_queryset(self):
        post_filter = SituationReport.objects.filter(published=True)
        query = self.request.GET.get('q')
        if query:
            object_list = post_filter.filter(
                Q(state__icontains=query) | Q(lga__icontains=query) |
                Q(polling_unit__icontains=query) | Q(brief_description__icontains=query)
            )
        else:
            object_list = SituationReport.objects.filter(published=True)

        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = self.request.GET.get('q')
        return context
#SEARCH------VIEW------END