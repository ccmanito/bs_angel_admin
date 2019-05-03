#! /usr/bin/env python
#-*- coding:utf-8 -*-

from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework.request import Request
from .controller import *
from .models import *
from system.models import SchoolInfo
from .common import get_parameter_dic
import time,json,requests,hashlib
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from qiniu import Auth
import json


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
    用户信息管理
    '''
    def get(self, request, *args, **kwargs):
        '''
        获取用户信息
        '''
        token = param = request.GET.get('token', '')
        result = UserInfo.objects.filter(u_id=token).values()
        result_dict = result[0]
        school = '西安邮电大学'
        res = SchoolInfo.objects.filter(school=school).values()
        # schoolinfo = {}
        # 权限处理
        if result_dict['roles'] == 3:
            result_dict['roles'] = ['admin']
        elif result_dict['roles'] == 2:
            result_dict['roles'] = ['teacher']
        else:
            result_dict['roles'] = ['student']
        result_dict['avatar'] = result_dict.pop('avatar')
        result_dict['name'] = result_dict.pop('name')
        result_dict['schoolinfo'] = res[0]
        result_data = {'code': 200,'msg':'success', 'data': result_dict }
        return Response(result_data)
    def post(self, request, *args, **kwargs):
        '''
        修改用户信息
        '''
        params = get_parameter_dic(request)
        
        # 获取参数
        tempdict = params.get('baseinfo')
        tempdict['livinghabits'] = params.get('habits')
        tempdict['interests'] = params.get('interests')
        passwordlist = params.get('passwordlist')
        
        #字段过滤
        token = tempdict.pop('token')
        tempdict.pop('usertype')
        tempdict.pop('roles')
        
        try:
            if passwordlist != False:
                # 绑定账号 
                if passwordlist['emailpasswd'] != '':
                    # 绑定email
                
                    # 密码MD5加密
                    credential = passwd_fomt(passwordlist['emailpasswd'])
                
                    UserAuth.objects.filter(u_id=token, identity_type='email').delete()
                    UserAuth.objects.create(identifier=tempdict['email'], identity_type='email', 
                        credential = credential , u_id=token, verified=1)
            
                elif passwordlist['mobilepasswd'] != '':
                    # 绑定 mobile
                    credential = passwd_fomt(passwordlist['mobilepasswd'])
                    UserAuth.objects.filter(u_id=token, identity_type='mobile').delete()
                    UserAuth.objects.create(identifier=tempdict['mobile'], identity_type='mobile', 
                        credential = credential , u_id=token, verified=1)
                else:
                    credential = passwd_fomt(passwordlist['twopasswd'])
                    UserAuth.objects.filter(u_id=token, identity_type='mobile').delete()
                    UserAuth.objects.filter(u_id=token, identity_type='email').delete()
                    UserAuth.objects.create(identifier=tempdict['mobile'], identity_type='mobile', 
                        credential = credential , u_id=token, verified=1)
                    UserAuth.objects.create(identifier=tempdict['email'], identity_type='email', 
                        credential = credential , u_id=token, verified=1)  
        except Exception:
            UserInfo.objects.filter(u_id=token).update(**tempdict)
            result_data = {'code': 200,'msg':'success', 'data': {} }
            return Response(result_data)
        
        try:
            UserInfo.objects.filter(u_id=token).update(**tempdict)
        except Exception:
            result_data = {'code': 200,'msg':'success', 'data': {} }
            return Response(result_data)
        
        result_data = {'code': 200,'msg':'success', 'data': {} }
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
        name = params['name'] # 昵称
        verified = True
        avatar = settings.AVATAR
        createtime = str(int(time.time()))
        # 数据对象操作
        credential = passwd_fomt(credential)
        try:
            if '@' in identifier:
                identity_type = 'email'
                res = UserInfo.objects.get_or_create(email=identifier, name=name, avatar=avatar, createtime=createtime)
                resset = UserInfo.objects.filter(email=identifier).values()
            else:
                identity_type = 'mobile'
                res = UserInfo.objects.get_or_create(mobile=identifier, name=name, avatar=avatar,  createtime=createtime) # 返回的是元祖 （data，true）
                resset = UserInfo.objects.filter(mobile=identifier).values()
            # 拿到u_id
            if res[1]:
                u_id = resset[0]['u_id'] #int

                res1 = UserAuth.objects.get_or_create(identifier=identifier, identity_type=identity_type, 
                    credential = credential, u_id=u_id, verified=verified)
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
        
        
        source = request.GET.get('source')
        result_dict = {}
        if source == 'true':
            result = UserAuth.objects.filter(identifier = param).values()
            if result:
                result_dict['identifier'] = result[0]['identifier']
            else:
                result_dict['identifier'] = ''
        else:
            try:
                token = int(request.META.get("HTTP_TOKEN"))
            except Exception:
                result_dict = {}
                result_dict['identifier'] = ''
                return Response({'code': 200,'msg':'success', 'data': result_dict })
            templist = []
            res = UserInfo.objects.filter(u_id=token).values()
            templist.append(res[0]['email'])
            templist.append(res[0]['mobile'])
            if param in templist:
                
                result_dict['identifier'] = ''
            else:
                result = UserAuth.objects.filter(identifier = param).values()
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
        
        githubinfo = {}
        if  temp['eer'] == '':
            github_userinfo = temp['result']
            # 初始化一些参数
            identifier = str(github_userinfo['id']) # 身份唯一标识
            credential = access_token # 授权凭证 
            github = github_userinfo['login']
            identity_type = 'github'
            if not github_userinfo['name']:
                name = github
            else:
                name = github_userinfo['name'] # 昵称
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
            # 绑定站内信息
            githubinfo = {}
            githubinfo['identifier'] = identifier
            githubinfo['credential'] = credential
            githubinfo['github'] = github
            githubinfo['name'] = name
            githubinfo['identity_type'] = identity_type
            githubinfo['avatar'] = avatar

            return render(request, 'login/home.html', {'githubinfo': githubinfo })
           
        
        return HttpResponseRedirect(settings.LOCAL_URL + '/user/github?token='+ token )

class GetQuniu(APIView):
    '''
    图片上传七牛云相关接口
    '''
    def get(self, request, *args, **kwargs):
        #需要填写你的 Access Key 和 Secret Key
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        #构建鉴权对象
        q = Auth(access_key, secret_key)
        #要上传的空间
        bucket_name = 'bs_angel'

        key = None
        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, key, 3600)

        res = {'code': 200,'msg':'success', 'data': {'token': token} }
        return Response(res)

class Syncavatar(APIView):
    '''
    更改用户头像，实时同步
    '''
    def post(self, request, *args, **kwargs):
        params = get_parameter_dic(request)
        u_id = params['token']
        avatar = params['avatar']
        UserInfo.objects.filter(u_id=u_id).update(avatar=avatar)
        res = {'code': 200,'msg':'success', 'data': {} }
        return Response(res)

def github(request):
    '''
    # 重定向渲染函数
    '''
    token = request.GET.get('token')
    return render(request, 'login/index.html', {'token': token})

def BindAccount(requests):
    '''
    第三方登录，站内账户绑定接口
    '''
    identifier = requests.POST.get('identifier', None)
    credential = requests.POST.get('credential', None)
    githubinfo = requests.POST.get('githubinfo', None)
    githubinfo = eval(githubinfo)
    md5 = hashlib.md5()
    #实例化md5加密方法
    md5.update(credential.encode())
    #进行加密，python2可以给字符串加密，python3只能给字节加密
    credential = md5.hexdigest()
    paramdict = {
        'identifier': identifier,
        'credential': credential,
        }
        
        #  数据库操作，匹配账户信息
    result = UserAuth.objects.filter(**paramdict).values()
    if result:
        # 存在账户，对信息进行合并
        try:
            paraminfo = {
                'github': githubinfo['github']
            }
            u_id = result[0]['u_id']
            resset = UserInfo.objects.filter(u_id=u_id).values()
            if  not resset[0]['avatar']:
                paraminfo['avatar'] = githubinfo['avatar']
            if  not resset[0]['name']:
                paraminfo['name'] = githubinfo['name']
            UserInfo.objects.filter(u_id=u_id).update(**paraminfo)
            
            # 创建登录凭证
            createtime = str(int(time.time()))
            UserAuth.objects.get_or_create(identifier=githubinfo['identifier'], identity_type=githubinfo['identity_type'], 
                    credential =githubinfo['credential'], u_id=u_id, verified=True)
            
        except Exception:
            return HttpResponse('false')
        
        return HttpResponse(u_id)
    else:
        # 不存在返回
        return HttpResponse('false')

def BindAccount2(requests):
    '''
    第三方登录，第一次登录不绑定站内账号，选择跳过走这个接口
    '''
    githubinfo = requests.POST.get('githubinfo', None)
    githubinfo = eval(githubinfo)
    try:
        createtime = str(int(time.time()))
        res = UserInfo.objects.get_or_create(github=githubinfo['github'], name=githubinfo['name'], avatar=githubinfo['avatar'], createtime=createtime) # 返回的是元祖 （data，true）
        resset = UserInfo.objects.filter(github=githubinfo['github'],createtime=createtime).values()
        # 拿到u_id
        if res[1]:
            u_id = resset[0]['u_id'] #int
            res1 = UserAuth.objects.get_or_create(identifier=githubinfo['identifier'], identity_type=githubinfo['identity_type'], 
            credential = githubinfo['credential'], u_id=u_id, verified=True)
            if res1[1]:
                token = str(u_id)
            else:
                token = ''
    except Exception as s:
        return HttpResponse(s)
    
    return HttpResponse(u_id) 