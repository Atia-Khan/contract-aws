# Import necessary modules
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.staticfiles import views
# Import external packages
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

# Import my packages
from .views import  CustomTokenObtainPairView

# Define URL patterns for authentication using djoser and social authentication
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),
    path('admin/', admin.site.urls),
    path('', include('folder.urls', namespace='main')),
    path('folder/', include('folder.urls', namespace='folder')),
    path('file/', include('file.urls', namespace='file')),
# urls.py
    path('api/token/', CustomTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += [
        re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
        re_path(r'^static/(?P<path>.*)$', views.serve),
        re_path(r'^(?P<path>.*)$', views.serve),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
 # add at the last
# urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


