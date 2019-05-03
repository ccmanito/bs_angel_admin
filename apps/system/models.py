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

class SchoolInfo(models.Model):
    school = models.CharField(max_length=100, verbose_name=u'学校名称', unique=True ,null=True)
    college = models.CharField(max_length=1000, verbose_name=u'学院集合' ,null=True)
    major = models.CharField(max_length=1000, verbose_name=u'专业集合' ,null=True)
    grade = models.CharField(max_length=1000, verbose_name=u'年级集合' ,null=True)
    classname = models.CharField(max_length=1000, verbose_name=u'班级集合' ,null=True)
    
    class Meta:
        db_table='school_info'