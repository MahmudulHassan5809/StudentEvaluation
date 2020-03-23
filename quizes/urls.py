from django.urls import path


from . import views

app_name = "quizes"

urlpatterns = [
    path('', views.QuizeBoard.as_view(), name="quize_board"),
    path('start-exam/<str:topic_name>/<int:topic_id>/',
         views.StartExam.as_view(), name="start_exam"),
    path('view-answer/<str:topic_name>/<int:topic_id>/',
         views.ViewAnswer.as_view(), name="view_answer"),

    path('re-try',
         views.ReTry.as_view(), name="re_try"),

]
