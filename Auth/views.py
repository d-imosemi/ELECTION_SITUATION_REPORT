from django.shortcuts import redirect
from .forms import EditProfileForm, LoginForm, SignUpForm
from django.contrib.auth import logout 
from django.contrib import messages

from django.contrib.auth.views import PasswordChangeView, LoginView


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

	def dispatch(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			messages.warning(self.request, "Already logged In")
			return redirect('home')
		return super().dispatch(*args, **kwargs)



class UserLoginView(LoginView):
	form_class = LoginForm
	template_name = 'login.html'
	redirect_authenticated_user = True

	def get_success_url(self):
		messages.success(
			self.request, 'Logged In')
		return reverse_lazy("dashboard")

	def dispatch(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			messages.warning(self.request, "Already logged In")
			return redirect('home')
		return super().dispatch(*args, **kwargs)



def logout_request(request):
	logout(request)
	messages.info(request, "Logged Out.") 
	return redirect("home")
	



@method_decorator(login_required, name='dispatch')
class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'edit_setting.html'
    def get_success_url(self):
        messages.success(
            self.request, 'Profile Edited')
        return reverse_lazy("dashboard")

    
    def get_object(self):
        return self.request.user




@method_decorator(login_required, name='dispatch')
class PasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        messages.success(
            self.request, 'Password Changed')
        return reverse_lazy("dashboard")