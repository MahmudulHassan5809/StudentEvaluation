
from django.urls import path, include
from . import views

app_name = 'boards'

urlpatterns = [
    path('', views.home, name='home'),

    path('boards/my-posts', views.MyPost.as_view(), name='my_posts'),

    path('boards/<int:pk>/', views.TopicListView.as_view(), name='board_topics'),

    path('boards/<int:pk>/new', views.new_topic, name='new_topic'),

    path('boards/<int:pk>/topics/<int:topic_pk>',
         views.PostListView.as_view(), name='topic_posts'),

    path('boards/<int:pk>/topics/<int:topic_pk>/reply',
         views.reply_topic, name='reply_topic'),

    path('boards/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit',
         views.PostUpdateView.as_view(), name='edit_post'),

    path('boards/posts/<int:post_pk>/delete',
         views.DeletePost.as_view(), name='delete_post'),
]
