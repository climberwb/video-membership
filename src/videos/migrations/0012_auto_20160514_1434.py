# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-14 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0011_auto_20160506_1514'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-title', 'timestamp']},
        ),
        migrations.AddField(
            model_name='video',
            name='order',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
