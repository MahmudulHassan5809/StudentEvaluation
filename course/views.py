from django.shortcuts import render, redirect, get_object_or_404
from accounts.mixins import AictiveUserRequiredMixin, AictiveTeacherRequiredMixin, AictiveStudentRequiredMixin
from course.forms import CourseChoiceForm
from course.models import StudentCourse
from accounts.models import Teacher, Student
from django.contrib.auth.models import User
from session.models import Semester
from django.views import View
# Create your views here.


class TeacherCourses(AictiveTeacherRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        teacher = get_object_or_404(Teacher, teacher=request.user.id)
        teacher_courses = request.user.user_teacher.teacher_courses.filter(
            teacher=teacher)

        context = {
            'title': 'My Courses',
            'teacher_courses': teacher_courses
        }
        return render(request, 'accounts/teacher/teacher_courses.html', context)


class StudentCourseSelect(AictiveStudentRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        course_select_form = CourseChoiceForm()
        active_semester = Semester.objects.filter(active=True).first()
        student_obj = get_object_or_404(Student, student=request.user.id)
        my_courses = student_obj.student_course.filter(
            student=student_obj).first()

        context = {
            'title': 'Select Course',
            'course_select_form': course_select_form,
            'active_semester': active_semester,
            'my_courses': my_courses
        }
        return render(request, 'accounts/student/course_select.html', context)

    def post(self, request, *args, **kwargs):
        course_select_form = CourseChoiceForm(request.POST)
        active_semester = Semester.objects.filter(active=True).first()
        student_obj = get_object_or_404(Student, student=request.user.id)
        my_courses = student_obj.student_course.filter(
            student=student_obj).first()

        context = {
            'title': 'Select Course',
            'course_select_form': course_select_form,
            'active_semester': active_semester,
            'my_courses': my_courses
        }
        if course_select_form.is_valid():
            student_course_allready_created = StudentCourse.objects.filter(
                student=student_obj).first()
            if student_course_allready_created:
                for course_id in request.POST.getlist('courses'):
                    student_course_allready_created.courses.add(int(course_id))
            else:
                student_course = StudentCourse.objects.create(
                    student=student_obj)
                for course_id in request.POST.getlist('courses'):
                    student_course.courses.add(int(course_id))

            return redirect('course:student_course_select')
        else:
            return render(request, 'accounts/student/course_select.html', context)
