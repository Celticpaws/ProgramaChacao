# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 14:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maximas', '0004_auto_20170527_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='adulto',
            name='dnis',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='joven',
            name='dnis',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='joven',
            name='celular',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='j_celular', to='maximas.Telefono'),
        ),
        migrations.AlterField(
            model_name='joven',
            name='f_nac',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='joven',
            name='f_promesa',
            field=models.DateField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='joven',
            name='tel_local',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='j_te_local', to='maximas.Telefono'),
        ),
    ]
