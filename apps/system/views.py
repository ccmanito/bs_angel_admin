#! /usr/bin/env python
#-*- coding:utf-8 -*-

from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework.request import Request
from .models import *
from login.common import get_parameter_dic
import time,json,requests,hashlib


class InterestDispose(APIView):
    '''
    兴趣爱好信息管理
    '''
    def get(self, request,format=None, *args, **kwargs):
        '''
        获取兴趣爱好列表信息
        '''
        params = get_parameter_dic(request)
        try:
            res = Interest.objects.filter().values()
        except Exception:
            result_data = {'code': 200,'msg':'success', 'data': {} }
        
        result_data = {'code': 200,'msg':'success', 'data': res }
        return Response(result_data)
    
    def post(self, request,format=None, *args, **kwargs):
        '''
        增加兴趣信息
        '''
        params = get_parameter_dic(request)
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)

    def put(self, request,format=None, *args, **kwargs):
        '''
        修改兴趣信息
        '''
        params = get_parameter_dic(request)
        Interest.objects.filter(id=id).update()
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)
    
    def delete(self, request,format=None, *args, **kwargs):
        '''
        删除兴趣爱好信息
        '''
        params = get_parameter_dic(request)
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)