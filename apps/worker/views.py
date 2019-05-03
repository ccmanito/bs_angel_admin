from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework.request import Request
from .models import *
from .controller import *
from .tasks import regularly
from login.common import get_parameter_dic
import time,json,requests,hashlib


class WorkCreate(APIView):
    '''
    工单接口
    '''
    def get(self, request, format=None, *args, **kwargs):
        '''
        工单获取，根据权限显示工单列表
        '''
        params = get_parameter_dic(request)
        
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)

    def post(self, request, format=None, *args, **kwargs):
        '''
        工单录入
        '''
        params = get_parameter_dic(request)
        
        timestr = format_time(params['endtime'])
        regularly(timestr, ['e'])
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)

class KmeansModel(APIView):
    '''
    k-means 算法调用
    '''
    def get(self, request,format=None, *args, **kwargs):
        '''
        get方法
        '''
        params = get_parameter_dic(request)
        
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)
    def post(self,request, format=None, *args, **kwargs):
        '''
        post方法
        '''
        params = get_parameter_dic(request)
        
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)