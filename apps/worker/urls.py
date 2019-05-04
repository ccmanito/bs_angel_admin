#! /usr/bin/env python
#-*- coding:utf-8 -*-

from django.urls import path,re_path
from worker import views

urlpatterns = [
        path(u'info', views.WorkerInfo.as_view(), name='工单info'),
        path(u'result', views.KmeansModel.as_view(), name='分配算法调用'),
        path(u'test', views.Test.as_view(), name='测试'),
]