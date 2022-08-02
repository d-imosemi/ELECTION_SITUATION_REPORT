from ipaddress import ip_address
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse

from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string

from report.models import *


# Create your views here.

def index(request):
    report = SituationReport.objects.filter(published=True)[0:6]
    quote = DailyInspiration.objects.all()[0:1]
    header_title = HeaderTitle.objects.all()[0:1]
    candidate = Candidate.objects.all()[0:4]
    count =  SituationReport.objects.filter(published=True).count()
    users = User.objects.all().count()
    states = State.objects.all()


    context = {
        'report': report,
        'quote' : quote,
        'header_title' : header_title,
        'candidate' : candidate,
        'count' : count,
        'users' : users,
        'states': states,
          
    }
    return render(request, 'index.html', context)





def StateView(request, pk):
    state = State.objects.get(id=pk)
    state_count = State.objects.filter(id=pk).count()

    context = {
        'state': state,
        'state_count': state_count,
    }
    return render(request, 'state_view.html', context)




class AllReports(ListView):
    model: SituationReport
    paginate_by = 20
    template_name = 'all_reports.html'

    def get_queryset(self):
        object_list = SituationReport.objects.filter(published=True)
        return object_list



def ReportDetail(request, pk):
    template_name = 'report_detail.html'
    report = get_object_or_404(SituationReport, pk=pk, published=True)
    
    
    ip = request.META['REMOTE_ADDR']
    if not ViewCount.objects.filter(video=report, session=request.session.session_key):
        view = ViewCount(video=report, ip_address=ip, session=request.session.session_key)
        view.save()
    video_views = ViewCount.objects.filter(video=report).count()


    is_liked = False
    if report.likes.filter(id=request.user.id).exists():
       is_liked = True
    if report.total_downvote() > 1000:
        report.delete()
        return redirect('home')
    return render(
        request,
        template_name,
        {
            'report': report,
            'is_liked': is_liked,
            'total_likes': report.total_downvote(),
            'view_count' : video_views
        }
    )



@method_decorator(login_required, name='dispatch')
class AddVideo(CreateView):
    model = SituationReport
    fields = ('title', 'state', 'lga', 'ward', 'polling_unit', 'video', 'brief_description',)
    queryset: SituationReport.objects.filter(published=False)
    template_name = "dashboard.html"

    def get_success_url(self):
        messages.success(
            self.request, 'Video Uploaded, Wait for 10-30 mins for Approval')
        return reverse_lazy("home")
    
    def get_context_data(self, *args, **kwargs):
        user_video = SituationReport.objects.filter(user=self.request.user)
        context = super().get_context_data(*args, **kwargs)
        context['user_video'] = user_video
        return context

    def form_valid(self, form):
        form.instance.user=self.request.user
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)



@login_required
def LikeView(request, pk):
    post = get_object_or_404(SituationReport, id=request.POST.get('post_id'))

    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('report_detail', args=[str(pk)]))

# @login_required
# def LikeView(request):

#     post = get_object_or_404(SituationReport, id=request.POST.get('id'))    
#     is_liked = False
#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user)
#         is_liked = False
       
#     else:
#         post.likes.add(request.user)
#         is_liked = True
        
#     context = {
#         'post': post,
#         'is_liked': is_liked,
#         'total_likes': post.total_likes(),
#     }
#     if request.is_ajax():
#         html = render_to_string('like_section.html', context, request=request)
#         return JsonResponse({'form': html})





#SEARCH----VIEW
class SearchResultsView(ListView):
    model = SituationReport
    template_name = 'search_results.html'
   

    def get_queryset(self):
        post_filter = SituationReport.objects.filter(published=True)
        query = self.request.GET.get('q')
        if query:
            object_list = post_filter.filter(
                Q(title__icontains=query) | Q(lga__icontains=query) |
                Q(polling_unit__icontains=query) | Q(state__name__icontains=query)
            )
        else:
            object_list = SituationReport.objects.filter(published=True)

        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = self.request.GET.get('q')
        return context
#SEARCH------VIEW------END