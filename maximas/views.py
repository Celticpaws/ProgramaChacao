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

def definegrupo(g):
	if g == "STA":
		return "SANTO TOMAS DE AQUINO"
	if g == "PLE":
		return "PLEYADES"
	if g == "ROR":
		return "RORAIMA"
	if g == "TIU":
		return "TIUNA"
	if g == "DON":
		return "DON BOSCO"
	if g == "CAT":
		return "CATATUMBO"
def defineunidad(unidad):
	if unidad == "MM":
		return 'Manada Masculina'
	elif unidad == "MF":
		return 'Manada Femenina'
	elif unidad == "TM":
		return 'Tropa Masculina'
	elif unidad == "TF":
		return 'Tropa Femenina'
	elif unidad == "CF":
		return 'Clan Femenino'
	elif unidad == "CM":
		return 'Clan Masculino'

def undefineunidad(unidad):
	if unidad == 'Manada Masculina':
		return 'MM'
	elif unidad == 'Manada Femenina':
		return 'MF'
	elif unidad == 'Tropa Masculina':
		return 'TM'
	elif unidad == "Tropa Femenina":
		return 'TF'
	elif unidad == "Clan Femenino":
		return 'CF'
	elif unidad == "Clan Masculino":
		return 'CM'


def login(request, method='POST'):
	form = RegisterForm()
	if request.user.is_authenticated():
		g = Grupo.objects.get(usuario=request.user).grupo
		return redirect(g+"/metas/")
	elif request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None and user.is_active:
			auth.login(request, user)
			g = Grupo.objects.get(usuario=user).grupo
			return redirect(g+"/metas/")
		else:
			return render(request, "login.html", {})
	else:
		return render(request, "login.html", {})

@login_required(login_url ='/')
def cuadrosmetasunidad(request,grupo,unidad):
	g = definegrupo(Grupo.objects.get(usuario=request.user).grupo)
	grupo =  definegrupo(grupo)
	if (grupo == g):
		u = defineunidad(unidad)
		try:
			ano = int(request.GET['a'])
		except:
			ano = datetime.today().year
		jovenes = Joven.objects.filter(grupo=grupo,unidad=u)
		hoy = datetime.today().replace(year=ano)
		iniano = hoy.replace(month=1,day=1)
		finano = hoy.replace(month=12,day=31)
		futuro = datetime.today() + timedelta(days=1826)
		edades=[]
		porcentajes = []
		fechas=[]
		adelantos=[]
		for j in jovenes:
			try:
				nacimiento = datetime.strptime(j.f_nac, '%d/%m/%Y')
			except:
				nacimiento = hoy
			try:
				ingreso = datetime.strptime(j.f_promesa, '%d/%m/%Y')
			except:
				ingreso = datetime.today()
			edades.append((hoy - nacimiento).days/365)
			if j.unidad == 'Manada Femenina' or j.unidad =='Manada Masculina':
				egreso = nacimiento + timedelta(days=4012)
				lleva= (hoy-ingreso)
				quedan = (egreso-hoy)
				vidaenmanada = lleva + quedan
				lobato = ingreso + timedelta(days=vidaenmanada.days*0.07)
				fresca = ingreso + timedelta(days=vidaenmanada.days*0.28)
				alerta = ingreso + timedelta(days=vidaenmanada.days*0.53)
				agil = ingreso + timedelta(days=vidaenmanada.days*0.70)
				libre = ingreso + timedelta(days=vidaenmanada.days*0.87)
				ls = ingreso + timedelta(days=vidaenmanada.days*0.95)
				fec = [ingreso,lobato,fresca,alerta,agil,libre,ls,egreso]
				p =[]
				acc = 0.00
				if vidaenmanada.days > 0:
					for f in fec:
						if f >=iniano and f <= finano:
							pen = float((f-iniano).days)*100/float((finano-iniano).days)
							agr = pen-acc
							p.append(agr)
							acc = pen
						else:
							if f<iniano:
								agr= 0
								p.append(agr)
							else:
								if acc!=100.00 :
									agr = 100.00-acc
									p.append(agr)
									acc = 100
								else:
									agr = 0
									p.append(agr)
				else:
					for f in fec:
						p.append(0)
				porcentajes.append(p)
				fechas.append([nacimiento,egreso])
			if j.unidad == 'Tropa Femenina' or j.unidad =='Tropa Masculina':
				egreso = nacimiento + timedelta(days=5840)
				lleva= (hoy-ingreso)
				quedan = (egreso-hoy)
				vidaentropa = lleva + quedan
				aventurero = ingreso + timedelta(days=vidaentropa.days*0.05)
				explorador = ingreso + timedelta(days=vidaentropa.days*0.55)
				pionero = ingreso + timedelta(days=vidaentropa.days*0.90)
				sb = ingreso + timedelta(days=vidaentropa.days*0.95)
				fec = [ingreso,aventurero,explorador,pionero,sb,egreso]
				p =[]
				acc = 0.00
				if vidaentropa.days > 0:
					for f in fec:
						if f >=iniano and f <= finano:
							pen = float((f-iniano).days)*100/float((finano-iniano).days)
							agr = pen-acc
							p.append(agr)
							acc = pen
						else:
							if f<iniano:
								agr= 0
								p.append(agr)
							else:
								if acc!=100.00 :
									agr = 100.00-acc
									p.append(agr)
									acc = 100
								else:
									agr = 0
									p.append(agr)
				else:
					for f in fec:
						p.append(0)
				porcentajes.append(p)
				fechas.append([nacimiento,egreso])
			if j.unidad == 'Clan Femenino' or j.unidad =='Clan Masculino':
				egreso = nacimiento + timedelta(days=7665)
				lleva= (hoy-ingreso)
				quedan = (egreso-hoy)
				vidaenclan = lleva + quedan
				precursor = ingreso + timedelta(days=vidaenclan.days*0.01)
				expedicionario = ingreso + timedelta(days=vidaenclan.days*0.31)
				descubridor = ingreso + timedelta(days=vidaenclan.days*0.61)
				fundador = ingreso + timedelta(days=vidaenclan.days*0.91)
				rc = ingreso + timedelta(days=vidaenclan.days)
				fec = [ingreso,precursor,expedicionario,descubridor,fundador,rc]
				p =[]
				acc = 0.00
				if vidaenclan.days > 0:
					for f in fec:
						if f >=iniano and f <= finano:
							pen = float((f-iniano).days)*100/float((finano-iniano).days)
							agr = pen-acc
							p.append(agr)
							acc = pen
						else:
							if f<iniano:
								agr= 0
								p.append(agr)
							else:
								if acc!=100.00 :
									agr = 100.00-acc
									p.append(agr)
									acc = 100
								else:
									agr = 0
									p.append(agr)
				else:
					for f in fec:
						p.append(0)
				porcentajes.append(p)
				fechas.append([nacimiento,egreso])
			adelantos.append(fec)
		return render(request, 'cuadrometasunidad.html', 
			{'jovenes':zip(jovenes,edades,porcentajes,fechas,adelantos),'hoy':hoy,'futuro':futuro,'g':grupo,'u':u,'unidad':unidad})
	else:
		return render(request, '404.html', {})

@login_required(login_url ='/')
def cuadrosmetas(request,grupo):
	g =  definegrupo(grupo)
	grupo = definegrupo(Grupo.objects.get(usuario=request.user).grupo)

	if (grupo == g):
		unidades = Joven.objects.filter(grupo=g).values("unidad").distinct().order_by('unidad')
		u = []
		for x in unidades:
			u.append(undefineunidad(x['unidad']))
		adelantos =['Cachorro','Huella Fresca','Huella Alerta','Huella Agil','Huella Libre','Lobo Saltarin','Novicio','Aventurero','Explorador','Pionero','Scout de Bolivar','Novato','Precursor','Expedicionario','Descubridor','Fundador','Rover Ciudadano']
		can = []
		for a in adelantos:
			can.append(Joven.objects.filter(adelanto=a,grupo=g).count())
		resumen= zip(adelantos,can)
		return render(request, 'cuadrometasgrupo.html', 
			{'resumen':resumen,'unidades':zip(unidades,u),'g':grupo,'grupo':g})
	else:
		return render(request, '404.html', {})

@login_required(login_url ='/')
def cipgrupo(request,grupo):
	g =  definegrupo(grupo)
	grupo = definegrupo(Grupo.objects.get(usuario=request.user).grupo)

	if (grupo == g):
		unidades = Joven.objects.filter(grupo=g).values("unidad").distinct().order_by('unidad')
		u = []
		for x in unidades:
			u.append(undefineunidad(x['unidad']))
		manada = CIP.objects.filter(unidad='M').order_by('nivel')
		tropa = CIP.objects.filter(unidad='T').order_by('nivel')
		clan = CIP.objects.filter(unidad='C').order_by('nivel')
		general = CIP.objects.filter(unidad='G').order_by('nivel')
		
		jovenesmanada = Joven.objects.values_list('pk',flat=True).filter(grupo=g,unidad__in=['Manada Masculina','Manada Femenina'])
		jovenestropa = Joven.objects.values_list('pk',flat=True).filter(grupo=g,unidad__in=['Tropa Masculina','Tropa Femenina'])
		jovenesclan = Joven.objects.values_list('pk',flat=True).filter(grupo=g,unidad__in=['Clan Masculino','Clan Femenino'])
		jovenesgeneral = Joven.objects.values_list('pk',flat=True).filter(grupo=g)

		listmanada=[]
		for x in manada:
			listmanada.append(Participante.objects.filter(dnis__in=jovenesmanada,evento=x.nombre).count())
		listtropa=[]
		for x in tropa:
			listtropa.append(Participante.objects.filter(dnis__in=jovenestropa,evento=x.nombre).count())
		listclan=[]
		for x in clan:
			listclan.append(Participante.objects.filter(dnis__in=jovenesclan,evento=x.nombre).count())
		listgeneral=[]
		for x in general:
			listgeneral.append(Participante.objects.filter(dnis__in=jovenesgeneral,evento=x.nombre).count())
		return render(request, 'cipgrupo.html', 
			{'unidades':zip(unidades,u),'g':grupo,'grupo':g,'manada':zip(manada,listmanada),'tropa':zip(tropa,listtropa),'clan':zip(clan,listclan),'general':zip(general,listgeneral),})
	else:
		return render(request, '404.html', {})

@login_required(login_url ='/')
def cipunidad(request,grupo,unidad):
	g =  definegrupo(grupo)
	gru = definegrupo(Grupo.objects.get(usuario=request.user).grupo)
	if (gru == g):
		gr = definegrupo(grupo)
		u = defineunidad(unidad)
		jovenes = Joven.objects.filter(grupo=gr,unidad=u)
		if unidad == "MM" or unidad == "MF":
			grupal = CIP.objects.filter(unidad='G') 
			distrital = CIP.objects.filter(unidad='M',nivel ="Distrital")
			regional = CIP.objects.filter(unidad='M',nivel ="Regional")
			nacional = CIP.objects.filter(unidad='M',nivel ="Nacional") 
		elif unidad == "TM" or unidad == "TF":
			grupal = CIP.objects.filter(unidad='G')
			distrital = CIP.objects.filter(unidad='T',nivel ="Distrital")
			regional = CIP.objects.filter(unidad='T',nivel ="Regional")
			nacional = CIP.objects.filter(unidad='T',nivel ="Nacional")
		elif unidad == "CM" or unidad == "CF":
			grupal = CIP.objects.filter(unidad='G')
			distrital = CIP.objects.filter(unidad='C',nivel ="Distrital")
			regional = CIP.objects.filter(unidad='C',nivel ="Regional")
			nacional = CIP.objects.filter(unidad='C',nivel ="Nacional")
		listado = []
		for j in jovenes:
			listagrupo = []
			for g in grupal:
				try:
					p = Participante.objects.get(evento=g.nombre,dnis=j.id)
					e = Certificado.objects.get(razon=p.evento)
					listagrupo.append([p.numero,e.codigo])
				except:
					listagrupo.append([0,0])
			for g in distrital:
				try:
					p = Participante.objects.get(evento=g.nombre,dnis=j.id)
					e = Certificado.objects.get(razon=p.evento)
					listagrupo.append([p.numero,e.codigo])
				except:
					listagrupo.append([0,0])
			for g in regional:
				try:
					p = Participante.objects.get(evento=g.nombre,dnis=j.id)
					e = Certificado.objects.get(razon=p.evento)
					listagrupo.append([p.numero,e.codigo])
				except:
					listagrupo.append([0,0])
			for g in nacional:
				try:
					p = Participante.objects.get(evento=g.nombre,dnis=j.id)
					e = Certificado.objects.get(razon=p.evento)
					listagrupo.append([p.numero,e.codigo])
				except:
					listagrupo.append([0,0])
			listado.append(listagrupo)
		return render(request,'cipunidad.html',{'g':gr,'u':u,'jovenes':zip(jovenes,listado),'grupal':grupal,'distrital':distrital,'regional':regional,'nacional':nacional})
	else:
		return render(request, '404.html', {})

def certificados(request,codigo):
	certificado = Certificado.objects.get(codigo=codigo)
	evento = Evento.objects.get(certificado=certificado)
	participantes = Participante.objects.filter(evento=evento.nombre)
	return render(request,'certificados.html',{'certificado':certificado,'evento':evento,'participantes':participantes})

def certificadoindividual(request,evento,nombre):
    evento = Evento.objects.get(certificado__codigo=evento)
    participante = Participante.objects.get(numero=nombre)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "filename='"+evento.certificado.codigo+"-"+participante.numero+".pdf'"
    
    logo = ImageReader("static/certificados/"+evento.certificado.codigo+".jpg")
    
    p = canvas.Canvas(response,pagesize=landscape(letter))
    w, h = landscape(letter)
    p.drawImage(logo, 0,0,width=w,height=h) 
    p.setFillColorRGB(0.2,0.5,0.3)
    p.setFont("Helvetica-Bold",48)
    p.drawCentredString(w/2, h/2-50, participante.primer_nombre.upper()+" "+participante.primer_apellido.upper())
    p.setFillColorRGB(1,1,1)
    p.setFont("Helvetica",12)
    p.drawCentredString(w/2+300, h/2-250, evento.certificado.codigo+"-"+participante.numero)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
