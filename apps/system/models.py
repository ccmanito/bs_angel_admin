# -*-coding:utf-8 -*-
from django.db import models


class DormInfo(models.Model):
    u_id = models.CharField(null=True,max_length=64,verbose_name=u'创建人u_id')
    proposer_name = models.CharField(null=True,max_length=64,verbose_name=u'创建人姓名')
    address = models.CharField(max_length=100, null=True, verbose_name=u'宿舍地址')
    floor = models.CharField(max_length=100, null=True, verbose_name=u'宿舍楼层' )
    dorm_id = models.CharField(max_length=100, null=True, verbose_name=u'宿舍号')
    status = models.IntegerField(default=0, verbose_name=u'宿舍状态',)
    dorm_size = models.IntegerField(default=6, verbose_name=u'宿舍大小')
    residents = models.CharField(max_length=200, null=True, default= '无', verbose_name=u'住户信息' )
    remark = models.CharField(max_length=500, null=True, verbose_name=u'备注信息')
    in_date = models.CharField(max_length=200, null=True, verbose_name=u'入住时间')

    class Meta:
        db_table='dorm_info'


class SchoolInfo(models.Model):
    school = models.CharField(max_length=100, verbose_name=u'学校名称', unique=True ,null=True)
    college = models.CharField(max_length=1000, verbose_name=u'学院集合' ,null=True)
    major = models.CharField(max_length=1000, verbose_name=u'专业集合' ,null=True)
    grade = models.CharField(max_length=1000, verbose_name=u'年级集合' ,null=True)
    classname = models.CharField(max_length=1000, verbose_name=u'班级集合' ,null=True)
    
    class Meta:
        db_table='school_info'