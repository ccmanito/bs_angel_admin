#! /usr/bin/env python
#-*- coding:utf-8 -*-

from django.urls import path,re_path
from login import views

urlpatterns = [
        path(u'login', views.LoginAuth.as_view(), name='用户登陆'),
        path(u'info', views.LoginInfo.as_view(), name='获取用户信息'),
        path(u'logout', views.LoginOut.as_view(), name='用户登出'),
        path(u'regedit', views.Regedit.as_view(), name='用户注册'),
        path(u'isuser', views.Regedit.as_view(), name='判断用户是否存在'),
        path(u'github_check', views.GithubCheck.as_view(), name='github第三方登录'),
        path(r'github', views.github, name='github'),
        path(r'bind', views.BindAccount, name='第三方登录站内绑定接口'),
        path(r'bind/skip', views.BindAccount2, name='第三方登录跳过直接登录接口'),
        path(u'syncavatar', views.Syncavatar.as_view(), name='同步用户头像'),
]