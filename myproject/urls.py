#from django.contrib import admin
from baton.autodiscover import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),


    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('course/', include('course.urls', namespace='course')),
    path('forum/', include('boards.urls', namespace='boards')),
    path('quizes/', include('quizes.urls', namespace='quizes')),
    path('', include('pages.urls', namespace='pages')),

    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.FORCE_STATIC_FILE_SERVING and not settings.DEBUG:
  settings.DEBUG = True
  urlpatterns += static(settings.STATIC_URL,
                        document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
  settings.DEBUG = False


admin.site.site_header = "StudentEvaluation Admin"
admin.site.site_title = "StudentEvaluation Admin Portal"
admin.site.index_title = "Welcome to StudentEvaluation Researcher Portal"
