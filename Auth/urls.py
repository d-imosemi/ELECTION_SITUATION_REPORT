from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("register/", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),

    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),

    path('password/', PasswordChangeView.as_view(),
        name='password_change'
    ),

]
