# -*-coding:utf-8 -*-
import json
import re
import urllib.request
from urllib.request import Request, urlopen
import requests
from django.conf import settings

OAUTH_GITHUB_CONFIG  = settings.OAUTH_GITHUB_CONFIG

def get_access_token(request_code):
    '''
    获取access_token  、 参数是 code
    '''
    params = {
        'grant_type': 'authorization_code',
        'client_id': OAUTH_GITHUB_CONFIG['client_id'],
        'client_secret': OAUTH_GITHUB_CONFIG['client_secret'],
        'code': request_code,
        'redirect_uri': OAUTH_GITHUB_CONFIG['redirect_uri'],
        'state': 'Github'
        }
    url_access_token = 'https://github.com/login/oauth/access_token'
    header_selfdefine = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    # request 请求 access_token and user data
    try:
        print('888888888888')
        req = Request(url=url_access_token, data=json.dumps(params).encode('utf-8'),  method="POST", headers=header_selfdefine )
        resultset = urlopen(req).read().decode('utf-8')
        resultset = json.loads(resultset)
        access_token = resultset['access_token'] # 拿到access_token 就可以拿到第三方的数据。
        print(access_token)
    except Exception as eer:
        return {"eer": eer}
    return access_token


def get_github_userinfo(access_token):
    '''
    获取github用户信息
    '''
    req = {
            'result': {},
            'eer': ''
        }
    try:
        payload = {
            'access_token': access_token    
        }
        res = requests.get("https://api.github.com/user",params=payload)
        req['result'] = res.json()
    except Exception as eer:
        req['eer'] = eer
    return req
