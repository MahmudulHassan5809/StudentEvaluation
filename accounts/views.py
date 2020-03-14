from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import SignUpForm, LoginForm, UpdateProfile
from pages.forms import WeatherCityForm
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
import requests
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from accounts.decorators import active_user_required
from .mixins import AictiveUserRequiredMixin, AictiveTeacherRequiredMixin, AictiveStudentRequiredMixin
from accounts.tokens import account_activation_token
from pages.models import City
from accounts.models import Teacher, Student
from course.models import AssignTeacher
from programs.models import Department, Faculty
from django.views import View


# Create your views here.
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        signup_form = SignUpForm()
        context = {
            'signup_form': signup_form,
            'title': 'Register'
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request, *args, **kwargs):
        signup_form = SignUpForm(request.POST)
        context = {
            'signup_form': signup_form,
            'title': 'Register'
        }
        if signup_form.is_valid():
            user = signup_form.save()
            user.refresh_from_db()
            user.user_profile.phone_number = signup_form.cleaned_data.get(
                'phone_number')
            user.user_profile.address = signup_form.cleaned_data.get('address')
            user.user_profile.user_type = signup_form.cleaned_data.get(
                'user_type')
            user.user_profile.bio = signup_form.cleaned_data.get('bio')
            user.save()
            if signup_form.cleaned_data.get('user_type') == '0':
                department_id = request.POST.get('department')
                department_obj = get_object_or_404(
                    Department, id=department_id)

                faculty_id = request.POST.get('faculty')
                faculty_obj = get_object_or_404(Faculty, id=faculty_id)

                Teacher.objects.create(
                    teacher=user, department=department_obj, faculty=faculty_obj)

            elif signup_form.cleaned_data.get('user_type') == '1':
                department_id = request.POST.get('department')
                department_obj = get_object_or_404(
                    Department, id=department_id)

                faculty_id = request.POST.get('faculty')
                faculty_obj = get_object_or_404(Faculty, id=faculty_id)

                Student.objects.create(
                    student=user, department=department_obj, faculty=faculty_obj)
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=user.username, password=raw_password)
            #login(request, user)
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.success(
                request, ('Registration Completed.Please Confirm Your Email Address'))
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.user_profile.email_confirmed = True
        user.user_profile.save()
        messages.success(
            request, ('Thank You For Confirm The Email.Your Account Will Be Activated Soon'))
        return redirect('accounts:login')
    else:
        messages.success(request, ('Activation link is invalid!'))
        return redirect('accounts:login')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {
            'login_form': form,
            'title': 'Login'
        }
        return render(request, 'accounts/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        context = {
            'login_form': form,
            'title': 'Login'
        }
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

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
            return render(request, 'accounts/login.html', context)


class TeacherDashboard(AictiveTeacherRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        teacher_obj = get_object_or_404(Teacher, teacher=request.user.id)
        teacher_courses_count = request.user.user_teacher.teacher_courses.filter(
            teachers=teacher_obj).count()
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
        city = 'Las Vegas'

        cities = request.user.user_weather.all()
        print(cities)

        weather_data = []

        for city in cities:
            r = requests.get(url.format(city)).json()

            city_weather = {
                'city': city,
                'temperature': r["main"]["temp"],
                'feels_like': r["main"]["feels_like"],
                'temp_min': r["main"]["temp_min"],
                'temp_max': r["main"]["temp_max"],
                'pressure': r["main"]["pressure"],
                'humidity': r["main"]["humidity"],
                'description': r["weather"][0]["description"],
                'icon': r["weather"][0]["icon"],
            }
            weather_data.append(city_weather)

        weather_city_form = WeatherCityForm()
        context = {
            'title': 'Teacher Dashboard',
            'teacher_courses_count': teacher_courses_count,
            'weather_city_form': weather_city_form,
            'weather_data': weather_data
        }
        return render(request, 'accounts/teacher/teacher_dashboard.html', context)


class StudentDashboard(AictiveStudentRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Student Dashboard'
        }
        return render(request, 'accounts/student/student_dashboard.html', context)


class WeatherCity(AictiveUserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        weather_city_form = WeatherCityForm(request.POST)
        if weather_city_form.is_valid():
            save_form = weather_city_form.save(commit=False)
            save_form.owner = request.user
            save_form.save()
            if request.user.user_profile.user_type == '0':
                return redirect('accounts:teacher_dashboard')
            elif request.user.user_profile.user_type == '1':
                return redirect('accounts:student_dashboard')
        else:
            if request.user.user_profile.user_type == '0':
                return redirect('accounts:teacher_dashboard')
            elif request.user.user_profile.user_type == '1':
                return redirect('accounts:student_dashboard')


class MyProfile(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        update_profile_form = UpdateProfile(request=request)
        context = {
            'title': 'My Profile',
            'update_profile_form': update_profile_form

        }
        return render(request, 'accounts/my_profile.html', context)

    def post(self, request, *args, **kwargs):

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        bio = request.POST.get('bio')
        profile_image = request.FILES.get('profile_image')

        if first_name:
            request.user.first_name = first_name
        if last_name:
            request.user.last_name = last_name
        if phone_number:
            request.user.user_profile.phone_number = phone_number
        if address:
            request.user.user_profile.address = address
        if bio:
            request.user.user_profile.bio = bio
        if profile_image:
            request.user.user_profile.profile_pic = profile_image

        request.user.save()
        request.user.user_profile.save()

        messages.success(request, "Profile Updated Successfully")
        return redirect('accounts:my_profile')


class ChangePassword(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        chanage_password_form = PasswordChangeForm(user=request.user)
        context = {
            'chanage_password_form': chanage_password_form
        }
        return render(request, 'accounts/change_password.html', {'chanage_password_form': chanage_password_form})

    def post(self, request, *args, **kwargs):
        chanage_password_form = PasswordChangeForm(
            data=request.POST, user=request.user)
        context = {
            'chanage_password_form': chanage_password_form
        }
        if chanage_password_form.is_valid():
            chanage_password_form.save()
            update_session_auth_hash(request, chanage_password_form.user)
            messages.success(request, ('You have Changed Your Password...'))
            return redirect('accounts:change_password')
        else:
            return render(request, 'accounts/change_password.html', {'chanage_password_form': chanage_password_form})


class LogoutView(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, ('You Have Been Logged Out..'))
        return redirect('accounts:login')
