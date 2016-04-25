# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-25 20:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_auto_20160425_1957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='videos',
        ),
        migrations.AddField(
            model_name='video',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='videos.Category'),
        ),
    ]
