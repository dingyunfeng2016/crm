# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-12-01 20:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_auto_20181130_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='deal_date',
            field=models.DateField(blank=True, null=True, verbose_name='成交日期'),
        ),
    ]
