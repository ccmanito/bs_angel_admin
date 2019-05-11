#! /usr/bin/env python
#-*- coding:utf-8 -*-

from django.urls import path,re_path
from system import views

urlpatterns = [
        path(u'school/info', views.SchoolDetail.as_view(), name='学校信息管理'),
        path(u'dorm/info', views.DormDetail.as_view(), name='宿舍信息管理'),
        path(u'dorm/detail', views.InfoDetail.as_view(), name='宿舍信息获取'),
        path(u'user/list', views.UserList.as_view(), name='用户信息管理'),
]