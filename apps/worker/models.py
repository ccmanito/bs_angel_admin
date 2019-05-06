# -*-coding:utf-8 -*-
from django.db import models

class Work_Order(models.Model):
    keyword = models.CharField(max_length=64,unique=True, verbose_name=u'关键字')
    status_id = models.IntegerField(default=1,verbose_name=u'工单状态')
    school = models.CharField(null=True,max_length=64,verbose_name=u'分配单位')
    step_id = models.IntegerField(blank=True, null=True,default=0,verbose_name=u'当前步骤')
    proposer = models.CharField(null=True,max_length=64,verbose_name=u'申请人ID')
    proposer_name = models.CharField(null=True,max_length=64,verbose_name=u'申请人姓名')
    description = models.CharField(null=True,max_length=128,verbose_name=u'简单描述')
    remark = models.TextField(null=True,blank=True,verbose_name=u'备注信息')
    form_data = models.TextField(null=True, verbose_name=u'申请筛选数据')
    allocation_data = models.TextField(null=True, verbose_name=u'待分配数据')
    kemans_data = models.TextField(null=True, verbose_name=u'最佳聚类的数据')
    target_data = models.TextField(null=True, verbose_name=u'最终分配结果数据')
    create_date  = models.CharField(null=True,max_length=100, verbose_name=u'创建时间')
    end_date  = models.CharField(null=True,max_length=100, verbose_name=u'结束时间')

    def __str__(self):
        return self.keyword

    class Meta:
        db_table = 'work_order'
        verbose_name = u'分配流程工單'

class Auth_Work(models.Model):
    status_id = models.IntegerField(default=1,verbose_name=u'工单状态')
    school = models.CharField(null=True,max_length=64,verbose_name=u'所在单位')
    step = models.IntegerField(blank=True, null=True,default=0,verbose_name=u'当前步骤')
    proposer = models.CharField(null=True,unique=True,max_length=64,verbose_name=u'申请人ID')
    proposer_name = models.CharField(null=True,max_length=64,verbose_name=u'申请人姓名')
    professional = models.CharField(null=True,max_length=64,verbose_name=u'申请人职业')
    remark = models.TextField(null=True,blank=True,verbose_name=u'备注信息')
    create_date  = models.CharField(null=True,max_length=100, verbose_name=u'创建时间')

    def __str__(self):
        return self.proposer_name

    class Meta:
        db_table = 'auth_work'
        verbose_name = u'权限申请流程工單'

# class Space_Instance(models.Model):
#     '''
#     资源空间，宿舍资源等
#     '''
#     user_name = models.CharField(max_length=64,unique=True, verbose_name=u'空间所有者')
#     four_room = models.IntegerField(default=0,verbose_name=u'四人间')
#     six_room = models.IntegerField(default=0,verbose_name=u'六人间')
#     eight_room = models.IntegerField(default=0,verbose_name=u'八人间')
#     ten_room = models.IntegerField(default=0,verbose_name=u'十人间')

#     class Meta:
#         db_table = 'space_instance'
#         verbose_name = u'宿舍资源控制'