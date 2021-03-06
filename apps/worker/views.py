from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework.request import Request
from .models import *
from .controller import *
from .kmeans import *
from login.models import UserInfo
from system.models import DormInfo
from .tasks import regularly
from login.common import get_parameter_dic
import time,json,requests,hashlib
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


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
            print('wwwwwwwwwwwwwwwwwwwwwwwwwwww')
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
        elif step_id == 2:
            # 人性化分配
            u_id = params.get('u_id')

            # 获取男/女的总数
            res = Work_Order.objects.filter(id=w_id).values()
            allocation_data = res[0]['allocation_data']
            if allocation_data != None:
                allocation_data = json.loads(allocation_data)
                man_num = len(allocation_data['target_man'])
                woman_num = len(allocation_data['target_woman'])
            
            res_man = DormInfo.objects.filter(u_id=u_id, status=0,dorm_type='男').values()
            res_woman = DormInfo.objects.filter(u_id=u_id,status=0, dorm_type='女').values()
            
            six_dorm_num = DormInfo.objects.filter(u_id=u_id,status=0, dorm_size=6,dorm_type='女').count()
            four_dorm_num = DormInfo.objects.filter(u_id=u_id,status=0, dorm_size=4,dorm_type='女').count()
            eight_dorm_num = DormInfo.objects.filter(u_id=u_id,status=0, dorm_size=8,dorm_type='女').count()
            ten_dorm_num = DormInfo.objects.filter(u_id=u_id,status=0, dorm_size=10,dorm_type='女').count()
            six_dorm_man_num = DormInfo.objects.filter(u_id=u_id,status=0, dorm_size=6,dorm_type='男').count()
            four_dorm_man_num = DormInfo.objects.filter(u_id=u_id,status=0, dorm_size=4,dorm_type='男').count()
            eight_dorm_man_num = DormInfo.objects.filter(u_id=u_id,status=0, dorm_size=8,dorm_type='男').count()
            ten_dorm_man_num = DormInfo.objects.filter(u_id=u_id,status=0, dorm_size=10,dorm_type='男').count()
            
            womanlist = []
            manlist = []
            for i in res_man:
                temp_man_dict = {
                    'id': i['id'],
                    'dorm_id': i['dorm_id'],
                    'dorm_type': i['dorm_type'],
                    'address': i['address'],
                    'floor': i['floor'],
                    'dorm_size': i['dorm_size'],
                }
                manlist.append(temp_man_dict)
            for i in res_woman:
                temp_woman_dict = {
                    'id': i['id'],
                    'dorm_id': i['dorm_id'],
                    'address': i['address'],
                    'dorm_type': i['dorm_type'],
                    'floor': i['floor'],
                    'dorm_size': i['dorm_size'],
                }
                womanlist.append(temp_woman_dict)
            
            data = {
                'man_num': man_num,
                'woman_num': woman_num,
                'six_dorm_man_num': six_dorm_man_num,
                'four_dorm_man_num': four_dorm_man_num,
                'eight_dorm_man_num': eight_dorm_man_num,
                'ten_dorm_man_num': ten_dorm_man_num,
                'six_dorm_num': six_dorm_num,
                'four_dorm_num': four_dorm_num,
                'eight_dorm_num': eight_dorm_num,
                'ten_dorm_num': ten_dorm_num,
                'womanlist': womanlist,
                'manlist': manlist
            }
        elif step_id == 3:
            res = Work_Order.objects.filter(id=w_id).values()
            target_data = json.loads(res[0]['target_data'])

            data = target_data
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
        w_id = int(params.get('id', 0))
        arg = {
            'step_id': step_id
        }
        if step_id == 2:
            arg['kemans_data'] = params.get('kemans_data') 
        elif step_id == 3:
            arg['target_data'] = params.get('resultdata')
            try:
                syncDormInfo(params.get('resultdata'))
                # 分配结束同步到系统各个表
            except Exception as eer:
                print('分配宿舍同步失败',eer)
        
        else:
            print('更改步骤')
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
    
    def delete(self, request,format=None, *args, **kwargs):
        '''
        删除分配流程
        '''
        params = get_parameter_dic(request)
        id = params.get('id')
        try:
            Work_Order.objects.filter(id=id).delete()
        except Exception as eer:
            print('该用户信息删除失败' + eer)
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
        
        if roles == 3:
            # 管理员获取权限列表
            filters = params.get('filters', '')

            tempdict = {}
            if filters != '' and filters != '{}':
                temp = json.loads(filters)
                if temp['status_id'] != '':
                    tempdict['status_id'] = temp['status_id']
            
            res = Auth_Work.objects.filter(**tempdict).values()
            req = []
            for i in res:
                tempdict = {
                    'id': i['id'],
                    'school': i['school'],
                    'remark': i['remark'],
                    'u_id': i['proposer'],
                    'proposer_name': i['proposer_name'],
                    'create_date': format_time(i['create_date']),
                    'professional': i['professional'],
                    'status_id': i['status_id']
                }
                req.append(tempdict)
            data = req
        else:
            try:
                proposer = int(params.get('proposer'))
                res = Auth_Work.objects.filter(proposer=proposer).values().order_by('-create_date')
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
        params = get_parameter_dic(request)
        print(params)
        a_id = params.get('id')
        key = params.get('key')
        u_id = params.get('u_id')
        if key == 'pass':
            # 通过申请
            tempdict = {
                'step': 3,
                'status_id': 1
            }
            UserInfo.objects.filter(u_id=u_id).update(roles=2,status=2)
            Auth_Work.objects.filter(id=a_id).update(**tempdict)
        else:
            # 驳回申请
            tempdict = {
                'step': 0,
                'status_id': 2
            }
            UserInfo.objects.filter(u_id=u_id).update(roles=1)
            Auth_Work.objects.filter(id=a_id).update(**tempdict)
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)


class Distribution(APIView):
    '''
    执行分配宿舍函数
    '''
    def post(self, request, format=None, *args, **kwargs):
        '''
        流程第三步，宿舍分配
        '''
        params = get_parameter_dic(request)
        w_id = params.get('id')
        woman_dorm_list = params.get('woman_dorm_list')
        man_dorm_list = params.get('man_dorm_list')
        
        # 对宿舍按房间大小进行降序排序
        man_dormlist = sorted(man_dorm_list,key=lambda keys:keys['dorm_size'],reverse = True)
        woman_dormlist = sorted(woman_dorm_list,key=lambda keys:keys['dorm_size'],reverse = True)
        
        # 获取待分配数据
        res = Work_Order.objects.filter(id=w_id).values()
        kemans_data = json.loads(res[0]['kemans_data'])
        ManData = kemans_data[0]['tag_man_list']
        WomanData = kemans_data[1]['tag_woman_list']
        
        # 男生宿舍分配
        num = len(ManData)
        count = 0
        for i in man_dormlist:
            i['userlist'] = []
            for j in range(i['dorm_size']):
                if count >= num:
                    break
                temp = ManData[count]
                
                if len(temp):
                    i['userlist'].append(temp.pop())
                else:
                    count = count + 1
                    break
                
        # 女生宿舍分配
        num = len(WomanData)
        count = 0
        for i in woman_dormlist:
            i['userlist'] = []
            for j in range(i['dorm_size']):
                if count >= num:
                    break
                temp = WomanData[count]
                
                if len(temp):
                    i['userlist'].append(temp.pop())
                else:
                    count = count + 1
                    break
        
        man_dormlist[:] =  [d for d in man_dormlist if d.get('userlist') != [] ]
        woman_dormlist[:] =  [d for d in woman_dormlist if d.get('userlist') != [] ]
        
        data = {
            'man_result': man_dormlist,
            'woman_result': woman_dormlist
        }
        result_data = {'code': 200,'msg':'success', 'data': data }
        return Response(result_data)


