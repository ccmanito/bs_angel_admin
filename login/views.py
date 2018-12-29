# from django.shortcuts import render
import json
from utils.serializer import JsonApiMixin
from django.views.generic.base import View


class LoginInfo(JsonApiMixin, View):
    '''
    用户登录接口
    '''
    def post(self, *args, **kwargs):
        param = self.request.POST
        if not param:
            return self.render_to_response(code=400, msg='post parameter is null', data={})
        # 获取用户账号和密码
        username = param.get('username', '')
        password = param.get('pssword', '')
        result_dict = {'username': username, 'password': password}
        return self.render_to_response(code=200, msg='success', data=result_dict)
