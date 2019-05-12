#! /usr/bin/env python
#-*- coding:utf-8 -*-
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework.request import Request
from .models import *
from login.models import UserInfo
from .controller import *
from login.common import get_parameter_dic
import time,json,requests,hashlib
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


class SchoolDetail(APIView):
    '''
    校园基本信息管理
    '''
    def get(self, request,format=None, *args, **kwargs):
        params = get_parameter_dic(request)
        key = params.get('key')
        if key == 'list':
            # 获取学校信息列表
            filters = params.get('filters', '')
            page = params.get('page',None)
            page_size = params.get('page_size',None)


            # 筛选功能
            tempdict = {}
            if filters != '' and filters != '{}':
                temp = json.loads(filters)
                if temp['school'] != '':
                    tempdict['school__contains'] = temp['school']
            
            if not page or not page_size:
                page = 1
                page_size = 10

            try:
                total_count = SchoolInfo.objects.filter(**tempdict).count()
                res = SchoolInfo.objects.filter(**tempdict).values().order_by('-id')
    
            except Exception as eer:
                print('查询宿舍信息失败' + eer)
            
            if total_count == 0:
                    result_data = {'code': 200,'msg':'查询结果为空', 'data': {} }
            
            paginator = Paginator(res,page_size)
            try:
                page_info = paginator.page(page)
            except PageNotAnInteger:
                page_info = paginator.page(1)
            except EmptyPage:
                page_info = paginator.page(paginator.num_pages)

            # datalist数据处理
            resultList = []
            for i in page_info:
                
                tempDict = {
                    'id': i['id'],
                    'school': i['school'],
                    'college': i['college'],
                    'major': i['major'],
                    'grade': i['grade'],
                    'classname': i['classname'],
                }
                
                resultList.append(tempDict)
            data = {
                'totalNum': total_count,
                'data': resultList
            }
        elif key == 'schoollist':
            # 获取学校列表
            res = SchoolInfo.objects.filter().values()
            school_list = []
            for i in res:
                school_list.append(i['school'])
            data = school_list
        elif key == 'comm':
            # 学校信息供其他模块使用，将信息格式化
            school = params.get('school')
            res = SchoolInfo.objects.filter(school=school).values()
            
            if len(res):
                req = {}
                for k,v in res[0].items():
                    if k == 'id':
                        continue
                    formatstr = v.replace('，', ',')
                    req[k] = formatstr.split(',')
                data = req
            else:
                data = {}
        else:
            # 修改学校信息调用源信息
            s_id = params.get('id')
            res = SchoolInfo.objects.filter(id=s_id).values()
            data = res[0]
        result_data = {'code': 200,'msg':'success', 'data': data }
        return Response(result_data)

    def post(self, request,format=None, *args, **kwargs):
        '''
        添加学校信息
        '''
        params = get_parameter_dic(request)

        school = params.get('school', '')
        college = params.get('college' '')
        major = params.get('major', '')
        grade = params.get('grade', '')
        classname = params.get('classname', '')
        try:
            SchoolInfo.objects.get_or_create(school=school, college=college, 
                        major = major , grade=grade, classname=classname)
        except Exception:
            result_data = {'code': 200,'msg':'success', 'data': {} }
            return Response(result_data)
        
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)

    def put(self, request,format=None, *args, **kwargs):
        '''
        更新学校信息
        '''
        params = get_parameter_dic(request)
        print(params)
        d_id = params.get('ticketId')
        school = params.get('school', '')
        college = params.get('college' '')
        major = params.get('major', '')
        grade = params.get('grade', '')
        classname = params.get('classname', '')
        
        tempdict = {
            'school': school,
            'college': college,
            'major': major,
            'grade': grade,
            'classname': classname
        }
        try:
            SchoolInfo.objects.filter(id=d_id).update(**tempdict)
        except Exception as eer:
            print('该学校信息更新失败' + eer)
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)
    
    def delete(self, request,format=None, *args, **kwargs):
        '''
        删除学院信息
        '''
        params = get_parameter_dic(request)
        d_id = params.get('id')
        try:
            SchoolInfo.objects.filter(id=d_id).delete()
        except Exception as eer:
            print('该学校信息删除失败' + eer)
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)


class DormDetail(APIView):
    '''
    宿舍信息管理
    '''
    def get(self, request,format=None, *args, **kwargs):
        '''
        获取宿舍列表信息
        '''
        params = get_parameter_dic(request)
        token = int(params.get('token'))
        filters = params.get('filters', '')
        tempres = UserInfo.objects.filter(u_id=token).values()
        roles=  int(tempres[0]['roles'])
        page = params.get('page',None)
        page_size = params.get('page_size',None)


        # 筛选功能
        tempdict = {}
        if filters != '' and filters != '{}':
            temp = json.loads(filters)
            print(temp)
            if temp['status'] != '':
                tempdict['status'] = temp['status']
            if temp['floor'] != '':
                tempdict['floor__contains'] = temp['floor']
        
        if not page or not page_size:
            page = 1
            page_size = 10

        try:
            if roles == 3:
                #管理员
                total_count = DormInfo.objects.filter(**tempdict).count()
                res = DormInfo.objects.filter(**tempdict).values().order_by('-id')
            else:
                total_count = DormInfo.objects.filter(u_id=token, **tempdict).count()
                res = DormInfo.objects.filter(u_id=token, **tempdict).values().order_by('-id')
            
        except Exception as eer:
            print('查询宿舍信息失败' + eer)
        
        if total_count == 0:
                result_data = {'code': 200,'msg':'查询结果为空', 'data': {} }
        
        paginator = Paginator(res,page_size)
        try:
            page_info = paginator.page(page)
        except PageNotAnInteger:
            page_info = paginator.page(1)
        except EmptyPage:
            page_info = paginator.page(paginator.num_pages)

        # datalist数据处理
        resultList = []
        for i in page_info:
            if i['residents'] == '无':
                residents = [{'name': '无'}]
            else:
                residents = json.loads(i['residents'])
            tempDict = {
                'id': i['id'],
                'status': i['status'],
                'residents': residents,
                'dorm_size': i['dorm_size'],
                'floor': i['floor'],
                'address': i['address'],
                'dorm_type': i['dorm_type'] + '生宿舍',
                'in_date': format_time(i['in_date']),
                'dorm_id':  i['dorm_id'],
            }
            
            resultList.append(tempDict)
        data = {
            'totalNum': total_count,
            'data': resultList
         }
        result_data = {'code': 200,'msg':'success', 'data': data }
        return Response(result_data)
    
    def post(self, request,format=None, *args, **kwargs):
        '''
        增加宿舍信息
        '''
        params = get_parameter_dic(request)
        address = params.get('address')
        floor = params.get('floor')
        dorm_id = params.get('dorm_id')
        dorm_size = params.get('dorm_size')
        dorm_type = params.get('dorm_type')
        userinfo = params.get('userinfo')
        remark = params.get('remark')
        u_id = userinfo.get('token')
        proposer_name = userinfo.get('name')
        
        parameter = {
            'address': address,
            'floor': floor,
            'dorm_id': dorm_id,
            'remark': remark,
            'u_id': u_id,
            'dorm_size': dorm_size,
            'dorm_type': dorm_type,
            'proposer_name': proposer_name
        }
        try:
            DormInfo.objects.get_or_create(**parameter)
        except Exception as eer:
            print('执行失败：eer =' + eer)
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)

    def put(self, request,format=None, *args, **kwargs):
        '''
        清空宿舍信息
        '''
        params = get_parameter_dic(request)
        d_id = params.get('id')
        tempdict = {
            'residents': '无',
            'status': 0,
            'in_date': None
        }
        try:
            DormInfo.objects.filter(id=d_id).update(**tempdict)
        except Exception as eer:
            print('该宿舍清空失败' + eer)
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)
    
    def delete(self, request,format=None, *args, **kwargs):
        '''
        删除宿舍信息
        '''
        params = get_parameter_dic(request)
        d_id = params.get('id')
        try:
            DormInfo.objects.filter(id=d_id).delete()
        except Exception as eer:
            print('该宿舍删除失败' + eer)
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)


class InfoDetail(APIView):
    '''
    用户获取宿舍信息
    '''
    def get(self, request,format=None, *args, **kwargs):
        params = get_parameter_dic(request)
        d_id = params.get('dorm_id')
        res = DormInfo.objects.filter(id=d_id).values()
        if res == []:
            if res[0]['residents'] == '无':
                residents = [{'name': '无'}]
            else:
                residents = json.loads(res[0]['residents'])
        
            data = [{
                'id': res[0]['id'],
                'address': res[0]['address'],
                'floor': res[0]['floor'],
                'residents': residents,
                'in_date': format_time(res[0]['in_date'])
            }]
        else:
            data = []
        result_data = {'code': 200,'msg':'success', 'data': data }
        return Response(result_data)


class UserList(APIView):
    '''
    用户信息管理
    '''
    def get(self, request, format=None, *args, **kwargs):
        '''
        所有用户信息查看
        '''
        params = get_parameter_dic(request)
        
        filters = params.get('filters', '')
        page = params.get('page',None)
        page_size = params.get('page_size',None)

        # 筛选功能
        tempdict = {}
        if filters != '' and filters != '{}':
            temp = json.loads(filters)
            if temp['name'] != '':
                tempdict['name__contains'] = temp['name']

            if temp['status'] != '':
                tempdict['status'] = temp['status']

        if not page or not page_size:
            page = 1
            page_size = 10

        try:
            total_count = UserInfo.objects.filter(**tempdict).count()
            res = UserInfo.objects.filter(**tempdict).values().order_by('u_id')

        except Exception as eer:
            print('查询用户信息失败' + eer)
        
        if total_count == 0:
                result_data = {'code': 200,'msg':'查询结果为空', 'data': {} }
        
        paginator = Paginator(res,page_size)
        try:
            page_info = paginator.page(page)
        except PageNotAnInteger:
            page_info = paginator.page(1)
        except EmptyPage:
            page_info = paginator.page(paginator.num_pages)

        # datalist数据处理
        resultList = []
        for i in page_info:
            
            tempDict = {
                'u_id': i['u_id'],
                'name': i['name'],
                'sex': i['sex'],
                'roles': i['roles'],
                'email': i['email'],
                'mobile': i['mobile'],
                'professional': i['professional'],
                'dorm_id': i['dorm_id'],
                'status': i['status'],
                'school': i['school'],
                'college': i['college'],
                'major': i['major'],
                'grade': i['grade'],
                'classname': i['classname'],
            }
            
            resultList.append(tempDict)
        data = {
            'totalNum': total_count,
            'data': resultList
        }
        result_data = {'code': 200,'msg':'success', 'data': data }
        return Response(result_data)

    def delete(self, request,format=None, *args, **kwargs):
        '''
        删除用户信息
        '''
        params = get_parameter_dic(request)
        u_id = params.get('u_id')
        try:
            UserInfo.objects.filter(u_id=u_id).delete()
        except Exception as eer:
            print('该用户信息删除失败' + eer)
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)    
    

class Statistics(APIView):
    '''
    资源统计
    '''
    def get(self, request,format=None, *args, **kwargs):
        params = get_parameter_dic(request)

        totalUserCount = UserInfo.objects.filter().count()
        totalDormCount = DormInfo.objects.filter().count()
        totalVisitsCount = int(3020)
        totalSchoolCount = SchoolInfo.objects.filter().count()
        
        total_woman = UserInfo.objects.filter(sex='女').count()
        total_man = UserInfo.objects.filter(sex='男').count()
        
        total_free_dorm = DormInfo.objects.filter(status=0).count()
        total_used_dorm = DormInfo.objects.filter(status=1).count()
        
        data = {
            'total_free_dorm': total_free_dorm,
            'total_used_dorm': total_used_dorm,
            'total_woman': total_woman,
            'total_man': total_man,
            'totalUserCount': totalUserCount,
            'totalDormCount': totalDormCount,
            'totalVisitsCount': totalVisitsCount,
            'totalSchoolCount': totalSchoolCount
        }
        result_data = {'code': 200,'msg':'success', 'data': data }
        return Response(result_data)