# from django.shortcuts import render
import json
from utils.serializer import JsonApiMixin
from django.views.generic.base import View


class Test(JsonApiMixin, View):
    def get(self, *args, **kwargs):
        result_dict = {'count': 'count', 'details': 'res_list'}
        return self.render_to_response(code=200, msg='success', data=result_dict)