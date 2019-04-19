# -*-coding:utf-8 -*-
from django.db import models


class Interest(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'兴趣爱好title', null=True)
    key = models.CharField(max_length=20, verbose_name=u'唯一键', unique=True ,null=True)
    
    def __str__(self):
        return self.title
    
    #定义元选项
    class Meta:
        db_table='angel_interest'
