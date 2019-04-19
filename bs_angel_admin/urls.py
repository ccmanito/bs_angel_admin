#-*- coding:utf-8 -*-
"""hodor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include,re_path
from login import urls as login_urls
from system import urls as system_urls
from login.views import GetQuniu
urlpatterns = [
    path(r'user/', include(login_urls)),
    path(r'sys/', include(system_urls)),
    path(r'qiniu/token', GetQuniu.as_view()),
]
