from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import SignUpForm,LoginForm
from django.utils.decorators import method_decorator
from accounts.decorators import active_user_required
from .mixins import AictiveUserRequiredMixin
from django.views import View


# Create your views here.
class RegisterView(View):
	def get(self,request,*args,**kwargs):
		form = SignUpForm()
		context = {
			'signup_form' : form,
			'title' : 'Register'
		}
		return render(request,'accounts/register.html',context)
	def post(self,request,*args,**kwargs):
		form = SignUpForm(request.POST)
		context = {
            'signup_form' : form,
			'title' : 'Register'
		}
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.user_profile.phone_number = form.cleaned_data.get('phone_number')
			user.user_profile.address = form.cleaned_data.get('address')
			user.user_profile.user_type = form.cleaned_data.get('user_type')
			user.user_profile.bio = form.cleaned_data.get('bio')
			user.save()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			#login(request, user)
			return redirect('accounts:login')
		else:
			return render(request,'accounts/register.html',context)


class LoginView(View):
	def get(self,request,*args,**kwargs):
		form = LoginForm()
		context = {
			'login_form' : form,
			'title' : 'Login'
		}
		return render(request,'accounts/login.html',context)

	@method_decorator(active_user_required())
	def post(self,request,*args,**kwargs):
		if form.is_valid():
			pass
		else:
			return render(request,'accounts/login.html',context)