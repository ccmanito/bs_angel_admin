#! /usr/bin/env python
#-*- coding:utf-8 -*-

from django.urls import path,re_path
from system import views

urlpatterns = [
        path(u'interest', views.InterestDispose.as_view(), name='兴趣爱好信息管理'),
]