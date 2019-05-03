#! /usr/bin/env python
#-*- coding:utf-8 -*-

from django.urls import path,re_path
from worker import views

urlpatterns = [
        path(u'creation', views.WorkCreate.as_view(), name='工单创建'),
        path(u'result', views.KmeansModel.as_view(), name='分配算法调用'),
]