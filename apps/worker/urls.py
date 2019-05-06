#! /usr/bin/env python
#-*- coding:utf-8 -*-

from django.urls import path,re_path
from worker import views

urlpatterns = [
        path(u'info', views.WorkerInfo.as_view(), name='工单info'),
        path(r'detail',views.WorkerDetail.as_view(), name='工单详情'),
        path(u'perfrom/kemans', views.KmeansModel.as_view(), name='分配算法调用'),
        path(u'test', views.Test.as_view(), name='测试'),
        path(r'auth',views.AuthWorker.as_view(), name='Auth流程接口'),
]