# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-11 14:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_auto_20160510_2041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='unread',
        ),
    ]
