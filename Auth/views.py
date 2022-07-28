from django.shortcuts import redirect
from .forms import EditProfileForm, SignUpForm
from django.contrib.auth import logout 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.views import PasswordChangeView, LoginView


from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic



class UserRegisterView(generic.CreateView):
	form_class = SignUpForm
	template_name = 'register.html'
	redirect_authenticated_user = True
	def get_success_url(self):
		messages.success(
			self.request, 'Registered Successfully')
		return reverse_lazy("login")



class UserLoginView(LoginView):
	template_name = 'login.html'
	redirect_authenticated_user = True

	def get_success_url(self):
		messages.success(
			self.request, 'Logged in Successfully')
		return reverse_lazy("dashboard")




def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")



@method_decorator(login_required, name='dispatch')
class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'edit_setting.html'
    def get_success_url(self):
        messages.success(
            self.request, 'Profile Edited Successfully')
        return reverse_lazy("dashboard")

    
    def get_object(self):
        return self.request.user




@method_decorator(login_required, name='dispatch')
class PasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        messages.success(
            self.request, 'Password changed Successfully')
        return reverse_lazy("dashboard")