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

	def __unicode__(self):
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

	def __str__(self):
		return str(self.grupo)


class Evento (models.Model):
	certificado = models.ForeignKey('Certificado')
	nombre = models.CharField(max_length=50)

	def __str__(self):
		return str(self.nombre)

class Condecoraciones(models.Model):
	con = (
		('NPB','Nudo de Perseverancia en Bronce'),('NPP','Nudo de Perseverancia en Plata'), ('NPO','Nudo de Perseverancia en Oro'),
		('BESP','Barra de Espiritud Scout en Plata'), ('BESO','Barra de Espiritud Scout en Oro'),
		('BV','Barra Vinotinto'),('OM1','Orden al Merito Primera Clase'),('OM2','Orden al Segunda Clase'),('OSJ','Orden de San Jorge')) 
	dnis = models.IntegerField(default=0)
	condecoracion = models.CharField(max_length=4,choices=con)
	fecha_entrega = models.DateField(default=datetime.now)
	numero = models.IntegerField(default=0)

	def __str__(self):
		return self.condecoracion+" - "+str(self.dnis)


	def __unicode__(self):
		return self.condecoracion+" - "+str(self.dnis)

class CIP (models.Model):
	unidades = (
    ('M','M'), ('T','T'),  ('C','C'), ('G','G')) 
	nivel = (
    ('Grupal','Grupal'),    ('Distrital','Distrital'),
    ('Regional','Regional'),    ('Nacional','Nacional'),) 

	certificado = models.ForeignKey('Certificado',null=True,blank=True)
	nombre = models.CharField(max_length=50)
	fecha = models.DateField()
	nivel = models.CharField(choices=nivel,max_length=10)
	unidad = models.CharField(choices=unidades,max_length=1)

	def __str__(self):
		return self.unidad+" "+self.nombre

	def __unicode__(self):
		return self.unidad+" "+self.nombre

class Certificado(models.Model):
	codigo = models.CharField(max_length=30)
	razon = models.CharField(max_length=50)
	def __str__(self):
		return str(self.razon)

class Participante(models.Model):
	dnis = models.IntegerField(default=0)
	primer_nombre = models.CharField(max_length=120)
	segundo_nombre = models.CharField(max_length=120)
	primer_apellido = models.CharField(max_length=120)
	segundo_apellido = models.CharField(max_length=120)
	evento = models.CharField(max_length=100)
	numero = models.CharField(max_length=3)

class ParticipanteCIP(models.Model):
	dnis = models.IntegerField(default=0)
	evento = models.CharField(max_length=100)
	numero = models.CharField(max_length=3)

class ParticipanteCursos(models.Model):
	dnis = models.IntegerField(default=0)
	evento = models.CharField(max_length=100)
	numero = models.CharField(max_length=3)

class ParticipanteProgramasMundiales(models.Model):
	dnis = models.IntegerField(default=0)
	evento = models.CharField(max_length=100)
	numero = models.CharField(max_length=5)
	fecha = models.DateField(blank=True,null=True)

def __str__(self):
		return self.primer_nombre+" "+self.primer_apellido+" - "+str(self.evento)

def __unicode__(self):
	return self.primer_nombre+" "+self.primer_apellido+" - "+str(self.evento)

class Prueba(models.Model):
	a = (('CA','Cachorro'),('HF','Huella Fresca'),
				('HA','Huella Alerta'),('HG','Huella Agil'),
				('HL','Huella Libre'),('LS','Lobo Saltarin'),
				('NO','Novicio'),('AV','Aventurero'),
				('EX','Explorador'),('PI','Pionero'),
				('SB','Scout de Bolivar'),('NV','Novato'),
				('PR','Precursor'),('EP','Expedicionario'),
				('DE','Descubridor'),('FU','Fundador'),('RC','Rover Ciudadano'))
	unidades = (
    ('M','Manada'), ('T','Tropa'),  ('C','Clan'), ('G','Grupo')) 
	unidad = models.CharField(max_length=1,choices=unidades)
	adelanto = models.CharField(max_length=2,choices=a)
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=200)

	def __str__(self):
		return self.unidad+" "+self.adelanto+" - "+self.nombre

	def __unicode__(self):
		return self.unidad+" "+self.adelanto+" - "+self.nombre

class Logro(models.Model):
	a = (('LO','Lobato/Lobezna'),('HF','Huella Fresca'),
				('HA','Huella Alerta'),('HG','Huella Agil'),
				('HL','Huella Libre'),('LS','Lobo Saltarin'),
				('NO','Novicio'),('AV','Aventurero'),
				('EX','Explorador'),('PI','Pionero'),
				('SB','Scout de Bolivar'),('NV','Novato'),
				('PR','Precursor'),('EP','Expedicionario'),
				('DE','Descubridor'),('FU','Fundador'),('RC','Rover Ciudadano'))
	unidades = (
    ('M','Manada'), ('T','Tropa'),  ('C','Clan'), ('G','Grupo')) 
	dnis = models.IntegerField(default=0)
	prueba = models.ForeignKey('Prueba')

	def __str__(self):
		return str(self.dnis)+" - "+str(self.prueba.pk)

	def __unicode__(self):
			return unicode(self.dnis)+" - "+unicode(self.prueba.pk)

class PermisoUnidad(models.Model):
	usuario = models.ForeignKey('auth.User')
	imagen = models.CharField(max_length=6,default="PLE-MM")
	manada_masculina = models.BooleanField(default=False)
	manada_femenina = models.BooleanField(default=False)
	tropa_masculina = models.BooleanField(default=False)
	tropa_femenina = models.BooleanField(default=False)
	clan_masculina = models.BooleanField(default=False)
	clan_femenina = models.BooleanField(default=False)

	def __str__(self):
			return str(self.usuario)