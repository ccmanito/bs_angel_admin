# Generated by Django 2.0.2 on 2019-05-04 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0002_work_order_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='work_order',
            name='kemans_data',
            field=models.TextField(null=True, verbose_name='最佳聚类的数据'),
        ),
    ]
