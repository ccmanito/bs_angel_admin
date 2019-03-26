# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
    url(r'user/login',LoginAuth.as_view()),
    url(r'user/info',LoginInfo.as_view()),
    url(r'user/logout',LoginOut.as_view()),
    url(r'user/regedit',Regedit.as_view()),
    url(r'user/isuser',Regedit.as_view()),
    url(r'user/github_check', GithubCheck.as_view()),
    url(r'user/github', github, name='github'),
)
