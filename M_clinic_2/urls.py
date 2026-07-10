"""
URL configuration for M_clinic_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import sys

from django.contrib import admin
from django.conf import settings
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('internal/', include('clinic.portal_urls')),
    path('', include('clinic.urls')),
]

# django.conf.urls.static.static() returns no patterns when DEBUG=False.
# Serve assets during local runserver anyway so portal/public CSS both work.
if settings.DEBUG or 'runserver' in sys.argv:
    static_root = settings.STATICFILES_DIRS[0]
    static_url = settings.STATIC_URL.lstrip('/')
    urlpatterns += [
        re_path(
            rf'^{static_url}(?P<path>.*)$',
            serve,
            {'document_root': static_root},
        ),
    ]
    media_url = settings.MEDIA_URL.lstrip('/')
    urlpatterns += [
        re_path(
            rf'^{media_url}(?P<path>.*)$',
            serve,
            {'document_root': settings.MEDIA_ROOT},
        ),
    ]
