# -*- coding: utf-8 -*-
import json
import re
from django.http.response import HttpResponse
from django.db.models.query import QuerySet
from django.core.serializers import serialize
from django.db import models


def default_serializer(obj):
    if isinstance(obj, QuerySet) or isinstance(obj, list):
        # Queryset实例直接使用Django内置的序列化工具进行序列化
        return json.loads(serialize('json', obj))
    if isinstance(obj, models.Model):
        # 单个model， django内置的序列化不支持，做一个转换
        return json.loads(serialize('json', [obj])[1:-1])
    if hasattr(obj, 'isoformat'):
        #处理日期类型
        return obj.isoformat()
    return obj


def json_serializer(query_list, fields=None, exclude=None):
    """
    将 queryset 或者单个 查出的model 序列化成json.
    :param query_list:  queryset值 或单个对象
    :param fields: 值为列表 ['id',..]， 需要返回的字段
    :param exclude: 值为列表 ['id', ]， 排除的字段值
    :return: 返回结果为经过fields和exclude过滤后的json结果。
    """
    temp_list = default_serializer(query_list)

    if isinstance(temp_list, dict):
        # 单个数据
        field_list = temp_list['fields']
        field_list['id'] = str(temp_list['pk'])
        if fields and isinstance(fields, list):
            for fd in field_list.keys():
                if fd not in fields:
                    del field_list[fd]
        if exclude and isinstance(exclude, list):
            for fd in exclude:
                if fd in field_list.keys():
                    del field_list[fd]
        for keys, values in field_list.iteritems():
            if not values:
                # 数据库无值时， 赋空字符串
                field_list[keys] = ""
            if isinstance(values, int) or isinstance(values, float):
                field_list[keys] = str(values)
            if isinstance(values, unicode) and re.match("(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)", values):
                # 时间格式转换
                temp_datetime = values.replace("T", " ")
                temp_datetime = temp_datetime.split('.')[0]
                field_list[keys] = temp_datetime
    elif isinstance(temp_list, list):
        # queryset数组
        field_list = []
        for temp in temp_list:
            temp_field = temp['fields']
            temp_field['id'] = temp['pk']
            if fields and isinstance(fields, list):
                for fd in temp_field.keys():
                    if fd not in fields:
                        del temp_field[fd]
            if exclude and isinstance(exclude, list):
                for fd in exclude:
                    if fd in temp_field.keys():
                        del temp_field[fd]
            for keys, values in temp_field.iteritems():
                if not values:
                    temp_field[keys] = ""
                if isinstance(values, int) or isinstance(values, float):
                    temp_field[keys] = str(values)
                if isinstance(values, unicode) and re.match("(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)", values):
                    # 时间格式转换
                    temp_datetime = values.replace("T", " ")
                    temp_datetime = temp_datetime.split('.')[0]
                    temp_field[keys] = temp_datetime
            field_list.append(temp_field)
    else:
        field_list = temp_list
    return field_list


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    response_class = HttpResponse

    def json_required(self, request):
        if request.GET.get("format") == "json" or "application/json" in request.META.get("CONTENT_TYPE"):
            return True
        return False

    def render_to_response(self, context, callback=None, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        response_kwargs['content_type'] = 'application/json'
        json_res = self.convert_context_to_json(context)
        if callback:
            JsonP = callback + '(' + json.dumps(json_res) + ')'
            return self.response_class(JsonP, **response_kwargs)
        return self.response_class(json.dumps(json_res), **response_kwargs)

    def convert_context_to_json(self, context, fields=None, exclude=None):
        """Convert the context dictionary into a JSON object"""
        if not isinstance(context, dict):
            context = json_serializer(context, fields, exclude)
        return context


class JsonApiMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    response_class = HttpResponse

    def render_to_response(self, code=200, msg="success", data="", **response_kwargs):
        response_kwargs['content_type'] = 'application/json'
        context = {
            "code": code,
            "msg": msg,
            "data": data
        }
        callback = self.request.GET.get("callback")
        if callback:
            JsonP = callback + '(' + json.dumps(context) + ')'
            return self.response_class(JsonP, **response_kwargs)
        return self.response_class(json.dumps(context), **response_kwargs)

    def json_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(json.dumps(context), **response_kwargs)
