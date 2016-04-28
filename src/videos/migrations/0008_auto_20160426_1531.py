# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0007_auto_20160426_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='video',
            unique_together=set([('slug', 'category')]),
        ),
    ]