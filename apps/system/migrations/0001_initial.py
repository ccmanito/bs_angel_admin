# Generated by Django 2.0.2 on 2019-04-18 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True, verbose_name='兴趣爱好title')),
                ('key', models.CharField(max_length=20, null=True, unique=True, verbose_name='唯一键')),
            ],
            options={
                'db_table': 'angel_interest',
            },
        ),
    ]
