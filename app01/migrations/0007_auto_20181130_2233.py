# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-11-30 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_customer_class_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='手机号'),
        ),
    ]