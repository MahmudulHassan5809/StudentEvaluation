from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
import json

class AictiveUserRequiredMixin:
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated and request.user.user_profile.active:
			return super().dispatch(request, *args, **kwargs)
		else:
			messages.error(request, ('Please Login Or May Be Your Account Is Not Active'))
			return redirect('accounts:login')



class AictiveTeacherRequiredMixin:
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated and request.user.user_profile.active and request.user.user_profile.user_type=='0':
			return super().dispatch(request, *args, **kwargs)
		else:
			messages.error(request, ('Sorry You Are Not Teacher'))
			return redirect('accounts:login')



class AictiveStudentRequiredMixin:
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated and request.user.user_profile.active and request.user.user_profile.user_type=='1':
			return super().dispatch(request, *args, **kwargs)
		else:
			messages.error(request, ('Sorry You Are Not Student'))
			return redirect('accounts:login')