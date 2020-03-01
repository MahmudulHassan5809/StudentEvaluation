from django.urls import path


from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
	
	
    path('student/dashboard/', views.StudentDashboard.as_view(), name="student_dashboard"),

	path('activate/<uidb64>/<token>',views.activate, name='activate'),


	path('teacher/dashboard/', views.TeacherDashboard.as_view(), name="teacher_dashboard"),
	path('teacher/courses/', views.TeacherCourses.as_view(), name="teacher_courses"),


	path('logout/',views.LogoutView.as_view(), name='logout'),
]