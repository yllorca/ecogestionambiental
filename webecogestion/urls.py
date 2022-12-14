"""webecogestion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import allauth
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^admin/', admin.site.urls),
    path('panel/',  include('apps.panel.urls', namespace='panel')),
    path('', include('apps.home.urls', namespace='home')),
    path('accounts/', include('allauth.urls')),
    path('accounts/login/', allauth.account.views.LoginView, name='account_login'),
    path('tinymce/', include('tinymce.urls')),

    # url(r'^', include('apps.home.urls', namespace='home')),
    # url(r'^panel/', include('apps.panel.urls', namespace='panel')),
    # url(r'^accounts/', include('allauth.urls')),
    #
    # url(r'^accounts/login/', allauth.account.views.LoginView, name='account_login'),
    #
    # url(r'^tinymce/', include('tinymce.urls')),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG == False:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
    ]

admin.site.site_header = 'Ecogestion Ambiental Ltda'
