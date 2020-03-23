from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
import json
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import SignUpForm, LoginForm, UpdateProfile, SendMailForm
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from accounts.decorators import active_user_required
from .mixins import AictiveUserRequiredMixin, AictiveTeacherRequiredMixin, AictiveStudentRequiredMixin
from accounts.tokens import account_activation_token
from accounts.models import Teacher, Student
from course.models import AssignTeacher, Course
from session.models import Semester
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
            # user.user_profile.bio = signup_form.cleaned_data.get('bio')
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
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=user.username, password=raw_password)
            # login(request, user)
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
                elif request.user.is_staff:
                    return redirect('admin:login')
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

        semester_ids = Semester.objects.values_list('id', flat=True)
        teacher_courses_count_dict = {}
        for s_id in semester_ids:
            semester_obj = get_object_or_404(Semester, id=s_id)
            teacher_courses_count = AssignTeacher.objects.filter(
                teachers=teacher_obj, course__semester=semester_obj).count()
            semester_name = str(semester_obj.semester_full_name)

            teacher_courses_count_dict[semester_obj.semester_full_name] = {
                's_name': semester_obj.semester_full_name,
                'c_count': teacher_courses_count
            }

        context = {
            'title': 'Teacher Dashboard',
            'teacher_courses_count': teacher_courses_count,
            'teacher_courses_count_dict': json.dumps(teacher_courses_count_dict)
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


class Dashboard(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
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
        # bio = request.POST.get('bio')
        profile_image = request.FILES.get('profile_image')

        if first_name:
            request.user.first_name = first_name
        if last_name:
            request.user.last_name = last_name
        if phone_number:
            request.user.user_profile.phone_number = phone_number
        if address:
            request.user.user_profile.address = address
        # if bio:
        #     request.user.user_profile.bio = bio
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


class SendMail(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        to_id = kwargs.get('to')

        if request.user.user_profile.user_type == '1':
            teacher_obj = get_object_or_404(Teacher, teacher=to_id)
            to = teacher_obj.teacher.email
        elif request.user.user_profile.user_type == '0':
            student_obj = get_object_or_404(Student, student=to_id)
            to = student_obj.student.email

        data = {
            'mail_from': request.user.email,
            'mail_to': to
        }

        send_mail_form = SendMailForm(initial=data)

        context = {
            'title': 'Send Mail',
            'to_id': to_id,
            'send_mail_form': send_mail_form
        }

        return render(request, 'accounts/send_mail.html', context)

    def post(self, request, *args, **kwargs):
        to_id = kwargs.get('to')
        send_mail_form = SendMailForm(request.POST)

        if send_mail_form.is_valid():
            mail_from = send_mail_form.cleaned_data.get('mail_from')
            mail_to = send_mail_form.cleaned_data.get('mail_to')
            mail_subject = send_mail_form.cleaned_data.get('mail_subject')
            mail_message = send_mail_form.cleaned_data.get('mail_message')
            html_content = f'<p>From {mail_from}<br>To {mail_to}<br> Message: {mail_message}</p>'
            email = EmailMessage(
                mail_subject,
                html_content,
                mail_from,
                [mail_to],
            )
            email.content_subtype = "html"
            email.send()
            messages.success(request, ('Mail Send Successfully...'))
            return redirect('accounts:send_mail', to_id)
        else:
            context = {
                'title': 'Send Mail',
                'send_mail_form': send_mail_form
            }
            return render(request, 'accounts/send_mail.html', context)


class LogoutView(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, ('You Have Been Logged Out..'))
        return redirect('accounts:login')
