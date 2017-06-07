# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 22:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maximas', '0019_permisounidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParticipanteCIP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dnis', models.IntegerField(default=0)),
                ('primer_nombre', models.CharField(max_length=120)),
                ('segundo_nombre', models.CharField(max_length=120)),
                ('primer_apellido', models.CharField(max_length=120)),
                ('segundo_apellido', models.CharField(max_length=120)),
                ('evento', models.CharField(max_length=100)),
                ('numero', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='ParticipanteCursos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dnis', models.IntegerField(default=0)),
                ('primer_nombre', models.CharField(max_length=120)),
                ('segundo_nombre', models.CharField(max_length=120)),
                ('primer_apellido', models.CharField(max_length=120)),
                ('segundo_apellido', models.CharField(max_length=120)),
                ('evento', models.CharField(max_length=100)),
                ('numero', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='ParticipanteProgramasMundiales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dnis', models.IntegerField(default=0)),
                ('primer_nombre', models.CharField(max_length=120)),
                ('segundo_nombre', models.CharField(max_length=120)),
                ('primer_apellido', models.CharField(max_length=120)),
                ('segundo_apellido', models.CharField(max_length=120)),
                ('evento', models.CharField(max_length=100)),
                ('numero', models.CharField(max_length=3)),
            ],
        ),
    ]
