# -*-coding:utf-8 -*-
from django.db import models


class UserAuth(models.Model):
    u_id =  models.IntegerField(default=0) # 作为userinfo表的外键
    identity_type = models.CharField(max_length=20) # 身份类型（站内username 邮箱email 手机mobile 或者第三方的qq weibo weixin等等）
    identifier = models.CharField(max_length=20) # 身份唯一标示，登录的账号（手机号，邮箱，第三方唯一标示）
    credential = models.CharField(max_length=100) # 授权凭证 （密码，第三方登录的token）
    createtime = models.CharField(max_length=100) # 创建时间
    verified = models.BooleanField(default=False)   # 是否已经验证（存储 1、0 来区分是否已经验证通过）
    
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
    nickname = models.CharField(max_length=100) #昵称
    sex = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=20)
    github = models.CharField(max_length=20)
    avatar = models.CharField(max_length=2048) #头像
    school = models.CharField(max_length=20)
    college = models.CharField(max_length=20)
    major = models.CharField(max_length=20)
    grade = models.CharField(max_length=20)
    classname = models.CharField(max_length=20)
    professional = models.CharField(max_length=20)
    interests = models.TextField()
    livinghabits = models.TextField()


    def __str__(self):
        return self.name
        
    class Meta:
        db_table='user_info'


