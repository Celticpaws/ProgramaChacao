# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import signals
from django.core.validators import RegexValidator
from datetime import datetime, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
import os
import time
# Create your models here.

class Telefono(models.Model):
    regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El telefono debe estar en formato: '+999999999'.")
    number = models.CharField(validators=[regex], max_length=15, blank=True) # validators should be a list

    def __str__(self):
    	return str(self.phone_number)

class Joven(models.Model):
	cedula = models.IntegerField(default=0)
	primer_nombre = models.CharField(max_length=30)
	segundo_nombre = models.CharField(max_length=30,blank=True)
	primer_apellido = models.CharField(max_length=30,blank=True)
	segundo_apellido = models.CharField(max_length=30,blank=True)
	gen = models.CharField(max_length=1)
	f_nac = models.CharField(max_length=30,blank=True)
	f_promesa = models.CharField(max_length=30,blank=True)
	unidad = models.CharField(max_length=30,blank=True)
	adelanto = models.CharField(max_length=30,blank=True)
	grupo = models.CharField(max_length=30,blank=True)
	distrito = models.CharField(max_length=30,blank=True)
	region = models.CharField(max_length=30,blank=True)
	celular = models.CharField(max_length=30,blank=True)
	tel_local = models.CharField(max_length=30,blank=True)
	correo = models.EmailField(max_length=70,blank=True)
	direccion = models.CharField(max_length=150,blank=True)

	def __str__(self):
		return str(self.id)+" - "+self.primer_nombre+" "+self.primer_apellido+" - "+self.unidad+" - "+self.grupo+" "

class Adulto(models.Model):
	cedula = models.IntegerField(default=0)
	primer_nombre = models.CharField(max_length=30)
	segundo_nombre = models.CharField(max_length=30)
	primer_apellido = models.CharField(max_length=30)
	segundo_apellido = models.CharField(max_length=30)
	gen = models.CharField(max_length=1)
	f_nac = models.DateField(default=datetime.now)
	f_promesa = models.DateField(default=datetime.now, blank=True)
	unidad = models.CharField(max_length=30)
	cargo = models.CharField(max_length=30)
	n_capacit = models.CharField(max_length=30)
	grupo = models.CharField(max_length=30)
	distrito = models.CharField(max_length=30)
	region = models.CharField(max_length=30)
	celular = models.ForeignKey('Telefono',related_name='a_celular',null=True)
	tel_local = models.ForeignKey('Telefono',related_name='a_te_local',null=True)
	correo = models.EmailField(max_length=70,blank=True)
	direccion = models.CharField(max_length=150)

class Grupo(models.Model):
	grupo = models.CharField(max_length=3)
	usuario = models.ForeignKey('auth.User')

class Evento (models.Model):
	certificado = models.ForeignKey('Certificado')
	nombre = models.CharField(max_length=50)

	def __str__(self):
		return str(self.nombre)

class Certificado(models.Model):
	codigo = models.CharField(max_length=30)
	razon = models.CharField(max_length=50)
	def __str__(self):
		return str(self.razon)

class Participante(models.Model):
	dnis = models.IntegerField(default=0)
	nombre = models.CharField(max_length=120)
	evento = models.CharField(max_length=100)
	numero = models.CharField(max_length=3)

	def __str__(self):
		return self.nombre+" "+str(self.evento)