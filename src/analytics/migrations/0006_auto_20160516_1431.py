# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-16 14:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('analytics', '0005_auto_20160516_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='pageview',
            name='primary_content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primary_obj', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='pageview',
            name='primary_object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pageview',
            name='secondary_content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secondary_obj', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='pageview',
            name='secondary_object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pageview',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 16, 14, 31, 19, 828017, tzinfo=utc)),
        ),
    ]
