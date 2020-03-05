from django.urls import path


from . import views

app_name = "course"

urlpatterns = [
    path('student/course/select/', views.StudentCourseSelect.as_view(),
         name="student_course_select"),
    path('student/previous/course/', views.StudentPreviousCourse.as_view(),
         name="student_previous_course"),

    path('teacher/courses/', views.TeacherCourses.as_view(), name="teacher_courses"),
]
