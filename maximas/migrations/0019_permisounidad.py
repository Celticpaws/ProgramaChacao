# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 00:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maximas', '0018_auto_20170602_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermisoUnidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manada_masculina', models.BooleanField(default=False)),
                ('manada_femenina', models.BooleanField(default=False)),
                ('tropa_masculina', models.BooleanField(default=False)),
                ('tropa_femenina', models.BooleanField(default=False)),
                ('clan_masculina', models.BooleanField(default=False)),
                ('clan_femenina', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]