# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 23:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maximas', '0012_auto_20170531_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='cip',
            name='nivel',
            field=models.CharField(choices=[('Grupal', 'Grupal'), ('Distrital', 'Distrital'), ('Regional', 'Regional'), ('Nacional', 'Nacional')], default=0, max_length=10),
            preserve_default=False,
        ),
    ]
