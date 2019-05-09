from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework.request import Request
from .models import *
from .controller import *
from .kmeans import *
from login.models import UserInfo
from .tasks import regularly
from login.common import get_parameter_dic
import time,json,requests,hashlib
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

class Test(APIView):
    '''
    测试
    '''
    def get(self, request, format=None, *args, **kwargs):
        keyword = 'xiyou'
        allocation_data = get_allocation_data(keyword)
        
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)


class WorkerDetail(APIView):
    '''
    工单详情
    '''
    def get(self, request, format=None, *args, **kwargs):
        '''
        获取工单详情
        '''
        params = get_parameter_dic(request)
        step_id = int(params.get('step_id', 10))
        w_id = int(params.get('id', 0))
        if step_id == 0:
            # 第一步阶段：数据收集详情页面接口
            res = Work_Order.objects.filter(id=w_id).values()
            allocation_data = res[0]['allocation_data']
            if allocation_data != None:
                allocation_data = json.loads(allocation_data)
                man_num = len(allocation_data['target_man'])
                woman_num = len(allocation_data['target_woman'])
                total_num  = man_num + woman_num
            else:
                total_num = '统计中'
            data = {
                'proposer_name': res[0]['proposer_name'],
                'school': res[0]['school'],
                'create_date': format_time(res[0]['create_date']),
                'countdown': countdown(res[0]['end_date']),
                'end_date': format_time(res[0]['end_date']),
                'form_data': res[0]['form_data'],
                'total_num': total_num
            }
        elif step_id == 1:
            # 第二部阶段 
            res = Work_Order.objects.filter(id=w_id).values()
            allocation_data = res[0]['allocation_data']
            if allocation_data != None:
                allocation_data = json.loads(allocation_data)
                man_num = len(allocation_data['target_man'])
                woman_num = len(allocation_data['target_woman'])
                total_num  = man_num + woman_num
                data = {
                    'total_num': total_num,
                    'man_num': man_num,
                    'woman_num': woman_num,
                    'countdown': countdown(res[0]['end_date'])
                }
            else:
                data = {
                    'total_num': 0,
                    'man_num': 0,
                    'woman_num': 0,
                    'countdown': countdown(res[0]['end_date'])
                }
        else:
            data = {}
        result_data = {'code': 200,'msg':'success', 'data': data }
        return Response(result_data)

    def put(self, request, format=None, *args, **kwargs):
        '''
        修改setp_id
        '''
        params = get_parameter_dic(request)
        step_id = int(params.get('step_id'))
        arg = {
            'step_id': step_id
        }
        if step_id == 2:
            arg['kemans_data'] = params.get('kemans_data')
        w_id = int(params.get('id', 0))
        
        try:
            Work_Order.objects.filter(id= w_id).update(**arg)
        except Exception:
            result_data = {'code': 200,'msg':'success', 'data': {} }
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)


class WorkerInfo(APIView):
    '''
    工单接口
    '''
    def get(self, request, format=None, *args, **kwargs):
        '''
        工单获取，根据权限显示工单列表
        '''
        params = get_parameter_dic(request)
        token = int(params.get('token'))
        filters = params.get('filters', '')
        tempres = UserInfo.objects.filter(u_id=token).values()
        roles=  int(tempres[0]['roles'])
       
        tempdict = {}
        if filters != '' and filters != '{}':
            temp = json.loads(filters)
            
            if temp['school'] != '':
                tempdict['school'] = temp['school']
            if temp['step_id'] != '':
                tempdict['step_id'] = temp['step_id']
        
        if roles == 3:
            #管理员
            res = Work_Order.objects.filter(**tempdict).values().order_by('-create_date')
        else:
            res = Work_Order.objects.filter(proposer=token, **tempdict).values().order_by('-create_date')
        
        # datalist数据处理
        resultList = []
        for i in res:
            # form_data=json.loads(i['form_data'])
            countDown = countdown(i['end_date'])
            tempDict = {
                'id': i['id'],
                'school': i['school'],
                'remark': i['remark'],
                'proposer_name': i['proposer_name'],
                'status_id': i['status_id'],
                'step_id': i['step_id'],
                'create_date': format_time(i['create_date']),
                'countdown': countDown
            }
            
            resultList.append(tempDict)
       
        result_data = {'code': 200,'msg':'success', 'data': resultList }
        return Response(result_data)

    def post(self, request, format=None, *args, **kwargs):
        '''
        工单接口
        '''
        params = get_parameter_dic(request)
        
        #参数获取
        form_data = params.get('form_data')
        description = params.get('description')
        userinfo = params.get('userinfo')
        end_date = params.get('endtime')
        remark = params.get('remark')
         
        temp_form_data = json.loads(form_data)
        keyword = temp_form_data.get('keyword')
        school = temp_form_data.get('school', '')
        status_id = 1
        step_id = 0
        proposer = userinfo.get('token')
        proposer_name = userinfo.get('name')
        create_date = int(time.time())
        
        # 工单录入   
        # 步骤一  
        try:
            req = Work_Order.objects.get_or_create(school= school, keyword=keyword, status_id=status_id, 
                        step_id = step_id , proposer=proposer, proposer_name=proposer_name, create_date=create_date,remark=remark,end_date=end_date,
                        description=description, form_data=form_data)
        except Exception:
            result_data = {'code': 200,'msg':'success', 'data': {} }
            return Response(result_data)

        print(req[1])
        # 步骤二
        # 定时执行宿舍分配
        if req[1]:
            timestr = format_time(params['endtime'])
            temp_args = []
            temp_args.append(keyword)
            regularly(timestr, temp_args)
        
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)


class KmeansModel(APIView):
    '''
    k-means 算法调用
    '''
    def get(self, request,format=None, *args, **kwargs):
        '''
        获取最佳聚类中心拐点图
        '''
        params = get_parameter_dic(request)  
        w_id = params.get('id', 0)
        res = Work_Order.objects.filter(id=w_id).values()
        keyword = res[0]['keyword']
        if res[0]['allocation_data'] != None:
            allocation_data = res[0]['allocation_data']
            try:
                get_elbow_picture(allocation_data,keyword)
            except Exception as eer:
                print("算法执行出错",eer)

        data = {
            'man': './static/images/man/' + keyword + '.png',
            'woman': './static/images/woman/' + keyword + '.png'
        }
        result_data = {'code': 200,'msg':'success', 'data': data }
        return Response(result_data)
    def post(self,request, format=None, *args, **kwargs):
        '''
        执行 kemans 获得分配结果
        '''
        params = get_parameter_dic(request)  
        w_id = params.get('id')
        woman_k = int(params.get('woman_k'))
        man_k = int(params.get('man_k'))
        res = Work_Order.objects.filter(id=w_id).values()
        keyword = res[0]['keyword']
        if res[0]['allocation_data'] != None:
            allocation_data = res[0]['allocation_data']
            #  kemans 调用
            try:
                results = run_kemans(allocation_data,keyword, woman_k, man_k)
            except Exception as eer:
                results = {}
                print("算法执行出错",eer)
        
        else:
            results = {}
        result_data = {'code': 200,'msg':'success', 'data': results }
        return Response(result_data)

class AuthWorker(APIView):
    '''
    权限管理
    '''
    def get(self, request, format=None, *args, **kwargs):
        '''
        权限申请列表获取,权限状态获取
        '''
        params = get_parameter_dic(request)  
        
        roles = int(params.get('roles'))
        proposer = int(params.get('proposer'))
        if roles == 3:
            # 管理员获取权限列表
            res = Auth_Work.objects.filter().values()
        else:
            try:
                res = Auth_Work.objects.filter(proposer=proposer).values()
                # 普通用户获取步骤，及状态
                data = {
                    'step': res[0]['step'],
                    'status_id': res[0]['status_id']
                }
            except Exception:
                data = {}

        result_data = {'code': 200,'msg':'success', 'data': data }
        return Response(result_data)

    def post(self, request, format=None, *args, **kwargs):
        '''
        权限申请提交
        '''
        params = get_parameter_dic(request)
        params['create_date'] = int(time.time())
        try:
            res = Auth_Work.objects.get_or_create(**params)
        except Exception:
            result_data = {'code': 200,'msg':'success', 'data': {} }
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)
    
    def put(self, request, format=None, *args, **kwargs):
        '''
        权限流程更新
        '''
        pass
