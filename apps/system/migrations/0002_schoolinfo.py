# Generated by Django 2.0.2 on 2019-04-29 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=100, null=True, unique=True, verbose_name='学校名称')),
                ('college', models.CharField(max_length=1000, null=True, verbose_name='学院集合')),
                ('major', models.CharField(max_length=1000, null=True, verbose_name='专业集合')),
                ('grade', models.CharField(max_length=1000, null=True, verbose_name='年级集合')),
                ('classname', models.CharField(max_length=1000, null=True, verbose_name='班级集合')),
            ],
            options={
                'db_table': 'school_info',
            },
        ),
    ]