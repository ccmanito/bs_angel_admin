# -*-coding:utf-8 -*-
from django.db import models


class UserAuth(models.Model):
    u_id =  models.IntegerField(default=0) # 作为userinfo表的外键
    identity_type = models.CharField(max_length=20, verbose_name=u'身份类型')
    identifier = models.CharField(max_length=20, verbose_name=u'身份唯一标示，登录的账号（手机号，邮箱，第三方唯一标示')
    credential = models.CharField(max_length=100, verbose_name=u'授权凭证 （密码，第三方登录的token）')
    verified = models.BooleanField(default=False, verbose_name=u'是否已经验证')
    
    def __str__(self):
        return self.name
    
    #定义元选项
    class Meta:
        db_table='user_auths' #指定UserAuth生成的数据表名为user_auths

class UserInfo(models.Model):
    '''
    u_id在系统中全局唯一
    '''
    u_id = models.AutoField(primary_key=True)
    roles = models.IntegerField(default=1)
    nickname = models.CharField(max_length=100, verbose_name=u'昵称')
    sex = models.CharField(default='男', max_length=20)
    email = models.CharField(max_length=50, null=True)
    mobile = models.CharField(max_length=20, null=True)
    github = models.CharField(max_length=20, null=True)
    avatar = models.CharField(max_length=2048, null=True, verbose_name=u'头像')
    school = models.CharField(max_length=20, null=True)
    college = models.CharField(max_length=20, null=True, verbose_name=u'学院')
    major = models.CharField(max_length=20, null=True, verbose_name=u'专业')
    grade = models.CharField(max_length=20, null=True, verbose_name=u'年级')
    classname = models.CharField(max_length=20, null=True, verbose_name=u'班级')
    professional = models.CharField(max_length=20, null=True, verbose_name=u'职业')
    interests = models.TextField(null=True, verbose_name=u'兴趣爱好')
    livinghabits = models.TextField(null=True, verbose_name=u'生活习惯')
    dorm_id = models.IntegerField(null=True, verbose_name=u'宿舍ID')
    status = models.IntegerField(null=True, verbose_name=u'宿舍分配状态（（0待分配,1分配中,2 已分配））')
    createtime = models.CharField(max_length=100, verbose_name=u'创建时间')


    def __str__(self):
        return self.name
        
    class Meta:
        db_table='user_info'
