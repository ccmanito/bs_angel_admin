#! /usr/bin/env python
#-*- coding:utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .controller import *
from .models import *
from .common import get_parameter_dic
import time,json,requests,hashlib
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.conf import settings


class LoginAuth(APIView):
    '''
    用户登录接口
    '''
    def post(self, request,format=None, *args, **kwargs):
        
        param = get_parameter_dic(request)
        paramdict = {} # 参数字典
        identifier = param['username']
        credential = param['password']
        identity_type = param['identity_type']
        
        md5 = hashlib.md5()
        #实例化md5加密方法
        md5.update(credential.encode())
        #进行加密，python2可以给字符串加密，python3只能给字节加密
        credential = md5.hexdigest()
        paramdict = {
        'identifier': identifier,
        'credential': credential,
        'identity_type': identity_type
        }
        
        #  数据库操作，匹配账户信息
        result = UserAuth.objects.filter(**paramdict).values()

        if result:
            token = result[0]['u_id']
            result_dict = {'token': token}
        else:
            temp = {'code':401.1, 'msg':'Login failed, Password mistake!', 'data':{} }
            return Response(temp)
        result_data = {'code': 200,'msg':'success', 'data': result_dict }
        return Response(result_data)
class LoginInfo(APIView):
    '''
    获取用户信息
    '''
    def get(self, request, *args, **kwargs):
        token = param = request.GET.get('token', '')
        # param  = get_parameter_dic(request)
        # token = param['token']
        result = UserInfo.objects.filter(u_id=token).values()
        result_dict = result[0]
        
        # 权限处理
        if result_dict['roles'] == 3:
            result_dict['roles'] = ['admin']
        elif result_dict['roles'] == 2:
            result_dict['roles'] = ['teacher']
        else:
            result_dict['roles'] = ['student']
        print(result_dict['roles'])
        result_dict['avatar'] = result_dict.pop('avatar')
        result_dict['name'] = result_dict.pop('nickname')
        result_dict['interest'] = {
            '喜欢': '宝宝',
            '爱好': 'zhouzhou' 
            }
        result_data = {'code': 200,'msg':'success', 'data': result_dict }
        return Response(result_data)


class LoginOut(APIView):
    '''
    登出接口
    '''
    def post(self, request, *args, **kwargs):
        result_dict = {}
        result_data = {'code': 200,'msg':'success', 'data': {} }
        return Response(result_data)

class Regedit(APIView):
    '''
    用户表单注册接口 邮箱email，手机号mobile三种方式注册
    '''
    def post(self, request, *args, **kwargs):
        params = get_parameter_dic(request)
        identifier = params['identifier'] # 身份唯一标识
        credential = params['credential'] # 授权凭证
        nickname = params['nickname'] # 昵称
        verified = True
        avatar = settings.AVATAR
        createtime = str(int(time.time()))
        # 数据对象操作
        md5 = hashlib.md5()
        #实例化md5加密方法
        md5.update(credential.encode())
        #进行加密，python2可以给字符串加密，python3只能给字节加密
        credential = md5.hexdigest()
        try:
            if '@' in identifier:
                identity_type = 'email'
                res = UserInfo.objects.get_or_create(email=identifier, nickname=nickname, avatar=avatar)
                resset = UserInfo.objects.filter(email=identifier).values()
            else:
                identity_type = 'mobile'
                res = UserInfo.objects.get_or_create(mobile=identifier, nickname=nickname, avatar=avatar) # 返回的是元祖 （data，true）
                resset = UserInfo.objects.filter(mobile=identifier).values()
            # 拿到u_id
            if res[1]:
                u_id = resset[0]['u_id'] #int

                res1 = UserAuth.objects.get_or_create(identifier=identifier, identity_type=identity_type, 
                    credential = credential, createtime=createtime, u_id=u_id, verified=verified)
                if res1[1]:
                    token = u_id
            else:
                return Response({'code':400, 'msg':'注册失败', 'data':{}})
        except Exception as err:
            return Response({'code':400, 'msg':'注册失败', 'data':{}})
       
        result_data = {'code': 200,'msg':'success', 'data': {'token': token} }
        return Response(result_data)
    
    def get(self, request, *args, **kwargs):
        '''
        判断用户是否存在
        '''
        param = request.GET.get('str', '')
        result = UserAuth.objects.filter(identifier = param).values()
        result_dict = {}
        if result:
            result_dict['identifier'] = result[0]['identifier']
        else:
            result_dict['identifier'] = ''
        return Response({'code': 200,'msg':'success', 'data': result_dict })


class GithubCheck(APIView):
    '''
    github第三方登录 Github 回调类
    '''
    def get(self, request, *args, **kwargs):
        request_code = request.GET.get('code')
        state = request.GET.get('state') or '/'
        
        #获取access_token
        access_token = get_access_token(request_code)
        
        # 获取用户信息
        temp = get_github_userinfo(access_token)
        if  temp['eer'] == '':
            github_userinfo = temp['result']
            # 初始化一些参数
            identifier = str(github_userinfo['id']) # 身份唯一标识
            credential = access_token # 授权凭证 
            github = github_userinfo['login']
            identity_type = 'github'
            if not github_userinfo['name']:
                nickname = github
            else:
                nickname = github_userinfo['name'] # 昵称
            if not github_userinfo['avatar_url']:
                avatar = settings.AVATAR
            else:
                avatar = github_userinfo['avatar_url']
        
        else:
            token = ''
            return HttpResponseRedirect(settings.LOCAL_URL + '/user/github?token='+ token )
        
        # 判断该用户是否第一次登录
        user_exist = UserAuth.objects.filter(identity_type='github', identifier=identifier).values()
        if user_exist:
            ''' 该用户存在，刷新access_token'''
            UserAuth.objects.filter(identity_type='Github', identifier=identifier).update(credential=credential)
            resset = UserAuth.objects.filter(identity_type='Github', identifier=identifier).values()
            token = str(resset[0]['u_id'])
        else:
            ''' 该用户不存在，注册'''
            try:
                res = UserInfo.objects.get_or_create(github=github, nickname=nickname, avatar=avatar) # 返回的是元祖 （data，true）
                resset = UserInfo.objects.filter(github=github).values()
            # 拿到u_id
                if res[1]:
                    u_id = resset[0]['u_id'] #int
                    createtime = str(int(time.time()))
                    res1 = UserAuth.objects.get_or_create(identifier=identifier, identity_type=identity_type, 
                    credential = credential, createtime=createtime, u_id=u_id, verified=True)
                    if res1[1]:
                        token = str(u_id)
                    else:
                        return Response({'code':400, 'msg':'注册失败', 'data':{}})
            except Exception as err:
                return Response({'code':400, 'msg':'注册失败', 'data':{}})
        
        return HttpResponseRedirect(settings.LOCAL_URL + '/user/github?token='+ token )

# 重定向渲染函数
def github(request):
    token = request.GET.get('token')
    return render(request, 'login/index.html', {'token': token})