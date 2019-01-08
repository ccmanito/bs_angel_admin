# from django.shortcuts import render
import json
from utils.serializer import JsonApiMixin
from django.views.generic.base import View


class LoginInfo(JsonApiMixin, View):
    '''
    用户登录接口
    '''
    def post(self, request, *args, **kwargs):
        param = json.loads(request.body, strict=False)
        # password = request.POST.get('password', '')
        # if not param:
        #     return self.render_to_response(code=400, msg='post parameter is null', data={})
        # 获取用户账号和密码
        username = param['username']
        print(username)
        password = param['password']

        result_dict = {'token': username}
        return self.render_to_response(code=200, msg='success', data=result_dict)
