# -*-coding:utf-8 -*-
import json
import re
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import QueryDict

def get_parameter_dic(request, *args, **kwargs):
    '''
    request 参数统一处理函数
    '''
    if isinstance(request, Request) == False:
        return {}

    query_params = request.query_params
    if isinstance(query_params, QueryDict):
        query_params = query_params.dict()
    result_data = request.data
    if isinstance(result_data, QueryDict):
        result_data = result_data.dict()

    if query_params != {}:
        return query_params
    else:
        return result_data