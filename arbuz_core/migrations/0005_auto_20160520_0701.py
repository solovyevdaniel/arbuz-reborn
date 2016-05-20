# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-20 07:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arbuz_core', '0004_auto_20160520_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminuser',
            name='is_activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='adminuser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='adminuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]