# -*- coding: utf-8 -*-
from .models import *
from .forms import *
from calendar import monthrange
from datetime import datetime
from django.contrib import *
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import *
from io import StringIO
from reportlab.lib.utils import ImageReader
import urllib
import json
import math
import sys

def defineadelanto (a):
	if a == "LO":
		return "Lobato"
	if a == "HF":
		return "Huella Fresca"
	if a == "HA":
		return "Huella Alerta"
	if a == "HG":
		return "Huella Agil"
	if a == "HL":
		return "Huella Libre"
	if a == "LS":
		return "Lobo Saltarin"
	if a == "AV":
		return "Aventurero"
	if a == "EX":
		return "Explorador"
	if a == "PI":
		return "Pionero"
	if a == "SB":
		return "Scout de Bolivar"
	if a == "PR":
		return "Precursor"
	if a == "EP":
		return "Expedicionario"
	if a == "DE":
		return "Descubridor"
	if a == "FU":
		return "Fundador"
	if a == "RC":
		return "Rover Ciudadano"

def undefineadelanto (a):
	if a == "Lobato":
		return "LO"
	if a == "Huella Fresca":
		return "FR"
	if a == "Huella Alerta":
		return "AL"
	if a == "Huella Agil":
		return "AG"
	if a == "Huella Libre":
		return "LI"
	if a == "Lobo Saltarin":
		return "LS"
	if a == "Aventurero":
		return "AV"
	if a == "Explorador":
		return "EX"
	if a == "Pionero":
		return "PI"
	if a == "Scout de Bolivar":
		return "SB"
	if a == "Precursor":
		return "PR"
	if a == "Expedicionario":
		return "EP"
	if a == "Descubridor":
		return "DE"
	if a == "Fundador":
		return "FU"
	if a == "Rover Ciudadano":
		return "RC"


@login_required(login_url ='/')
def modificaradelantoajax(request):
	try:
		j = int(request.GET['dnis'])
		pr = int(request.GET['p'])
		prueba = Prueba.objects.get(pk=pr)
		if Logro.objects.filter(dnis=j,prueba=prueba).exists():
			logro = Logro.objects.get(dnis=j,prueba=prueba)
			logro.delete()
			resultado = -1
		else:
			logro = Logro.objects.create(dnis=j,prueba=prueba)
			resultado = 1
	except:
		resultado = 0
	return HttpResponse(json.dumps(resultado),content_type='application/json')	

@login_required(login_url ='/')
def adelantarajax(request):
	try:
		j = Joven.objects.get(pk=int(request.GET['dnis']))
		a = request.GET['tipo']
		adelanto = defineadelanto(a)
		logrospasados = Logro.objects.filter(dnis=j.id,prueba__adelanto=undefineadelanto(adelanto))
		print(logrospasados)
		for l in logrospasados:
			l.delete()
		j.adelanto = adelanto
		j.save()
		adelanto = Adelanto.objects.create(usuario=j,insignia=a)
		resultado = 1
	except:
		resultado = 0
	return HttpResponse(json.dumps(resultado),content_type='application/json')	

def desvinculandoajax(request):
	try:
		j = Joven.objects.get(pk=int(request.GET['dnis']))
		unidad = int(request.GET['p'])
		if unidad == 1 and j.gen=='M':
			j.unidad = "Tropa Masculina"
			if j.adelanto == "Lobo Saltarin":
				j.adelanto = "Aventurero"
			else:
				j.adelanto = "Novicio"
		if unidad == 1 and j.gen=='F':
			j.unidad = "Tropa Femenina"
			if j.adelanto == "Lobo Saltarin":
				j.adelanto = "Aventurero"
			else:
				j.adelanto = "Novicio"
		if unidad == 2 and j.gen=='M':
			j.unidad = "Clan Masculino"
			if j.adelanto == "Scout de Bolivar":
				j.adelanto = "Precursor"
			else:
				j.adelanto = "Novato"
		if unidad == 2 and j.gen=='F':
			j.unidad = "Clan Femenino"
			if j.adelanto == "Scout de Bolivar":
				j.adelanto = "Precursor"
			else:
				j.adelanto = "Novato"
		if unidad == 3:
			j.unidad = "Adulto"
		j.save()
		logrospasados = Logro.objects.filter(dnis=j.id)
		for l in logrospasados:
			l.delete()
		especialidades = Especialidades.objects.filter(dnis=j.id)
		for e in especialidades:
			if e.nivel < 3:
				e.delete()
			elif e.nivel == 3:
				e.nivel = 1
				e.save()
		resultado = 1
	except:
		resultado = 0
	return HttpResponse(json.dumps(resultado),content_type='application/json')	

@login_required(login_url ='/')
def modificarespecialidadajax(request):
	# try:
	j = int(request.GET['dnis'])
	tipo = int(request.GET['tipo'])
	cambio = int(request.GET['cambio'])
	try:
		especialidad = Especialidades.objects.get(dnis=j,tipo=tipo-1)
		if especialidad.nivel == 1 and cambio == -1 :
			especialidad.delete()
			resultado = 0
		elif especialidad.nivel == 3 and cambio == 1:
			resultado = -1
		else:
			especialidad.nivel = especialidad.nivel + cambio
			if cambio == 1:
				especialidad.fecha_entrega = datetime.today()
			especialidad.save()
			resultado = especialidad.nivel
	except:
		especialidad = Especialidades.objects.create(dnis=j,tipo=tipo-1,nivel=1,fecha_entrega=datetime.today())
		resultado = 1
	# except:
	# 	resultado = 0
	return HttpResponse(json.dumps(resultado),content_type='application/json')		