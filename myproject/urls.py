from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('course/', include('course.urls', namespace='course')),
    path('', include('pages.urls', namespace='pages')),

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
