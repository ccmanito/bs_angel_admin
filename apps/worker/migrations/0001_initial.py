# Generated by Django 2.0.2 on 2019-05-03 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Work_Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=64, unique=True, verbose_name='关键字')),
                ('status_id', models.IntegerField(default=1, verbose_name='工单状态')),
                ('step_id', models.IntegerField(blank=True, default=1, null=True, verbose_name='当前步骤')),
                ('proposer', models.CharField(max_length=64, null=True, verbose_name='申请人ID')),
                ('proposer_name', models.CharField(max_length=64, null=True, verbose_name='申请人姓名')),
                ('description', models.CharField(max_length=128, null=True, verbose_name='简单描述')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注信息')),
                ('form_data', models.TextField(null=True, verbose_name='申请筛选数据')),
                ('allocation_data', models.TextField(null=True, verbose_name='待分配数据')),
                ('target_data', models.TextField(null=True, verbose_name='最终分配结果数据')),
                ('create_date', models.CharField(max_length=100, null=True, verbose_name='创建时间')),
                ('end_date', models.CharField(max_length=100, null=True, verbose_name='结束时间')),
            ],
            options={
                'verbose_name': '分配流程工單',
                'db_table': 'work_order',
            },
        ),
    ]
