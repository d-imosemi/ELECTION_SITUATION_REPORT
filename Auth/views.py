from django.shortcuts import render, redirect
from .forms import EditProfileForm, NewUserForm
from django.contrib.auth import login, authenticate, logout 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.views import PasswordChangeView


from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic



def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("main:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})



def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			user = authenticate(femail=email, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {email}.")
				return redirect("main:homepage")
			else:
				messages.error(request,"Invalid email or password.")
		else:
			messages.error(request,"Invalid email or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("main:homepage")



@method_decorator(login_required, name='dispatch')
class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_setting.html'
    def get_success_url(self):
        messages.success(
            self.request, 'Profile Edited Successfully')
        return reverse_lazy("dashboard")

    
    def get_object(self):
        return self.request.user




@method_decorator(login_required, name='dispatch')
class PasswordChangeView(PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        messages.success(
            self.request, 'Password changed Successfully')
        return reverse_lazy("dashboard")