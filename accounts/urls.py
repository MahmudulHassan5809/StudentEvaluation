from django.urls import path


from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('my-profile/', views.MyProfile.as_view(), name="my_profile"),
    path('chanage-password/', views.ChangePassword.as_view(),
         name="change_password"),
    path('add/weather-city/', views.WeatherCity.as_view(), name="weather_city"),



    path('student/dashboard/', views.StudentDashboard.as_view(),
         name="student_dashboard"),


    path('activate/<uidb64>/<token>', views.activate, name='activate'),


    path('teacher/dashboard/', views.TeacherDashboard.as_view(),
         name="teacher_dashboard"),


    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),


    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('send-mail/<int:to>/', views.SendMail.as_view(), name='send_mail'),
]
