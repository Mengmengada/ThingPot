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
import json
#If there is a url without a $(end note), no matter what string after is, it will go to this url
#This can be used to return a fixed template whatever the attacker send.
# with open('api/template.json') as data:
#     d = json.loads(data.read())
# username=[]
# for name in d["config"]["whitelist"]:
#     username=name
# print username
# username = "15A1OA1gfdeyUEvPNxa54pW1J07-yQEntEkPkEGd"
urlpatterns = [
    # url(r'executetest', views.ExecuteTest.as_view()),
    # url(r'add', views.AddObject.as_view()),
    # url(r'testlist', views.TestList.as_view()),
    url(r'api$', views.CreatUsers.as_view()), #to create user and return the username
    url(r'^api/[\s\S]{40}$', views.GetAllInfo.as_view()),
    # url(r'^api/[\s\S]{40}/lights/2/state', views.SetLight2.as_view()),
    url(r'^api/[\s\S]{40}/lights/(?P<light_id>[0-9]{0,3})/state', views.SetLight.as_view()),
    url(r'^api/[\s\S]{40}/lights/(?P<light_id>[0-9]{0,3})$', views.GetLight.as_view()),
    # url(r'^api/[\s\S]{40}/lights/1$', views.GetLight1.as_view()),
    # url(r'^api/[\s\S]{40}/lights/2$', views.GetLight2.as_view()),
    # url(r'^api/[\s\S]{40}/lights$', views.GetLights.as_view()),
    # url(r'^api/[\s\S]{40}/config$', views.GetConfig.as_view()),
    url(r'^api/[\s\S]{40}/(?P<key>.*)$', views.GetSubInfo.as_view()),
    url(r'^api/[\s\S]{40}/config/whitelist/[\s\S]{40}$', views.DelUsr.as_view()),
    # url(r'^api/[\s\S]{40}/config/name$', views.SetConfigName.as_view()),
    # url(r'^api/'+username[0], views.GetAllInfo.as_view()),
    # url(r'^api/'+username[0]+'/lights/2/state', views.SetLight2.as_view()),
    # url(r'^api/'+username[0]+'/lights/1/state', views.SetLight1.as_view()),

]
