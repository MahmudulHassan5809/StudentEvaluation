from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import SignUpForm,LoginForm
from django.utils.decorators import method_decorator
from accounts.decorators import active_user_required
from .mixins import AictiveUserRequiredMixin,AictiveTeacherRequiredMixin,AictiveStudentRequiredMixin
from accounts.models import Teacher,Student
from programs.models import Department,Faculty
from django.views import View


# Create your views here.
class RegisterView(View):
	def get(self,request,*args,**kwargs):
		signup_form = SignUpForm()
		context = {
			'signup_form' : signup_form,
			'title' : 'Register'
		}
		return render(request,'accounts/register.html',context)
	def post(self,request,*args,**kwargs):
		signup_form = SignUpForm(request.POST)
		context = {
            'signup_form' : signup_form,
			'title' : 'Register'
		}
		if signup_form.is_valid():
			user = signup_form.save()
			user.refresh_from_db()
			user.user_profile.phone_number = signup_form.cleaned_data.get('phone_number')
			user.user_profile.address = signup_form.cleaned_data.get('address')
			user.user_profile.user_type = signup_form.cleaned_data.get('user_type')
			user.user_profile.bio = signup_form.cleaned_data.get('bio')
			user.save()
			if signup_form.cleaned_data.get('user_type') == '0':
				department_id = request.POST.get('department')
				department_obj = get_object_or_404(Department,id=department_id)
				
				faculty_id = request.POST.get('faculty')
				faculty_obj = get_object_or_404(Faculty,id=faculty_id)
				
				Teacher.objects.create(teacher=user,department=department_obj,faculty=faculty_obj)
			
			elif signup_form.cleaned_data.get('user_type') == '1':
				department_id = request.POST.get('department')
				department_obj = get_object_or_404(Department,id=department_id)
				
				faculty_id = request.POST.get('faculty')
				faculty_obj = get_object_or_404(Faculty,id=faculty_id)
				
				Student.objects.create(student=user,department=department_obj,faculty=faculty_obj)
			#raw_password = form.cleaned_data.get('password1')
			#user = authenticate(username=user.username, password=raw_password)
			#login(request, user)
			messages.success(request, ('Registration Completed.Please Login'))
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

	
	def post(self,request,*args,**kwargs):
		form = LoginForm(request.POST)
		context = {
			'login_form' : form,
			'title' : 'Login'
		}
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			if username != '' and password != '':
				user = authenticate(request, username=username, password=password)
				if user is not None:
					login(request, user)
					if user.user_profile.user_type == '0':
						return redirect('accounts:teacher_dashboard')
					elif user.user_profile.user_type == '1':
						return redirect('accounts:student_dashboard')
				else:
					messages.error(request, ('Invalid Credentials'))
					return redirect('accounts:login')
			else:
				messages.error(request, ('Please Input All The Fields'))
				return redirect('accounts:login')
		else:
			return render(request,'accounts/login.html',context)



class TeacherDashboard(AictiveTeacherRequiredMixin,View):
	def get(self,request,*args,**kwargs):
		context = {
			'title' : 'Teacher Dashboard'
		}
		return render(request,'accounts/teacher/teacher_dashboard.html',context)



class StudentDashboard(AictiveStudentRequiredMixin,View):
	def get(self,request,*args,**kwargs):
		context = {
			'title' : 'Student Dashboard'
		}
		return render(request,'accounts/teacher/student_dashboard.html',context)