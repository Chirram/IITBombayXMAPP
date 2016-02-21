"""IITBxReportsProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from logger import views
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^faculty/',include('faculty.urls')),
    url(r'^$','logger.views.login_user'),
    url(r'^logout/$','logger.views.logout_user',name='getout'),
    url(r'^adminpanel/', include('adminpanel.urls')),
    url(r'^generalinformation/',include('socialreports.urls')),
    
    url(r'^student/',include('student.urls')),
    url(r'^ceopanel/',include('ceopanel.urls')),
   # url(r'^ceopanel/',include('ceopanel.urls')),
]
