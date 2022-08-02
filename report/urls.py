from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='home'),
    path('dashboard/', AddVideo.as_view(), name='dashboard'),
    path('search/', SearchResultsView.as_view(), name='search_results'),

    path('reports/', AllReports.as_view(), name='reports'),

    path('report/detail/<int:pk>/', ReportDetail, name='report_detail'),

    path('state/view/<int:pk>/', StateView, name='state_view'),

    path('reporter/Profile/<int:pk>/', UserProfile, name='user_videos'),


    path('like_post/<int:pk>/', LikeView, name='like_post'),

]
