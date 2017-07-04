"""manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url
from . import views
import logging

logger = logging.getLogger(__name__)
urlpatterns = [
    url(r'hue[\s\S]{0,40}$', views.GetInfo.as_view()),  # to get some info
    url(r'Philips[\s\S]{0,40}$', views.GetInfo.as_view()),  # to get some info
    url(r'api[^/;]{1,40}$', views.GetInfo.as_view()), # to create user and return the username
    url(r'^api/[^/;]{6}$', views.GetSimpConfig.as_view()),  # TO first get all the requests,
    url(r'^api/[^/;]{7,40}$', views.GetAllInfo.as_view()),  # TO first get all the requests,
    url(r'^api/[^/;]{0,5}$', views.GetAllInfo.as_view()),  # TO first get all the requests,
    url(r'^api/[\s\S]{0,40}/lights/(?P<light_id>[0-9]{0,3})/state', views.SetLight.as_view()),
    url(r'^api/[\s\S]{0,40}/lights/(?P<light_id>[0-9]{0,3})$', views.GetLight.as_view()),
    url(r'^api/[\s\S]{0,40}/(?P<key>.*)/$', views.GetSubInfo.as_view()),
    url(r'^api/[\s\S]{0,40}/config/whitelist/[\s\S]{40}$', views.DelUsr.as_view()),
    url(r'^api/[\s\S]{0, 40}/config/whitelist$', views.GetUsr.as_view()),

]
