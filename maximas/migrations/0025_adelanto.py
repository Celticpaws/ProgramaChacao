# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 22:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maximas', '0024_auto_20170606_2351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adelanto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insignia', models.CharField(choices=[('LO', 'Lobato/Lobezna'), ('HF', 'Huella Fresca'), ('HA', 'Huella Alerta'), ('HG', 'Huella Agil'), ('HL', 'Huella Libre'), ('LS', 'Lobo Saltarin'), ('NO', 'Novicio'), ('AV', 'Aventurero'), ('EX', 'Explorador'), ('PI', 'Pionero'), ('SB', 'Scout de Bolivar'), ('NV', 'Novato'), ('PR', 'Precursor'), ('EP', 'Expedicionario'), ('DE', 'Descubridor'), ('FU', 'Fundador'), ('RC', 'Rover Ciudadano')], max_length=2)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='joven', to='maximas.Joven')),
            ],
        ),
    ]