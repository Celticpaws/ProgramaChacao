# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 23:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maximas', '0021_auto_20170606_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='permisounidad',
            name='imagen',
            field=models.CharField(default='PLE-MM', max_length=6),
        ),
    ]
