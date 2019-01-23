# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-11-25 13:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20181125_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(1, '男'), (2, '女'), (3, '中间的')], default=1, null=True),
        ),
    ]
