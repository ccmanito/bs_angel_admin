# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
    url(r'user/login',LoginInfo.as_view()),
)