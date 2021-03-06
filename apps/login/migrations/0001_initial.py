# Generated by Django 2.0.2 on 2019-04-17 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAuth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_id', models.IntegerField(default=0)),
                ('identity_type', models.CharField(max_length=20, verbose_name='身份类型')),
                ('identifier', models.CharField(max_length=20, verbose_name='身份唯一标示，登录的账号（手机号，邮箱，第三方唯一标示')),
                ('credential', models.CharField(max_length=100, verbose_name='授权凭证 （密码，第三方登录的token）')),
                ('verified', models.BooleanField(default=False, verbose_name='是否已经验证')),
            ],
            options={
                'db_table': 'user_auths',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('u_id', models.AutoField(primary_key=True, serialize=False)),
                ('roles', models.IntegerField(default=1)),
                ('name', models.CharField(max_length=100, verbose_name='昵称')),
                ('sex', models.CharField(default='男', max_length=20)),
                ('email', models.CharField(max_length=50, null=True)),
                ('mobile', models.CharField(max_length=20, null=True)),
                ('github', models.CharField(max_length=20, null=True)),
                ('avatar', models.CharField(max_length=2048, null=True, verbose_name='头像')),
                ('school', models.CharField(max_length=20, null=True)),
                ('college', models.CharField(max_length=20, null=True, verbose_name='学院')),
                ('major', models.CharField(max_length=20, null=True, verbose_name='专业')),
                ('grade', models.CharField(max_length=20, null=True, verbose_name='年级')),
                ('classname', models.CharField(max_length=20, null=True, verbose_name='班级')),
                ('professional', models.CharField(max_length=20, null=True, verbose_name='职业')),
                ('interests', models.TextField(null=True, verbose_name='兴趣爱好')),
                ('livinghabits', models.TextField(null=True, verbose_name='生活习惯')),
                ('dorm_id', models.IntegerField(null=True, verbose_name='宿舍ID')),
                ('status', models.IntegerField(null=True, verbose_name='宿舍分配状态（（0待分配,1分配中,2 已分配））')),
                ('createtime', models.CharField(max_length=100, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'user_info',
            },
        ),
    ]
