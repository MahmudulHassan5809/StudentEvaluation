from django.urls import path


from . import views

app_name = "course"

urlpatterns = [
    path('student/course/select/', views.StudentCourseSelect.as_view(),
         name="student_course_select"),

    path('student/previous/course/', views.StudentPreviousCourse.as_view(),
         name="student_previous_course"),

    path('student/previous/course/<int:semester_id>',
         views.StudentPreviousCourse.as_view(), name="student_previous_course"),

    path('student/my-course/review/<int:id>',
         views.StudentCourseReview.as_view(), name="view_student_course_review"),



    path('teacher/courses/', views.TeacherCourses.as_view(), name="teacher_courses"),
    path('teacher/courses/<int:semester_id>',
         views.TeacherCourses.as_view(), name="teacher_courses"),
    path('teacher/course/details/<int:course_id>/<int:semester_id>',
         views.TeacherCourseDetails.as_view(), name="teacher_course_details"),

    path('evaluate/student/<int:student_id>/<int:course_id>/<int:semester_id>', views.StudentEvaluateByTeacher.as_view(),
         name="evaluate_student"),
    path('student/history/<int:student_id>/<int:course_id>/<int:semester_id>', views.StudentHistory.as_view(),
         name="student_history"),

]
