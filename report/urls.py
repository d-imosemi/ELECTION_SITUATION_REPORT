from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='home'),
    path('dashboard', AddVideo.as_view(), name='dashboard'),
    path('search/', SearchResultsView.as_view(), name='search_results'),

    path('reports', AllReports.as_view(), name='reports')

]
