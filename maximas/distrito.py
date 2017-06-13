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

from django.contrib.auth.decorators import permission_required

def revisarpermisos(permisos):
	u =  []
	if permisos.manada_masculina:
		u.append('MM')
	if permisos.manada_femenina:
		u.append('MF')
	if permisos.tropa_masculina:
		u.append('TM')
	if permisos.tropa_femenina:
		u.append('TF')
	if permisos.clan_masculina:
		u.append('CM')
	if permisos.clan_femenina:
		u.append('CF')
	return u

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

def undefinegrupo(g):
	if g == "SANTO TOMAS DE AQUINO":
		return "STA"
	if g == "PLEYADES":
		return "PLE"
	if g == "RORAIMA":
		return "ROR"
	if g == "TIUNA":
		return "TIU"
	if g == "DON BOSCO":
		return "DON"
	if g == "CATATUMBO":
		return "CAT"

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


@permission_required('is_staff',login_url ='/')
def cuadrosmetasd(request):
	u = ['MM','MF','TM','TF','CM','CF']
	permisos = PermisoUnidad.objects.get(usuario=request.user)
	grupos = ['PLEYADES','RORAIMA','TIUNA','SANTO TOMAS DE AQUINO','DON BOSCO','CATATUMBO']
	unidades = []
	jovenesdistrito = []
	for gr in grupos: 
		jovenestotal = []
		jovenesto = []
		for x in u:
			un = defineunidad(x)
			try:
				ano = int(request.GET['a'])
			except:
				ano = datetime.today().year
			jovenes = Joven.objects.filter(grupo=gr,unidad=un)
			jovenesto.append(jovenes)
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
			jovenestotal.append([zip(jovenes,edades,porcentajes,fechas,adelantos),x,un])
		jovenesdistrito.append([gr,jovenestotal])
	return render(request, 'distrito-cuadrometas.html', 
			{'fotoperfil':permisos.imagen,'unidades':zip(unidades,u),'jovenesdistrito':jovenesdistrito,'hoy':hoy,'futuro':futuro})
	
@login_required(login_url ='/')
def cipd(request,grupo):
	g =  definegrupo(grupo)
	permisos = PermisoUnidad.objects.get(usuario=request.user)
	u = revisarpermisos(permisos)
	unidades = []
	gru = definegrupo(Grupo.objects.get(usuario=request.user).grupo)
	gr = definegrupo(grupo)
	if (gru == g):
		listadogtotal = []
		listadodtotal = []
		listadorntotal = []
		grupaltotal = []
		distritaltotal = []
		regionaltotal = []
		nacionaltotal = []
		for x in u:
			un = defineunidad(x)
			unidades.append(defineunidad(x))
			jovenes = Joven.objects.filter(grupo=gr,unidad=un)
			if x == "MM" or x == "MF":
				grupal = CIP.objects.filter(unidad='G') 
				distrital = CIP.objects.filter(unidad='M',nivel ="Distrital")
				regional = CIP.objects.filter(unidad='M',nivel ="Regional")
				nacional = CIP.objects.filter(unidad='M',nivel ="Nacional") 
			elif x == "TM" or x == "TF":
				grupal = CIP.objects.filter(unidad='G')
				distrital = CIP.objects.filter(unidad='T',nivel ="Distrital")
				regional = CIP.objects.filter(unidad='T',nivel ="Regional")
				nacional = CIP.objects.filter(unidad='T',nivel ="Nacional")
			elif x == "CM" or x == "CF":
				grupal = CIP.objects.filter(unidad='G')
				distrital = CIP.objects.filter(unidad='C',nivel ="Distrital")
				regional = CIP.objects.filter(unidad='C',nivel ="Regional")
				nacional = CIP.objects.filter(unidad='C',nivel ="Nacional")
			listadog = []
			listadod = []
			listadorn = []
			for j in jovenes:
				listagrupo = []
				listadistrito=[]
				listaregnac=[]
				for g in grupal:
					try:
						p = ParticipanteCIP.objects.get(evento=g.nombre,dnis=j.id)
						e = Certificado.objects.get(razon=p.evento)
						listagrupo.append([p.numero,e.codigo])
					except:
						listagrupo.append([0,0])
				for g in distrital:
					try:
						p = ParticipanteCIP.objects.get(evento=g.nombre,dnis=j.id)
						e = Certificado.objects.get(razon=p.evento)
						listadistrito.append([p.numero,e.codigo])
					except:
						listadistrito.append([0,0])
				for g in regional:
					try:
						p = ParticipanteCIP.objects.get(evento=g.nombre,dnis=j.id)
						e = Certificado.objects.get(razon=p.evento)
						listaregnac.append([p.numero,e.codigo])
					except:
						listaregnac.append([0,0])
				for g in nacional:
					try:
						p = ParticipanteCIP.objects.get(evento=g.nombre,dnis=j.id)
						e = Certificado.objects.get(razon=p.evento)
						listaregnac.append([p.numero,e.codigo])
					except:
						listaregnac.append([0,0])
				listadog.append(listagrupo)
				listadod.append(listadistrito)
				listadorn.append(listaregnac)
			listadogtotal.append(zip(jovenes,listadog))
			listadodtotal.append(zip(jovenes,listadod))
			listadorntotal.append(zip(jovenes,listadorn))
			grupaltotal.append(grupal)
			distritaltotal.append(distrital)
			regionaltotal.append(regional)
			nacionaltotal.append(nacional)
		return render(request,'cip.html',{'fotoperfil':permisos.imagen,'gru':grupo,'g':gr,'cips':zip(unidades,grupaltotal,distritaltotal,regionaltotal,nacionaltotal,listadogtotal,listadodtotal,listadorntotal)})
	else:
		return render(request, '404.html', {})

@login_required(login_url ='/')
def condecoracionesd(request,grupo):
	g =  definegrupo(grupo)
	permisos = PermisoUnidad.objects.get(usuario=request.user)
	u = revisarpermisos(permisos)
	unidades = []
	gru = definegrupo(Grupo.objects.get(usuario=request.user).grupo)
	if (gru == g):
		jovenestotal = []
		barrastotal = []
		meritototal = []
		nudostotal = []
		for x in u:
			unidades.append(defineunidad(x))
			jovenes = Joven.objects.filter(grupo=g,unidad=defineunidad(x))
			nudos = []
			barras = []
			merito = []
			jo = []
			for j in jovenes:
				jo.append([j.id,j.primer_nombre+" "+j.primer_apellido])
				listanudos = []
				listabarras = []
				listamerito = []
				anos = [2,6,8]
				con = ['NPB','NPP','NPO']
				try:
					ingreso = datetime.strptime(j.f_promesa, '%d/%m/%Y')
				except:
					ingreso = datetime.today()
				for i,c in enumerate(anos):
					try:
						condecoracion = [1,Condecoraciones.objects.get(dnis=int(j.id),condecoracion=con[i])]
					except:
						if ingreso+timedelta(days=365*c) < datetime.today():
							condecoracion = [0,ingreso+timedelta(days=365*c)]
						else:
							condecoracion = [-1,ingreso+timedelta(days=365*c)]
					listanudos.append(condecoracion)
				nudos.append(listanudos)
				anos = [4,8,0]
				con = ['BESP','BESO','BV']
				try:
					ingreso = datetime.strptime(j.f_promesa, '%d/%m/%Y')
				except:
					ingreso = datetime.today()
				for i,c in enumerate(anos):
					try:
						condecoracion = [1,Condecoraciones.objects.get(dnis=int(j.id),condecoracion=con[i])]
					except:
						if con[i] != "BV" :
							if ingreso+timedelta(days=365*c) < datetime.today():
								condecoracion = [0,ingreso+timedelta(days=365*c)]
							else:
								condecoracion = [-1,ingreso+timedelta(days=365*c)]
						else:
							condecoracion = [-1,0]
					listabarras.append(condecoracion)
				barras.append(listabarras)
				conesp=['OM1','OM2','OSJ']
				for i in conesp:	
					try:
						condecoracion = [1,Condecoraciones.objects.get(dnis=int(j.id),condecoracion=i)]
					except:
						condecoracion = [-1,0]
					listamerito.append(condecoracion)
				merito.append(listamerito)
			nudostotal.append(zip(jo,nudos))
			barrastotal.append(zip(jo,barras))
			meritototal.append(zip(jo,merito))
		hoy = datetime.now()
		return render(request,'condecoraciones.html',{'fotoperfil':permisos.imagen,'gru':grupo,'g':g,'u':u,'condecoraciones':zip(unidades,nudostotal,barrastotal,meritototal),'hoy':hoy})
	else:
		return render(request, '404.html', {})


@login_required(login_url ='/')
def adelantosd(request,grupo):
	g =  definegrupo(grupo)
	permisos = PermisoUnidad.objects.get(usuario=request.user)
	u = revisarpermisos(permisos)
	unidades = []
	gru = definegrupo(Grupo.objects.get(usuario=request.user).grupo)
	if (gru == g):
		pruebastotal = []
		jovenestotal = []
		for x in u:
			unidades.append(defineunidad(x))
			if x == 'MM':
				adelantos = ['Lobato','Huella Fresca','Huella Alerta','Huella Agil','Huella Libre','Lobo Saltarin']
				gr = definegrupo(grupo)
				un = defineunidad(x)
				plobato = Prueba.objects.filter(unidad='M',adelanto='LO')
				pfresca = Prueba.objects.filter(unidad='M',adelanto='FR')
				palerta = Prueba.objects.filter(unidad='M',adelanto='AL')
				pagil = Prueba.objects.filter(unidad='M',adelanto='AG')
				plibre = Prueba.objects.filter(unidad='M',adelanto='LI')
				plobo = Prueba.objects.filter(unidad='M',adelanto='LS')
				pruebas = [plobato,pfresca,palerta,pagil,plibre,plobo]
				aprobados=[]
				for i,p in enumerate(adelantos):
					nombres = ['Cachorro']+adelantos[0:adelantos.index(p)]
					jovenes = Joven.objects.filter(grupo=g,unidad=defineunidad(x),adelanto__in =nombres)
					jovenestotal.append(jovenes)
					aproba=[]
					for j in jovenes:
						apro =[]
						for pr in pruebas[i]:
							apro.append([j.id,pr.id,Logro.objects.filter(dnis=j.id,prueba=pr).exists()])
						aproba.append(apro)
					aprobados.append(zip(jovenes,aproba))

				pruebas = zip(adelantos,pruebas,aprobados)
				pruebastotal.append(pruebas)
			elif x == 'MF':
				adelantos = ['Lobato','Huella Fresca','Huella Alerta','Huella Agil','Huella Libre','Lobo Saltarin']
				gr = definegrupo(grupo)
				un = defineunidad(x)
				plobato = Prueba.objects.filter(unidad='M',adelanto='LO')
				pfresca = Prueba.objects.filter(unidad='M',adelanto='FR')
				palerta = Prueba.objects.filter(unidad='M',adelanto='AL')
				pagil = Prueba.objects.filter(unidad='M',adelanto='AG')
				plibre = Prueba.objects.filter(unidad='M',adelanto='LI')
				plobo = Prueba.objects.filter(unidad='M',adelanto='LS')
				pruebas = [plobato,pfresca,palerta,pagil,plibre,plobo]
				aprobados=[]
				for i,p in enumerate(adelantos):
					nombres = ['Cachorro']+adelantos[1:adelantos.index(p)]
					jovenes = Joven.objects.filter(grupo=g,unidad=un,adelanto__in =nombres)
					jovenestotal.append(jovenes)
					aproba=[]
					for j in jovenes:
						apro =[]
						for pr in pruebas[i]:
							apro.append([j.id,pr.id,Logro.objects.filter(dnis=j.id,prueba=pr).exists()])
						aproba.append(apro)
					aprobados.append(zip(jovenes,aproba))
				pruebas = zip(adelantos,pruebas,aprobados)
				pruebastotal.append(pruebas)
			elif (x == 'TM' or x == 'TF') :
				adelantos = ['Aventurero','Explorador','Pionero','Scout de Bolivar']
				gr = definegrupo(grupo)
				un = defineunidad(x)
				paventurero = Prueba.objects.filter(unidad='T',adelanto='AV')
				pexplorador = Prueba.objects.filter(unidad='T',adelanto='EX')
				ppionero = Prueba.objects.filter(unidad='T',adelanto='PI')
				pscoutdebolivar = Prueba.objects.filter(unidad='T',adelanto='SB')
				pruebas = [paventurero,pexplorador,ppionero,pscoutdebolivar]
				aprobados=[]
				for i,p in enumerate(adelantos):
					nombres = ['Novicio']+adelantos[0:adelantos.index(p)]
					jovenes = Joven.objects.filter(grupo=g,unidad=defineunidad(x),adelanto__in =nombres)
					jovenestotal.append(jovenes)
					aproba=[]
					for j in jovenes:
						apro =[]
						for pr in pruebas[i]:
							apro.append([j.id,pr.id,Logro.objects.filter(dnis=j.id,prueba=pr).exists()])
						aproba.append(apro)
					aprobados.append(zip(jovenes,aproba))
				pruebas = zip(adelantos,pruebas,aprobados)
				pruebastotal.append(pruebas)
			elif (x =='CM' or x =='CF'):
				adelantos = ['Precursor','Servicio Social y Comunidad','Vivencia al Aire Libre','Desarrollo Personal','Actividades Propias']
				gr = definegrupo(grupo)
				un = defineunidad(x)
				jovenes = Joven.objects.filter(grupo=g,unidad=un)
				jovenestotal.append(jovenes)
				pep = Prueba.objects.filter(unidad='C',adelanto='PRE')
				pssc = Prueba.objects.filter(unidad='C',adelanto='Servicio Social y Comunidad')
				pval = Prueba.objects.filter(unidad='C',adelanto='Vivencia al Aire Libre')
				pdp = Prueba.objects.filter(unidad='C',adelanto='Desarrollo Personal')
				ppropias = Prueba.objects.filter(unidad='C',adelanto='Actividades Propias')
				pruebas = [pep,pssc,pval,pdp,ppropias]
				aprobados=[]
				for i,p in enumerate(adelantos):
					aproba=[]
					for j in jovenes:
						apro =[]
						for pr in pruebas[i]:
							apro.append([j.id,pr.id,Logro.objects.filter(dnis=j.id,prueba=pr).exists()])
						aproba.append(apro)
					aprobados.append(zip(jovenes,aproba))
				pruebas = zip(adelantos,pruebas,aprobados)
				pruebastotal.append(pruebas)
		total = zip(unidades,u,pruebastotal,jovenestotal)
		return render(request, 'adelantos.html', 
				{'fotoperfil':permisos.imagen,'total':total,'gru':grupo,'g':gr,})
	else:
		return render(request, '404.html', {})

@login_required(login_url ='/')
def cursosd(request,grupo):
	g =  definegrupo(grupo)
	permisos = PermisoUnidad.objects.get(usuario=request.user)
	u = revisarpermisos(permisos)
	unidades = []
	cursostotal = []
	gru = definegrupo(Grupo.objects.get(usuario=request.user).grupo)
	gr = definegrupo(grupo)
	listaunidad = []
	if (gru == g):
		for x in u:
			if x !="MM" and x !="MF":
				un = defineunidad(x)
				unidades.append(defineunidad(x))
				jovenes = Joven.objects.filter(grupo=gr,unidad=un)
				cursos = []
				if x == "TM" or x == "TF":
					cursos = ['Punta de Flecha en Bronce','Punta de Flecha en Plata','Punta de Flecha en Oro']
				elif x == "CM" or x == "CF":
					cursos = ['Horqueta','Remo','Canoa','Peregrino']
				cursostotal.append(cursos)
				listajoven = []
				for j in jovenes:
					listacursos = []
					for c in cursos:
						try:
							p = ParticipanteCursos.objects.get(evento=c,dnis=j.id)
							e = Certificado.objects.get(razon=p.evento)
							listacursos.append([p.numero,e.codigo])
						except:
							listacursos.append([0,0])
					listajoven.append(listacursos)
				listaunidad.append(zip(jovenes,listajoven))
			listafinal = (zip(unidades,cursostotal,listaunidad))
		return render(request,'cursos.html',{'fotoperfil':permisos.imagen,'gru':grupo,'g':gr,'cursos':listafinal})
	else:
		return render(request, '404.html', {})

@login_required(login_url ='/')
def programasmundialesd(request,grupo):
	g =  definegrupo(grupo)
	permisos = PermisoUnidad.objects.get(usuario=request.user)
	u = revisarpermisos(permisos)
	unidades = []
	cursostotal = []
	gru = definegrupo(Grupo.objects.get(usuario=request.user).grupo)
	gr = definegrupo(grupo)
	listaunidad = []
	if (gru == g):
		for x in u:
			un = defineunidad(x)
			unidades.append(defineunidad(x))
			jovenes = Joven.objects.filter(grupo=gr,unidad=un)
			cursos = ['Programa Scout Mundial del Ambiente','Programa Mensajeros de Paz']
			if x == "CM" or x == "CF":
				cursos.append("Programa Scouts del Mundo")
			cursostotal.append(cursos)
			listajoven = []
			for j in jovenes:
				listacursos = []
				for c in cursos:
					try:
						p = ParticipanteProgramasMundiales.objects.get(evento=c,dnis=j.id)
						e = Certificado.objects.get(razon=c)
						listacursos.append([p.numero,e.codigo])
					except:
						listacursos.append([0,0])
				
				listajoven.append(listacursos)
			listaunidad.append(zip(jovenes,listajoven))
		listafinal = (zip(unidades,cursostotal,listaunidad))
		return render(request,'programasmundiales.html',{'fotoperfil':permisos.imagen,'gru':grupo,'g':gr,'cursos':listafinal})
	else:
		return render(request, '404.html', {})

@login_required(login_url ='/')
def especialidadesd(request,grupo):
	g =  definegrupo(grupo)
	permisos = PermisoUnidad.objects.get(usuario=request.user)
	u = revisarpermisos(permisos)
	unidades = []
	cursostotal = []
	gru = definegrupo(Grupo.objects.get(usuario=request.user).grupo)
	gr = definegrupo(grupo)
	listaunidad = []
	cod = ['AYH','IDN','CFI','CYT','SER','PPT','VAL','HYD']
	cursos = ['Artes y Hobbies','Identidad Nacional','Cultura Física','Ciencia y Tecnología','Servicio','Preparación para el Trabajo','Vida al Aire Libre','Habilidades y Destrezas']	
	if (gru == g):
		for x in u:
			un = defineunidad(x)
			unidades.append(defineunidad(x))
			jovenes = Joven.objects.filter(grupo=gr,unidad=un)
			listajoven = []
			for j in jovenes:
				listacursos = []
				for i,c in enumerate(cursos):
					try:
						p = Especialidades.objects.get(tipo=i,dnis=j.id)
						listacursos.append([p.nivel,cod[i]])
					except:
						listacursos.append([0,0])
				listajoven.append(listacursos)
			listaunidad.append(zip(jovenes,listajoven))
		listafinal = (zip(unidades,listaunidad))
			
		return render(request,'especialidades.html',{'fotoperfil':permisos.imagen,'especialidades':cursos,'gru':grupo,'g':gr,'cursos':listafinal})
	else:
		return render(request, '404.html', {})


@permission_required('is_staff',login_url ='/')
def maximasalertad(request):
	u = ['MM','MF','TM','TF','CM','CF']
	permisos = PermisoUnidad.objects.get(usuario=request.user)
	grupos = ['PLEYADES','RORAIMA','TIUNA','SANTO TOMAS DE AQUINO','DON BOSCO','CATATUMBO']
	unidades = []
	jovenesdistrito = []
	permisos = PermisoUnidad.objects.get(usuario=request.user)
	u = revisarpermisos(permisos)
	unidades = []
	cursostotal = []
	listajoven = []
	for gr in grupos:
		hoy = datetime.today()
		for x in u:
			un = defineunidad(x)
			unidades.append(defineunidad(x)) 
			jovenes = Joven.objects.filter(grupo=gr,unidad=un)

			if x == "MM" or x == "MF" :
				for j in jovenes:
					try: 
						nacimiento = datetime.strptime(j.f_nac, '%d/%m/%Y')
					except:
						nacimiento = datetime.today()
					desvinculacion = nacimiento +timedelta(days=11*365) 
					if desvinculacion-timedelta(days=365/2) < hoy and desvinculacion > hoy:
						especialidades = Especialidades.objects.filter(dnis=j.id,nivel=3)
						if especialidades.count() >= 2:
							esp1= especialidades[0]
							esp2= especialidades[1]
						elif especialidades.count() == 1:
							esp1= especialidades[0]
							esp2= 0
						else:
							esp1=0
							esp2=0
						grupal = CIP.objects.values_list('nombre',flat=True).filter(nivel='Grupal')
						if ParticipanteCIP.objects.filter(dnis=j.id,evento__in=grupal).exists():
							g = ParticipanteCIP.objects.filter(dnis=j.id,evento__in=grupal)[0]
						else:
							g = 0
						distrital = CIP.objects.values_list('nombre',flat=True).filter(nivel='Distrital',unidad='M')
						if ParticipanteCIP.objects.filter(dnis=j.id,evento__in=distrital).exists():
							d = ParticipanteCIP.objects.filter(dnis=j.id,evento__in=distrital)[0]
						else:
							d = 0
						regional = CIP.objects.values_list('nombre',flat=True).filter(nivel='Regional',unidad='M')
						if ParticipanteCIP.objects.filter(dnis=j.id,evento__in=regional).exists():
							r = ParticipanteCIP.objects.filter(dnis=j.id,evento__in=regional)[0]
						else:
							r = 0
						nacional = CIP.objects.values_list('nombre',flat=True).filter(nivel='Nacional',unidad='M')
						if ParticipanteCIP.objects.filter(dnis=j.id,evento__in=nacional).exists():
							n = ParticipanteCIP.objects.filter(dnis=j.id,evento__in=nacional)[0]
						else:
							n = 0
						edad = (hoy - nacimiento).days/365
						estado = (esp1!=0 and esp2!=0 and g!=0 and d !=0 and (r!=0 or n!=0))
						desvin = (desvinculacion-hoy).days/30
						if desvin < 1:
							des = str((desvinculacion-hoy).days)+" días"
						else:
							des = str(desvin)+" meses"
						listajoven.append([gr,j,1,edad,des,esp1,esp2,g,d,r,n,estado])
			elif x == "TM" or x == "TF" : 
				for j in jovenes:
					try: 
						nacimiento = datetime.strptime(j.f_nac, '%d/%m/%Y')
					except:
						nacimiento = datetime.today()
					desvinculacion = nacimiento +timedelta(days=16*365) 
					if desvinculacion-timedelta(days=365/2) < hoy and desvinculacion > hoy:
						especialidades = Especialidades.objects.filter(dnis=j.id,nivel=3)
						if especialidades.count() >= 2:
							esp1= especialidades[0]
							esp2= especialidades[1]
						elif especialidades.count() == 1:
							esp1= especialidades[0]
							esp2= 0
						else:
							esp1=0
							esp2=0
						grupal = CIP.objects.values_list('nombre',flat=True).filter(nivel='Grupal')
						if ParticipanteCIP.objects.filter(dnis=j.id,evento__in=grupal).exists():
							g = ParticipanteCIP.objects.filter(dnis=j.id,evento__in=grupal)[0]
						else:
							g = 0
						distrital = CIP.objects.values_list('nombre',flat=True).filter(nivel='Distrital',unidad='T')
						if ParticipanteCIP.objects.filter(dnis=j.id,evento__in=distrital).exists():
							d = ParticipanteCIP.objects.filter(dnis=j.id,evento__in=distrital)[0]
						else:
							d = 0
						regional = CIP.objects.values_list('nombre',flat=True).filter(nivel='Regional',unidad='T')
						if ParticipanteCIP.objects.filter(dnis=j.id,evento__in=regional).exists():
							r = ParticipanteCIP.objects.filter(dnis=j.id,evento__in=regional)[0]
						else:
							r = 0
						nacional = CIP.objects.values_list('nombre',flat=True).filter(nivel='Nacional',unidad='T')
						if ParticipanteCIP.objects.filter(dnis=j.id,evento__in=nacional).exists():
							n = ParticipanteCIP.objects.filter(dnis=j.id,evento__in=nacional)[0]
						else:
							n = 0
						edad = (hoy - nacimiento).days/365
						estado = (esp1!=0 and esp2!=0 and g!=0 and d !=0 and (r!=0 or n!=0))
						desvin = (desvinculacion-hoy).days/30
						if desvin < 1:
							des = str((desvinculacion-hoy).days)+" días"
						else:
							des = str(desvin)+" meses"
						listajoven.append([gr,j,2,edad,des,esp1,esp2,g,d,r,n,estado])
			elif x == "CM" or x == "CF" : 
				for j in jovenes:
					try: 
						nacimiento = datetime.strptime(j.f_nac, '%d/%m/%Y')
					except:
						nacimiento = datetime.today()
					desvinculacion = nacimiento +timedelta(days=21*365) 
					if desvinculacion-timedelta(days=365/2) < hoy and desvinculacion > hoy:
						especialidades = Especialidades.objects.filter(dnis=j.id,nivel=3)
						if especialidades.count() >= 2:
							esp1= especialidades[0]
							esp2= especialidades[1]
						elif especialidades.count() == 1:
							esp1= especialidades[0]
							esp2= 0
						else:
							esp1=0
							esp2=0
						grupal = CIP.objects.values_list('nombre',flat=True).filter(nivel='Grupal')
						if ParticipanteCIP.objects.filter(dnis=j.id,evento__in=grupal).exists():
							g = ParticipanteCIP.objects.filter(dnis=j.id,evento__in=grupal)[0]
						else:
							g = 0
						distrital = CIP.objects.values_list('nombre',flat=True).filter(nivel='Distrital',unidad='C')
						if ParticipanteCIP.objects.filter(dnis=j.id,evento__in=distrital).exists():
							d = ParticipanteCIP.objects.filter(dnis=j.id,evento__in=distrital)[0]
						else:
							d = 0
						regional = CIP.objects.values_list('nombre',flat=True).filter(nivel='Regional',unidad='C')
						if ParticipanteCIP.objects.filter(dnis=j.id,evento__in=regional).exists():
							r = ParticipanteCIP.objects.filter(dnis=j.id,evento__in=regional)[0]
						else:
							r = 0
						nacional = CIP.objects.values_list('nombre',flat=True).filter(nivel='Nacional',unidad='C')
						if ParticipanteCIP.objects.filter(dnis=j.id,evento__in=nacional).exists():
							n = ParticipanteCIP.objects.filter(dnis=j.id,evento__in=nacional)[0]
						else:
							n = 0
						edad = (hoy - nacimiento).days/365
						estado = (esp1!=0 and esp2!=0 and g!=0 and d !=0 and (r!=0 or n!=0))
						desvin = (desvinculacion-hoy).days/30
						if desvin < 1:
							des = str((desvinculacion-hoy).days)+" días"
						else:
							des = str(desvin)+" meses"
						listajoven.append([gr,j,3,edad,des,esp1,esp2,g,d,r,n,estado])
	print(listajoven)
	return render(request,'distrito-maximasalerta.html',{'fotoperfil':permisos.imagen,'listajoven':listajoven})
	

def desvinculacionesd(request,grupo):
	g =  definegrupo(grupo)
	permisos = PermisoUnidad.objects.get(usuario=request.user)
	u = revisarpermisos(permisos)
	unidades = []
	cursostotal = []
	gru = definegrupo(Grupo.objects.get(usuario=request.user).grupo)
	gr = definegrupo(grupo)
	listaunidad = []
	if (gru == g):
		hoy = datetime.today()
		listajoven = []
		for x in u:
			un = defineunidad(x)
			unidades.append(defineunidad(x)) 
			jovenes = Joven.objects.filter(grupo=gr,unidad=un)
			if x == "MM" or x == "MF" :
				for j in jovenes:
					nacimiento = datetime.strptime(j.f_nac, '%d/%m/%Y')
					desvinculacion = datetime.strptime(j.f_nac, '%d/%m/%Y')+timedelta(days=11*365) 
					edad = (hoy - nacimiento).days/365 
					if desvinculacion < hoy :
						listajoven.append([j,1,edad,hoy-desvinculacion,j.gen])
			elif x == "TM" or x == "TF" : 
				for j in jovenes:
					nacimiento = datetime.strptime(j.f_nac, '%d/%m/%Y')
					desvinculacion = datetime.strptime(j.f_nac, '%d/%m/%Y')+timedelta(days=16*365) 
					edad = (hoy - nacimiento).days/365 
					if desvinculacion < hoy :
						listajoven.append([j,2,edad,hoy-desvinculacion,j.gen])
			elif x == "CM" or x == "CF" : 
				for j in jovenes:
					nacimiento = datetime.strptime(j.f_nac, '%d/%m/%Y')
					desvinculacion = datetime.strptime(j.f_nac, '%d/%m/%Y')+timedelta(days=21*365)
					edad = (hoy - nacimiento).days/365 
					if desvinculacion < hoy: 
						listajoven.append([j,3,edad,hoy-desvinculacion,j.gen])
		return render(request,'devinculacion.html',{'fotoperfil':permisos.imagen,'gru':grupo,'g':gr,'lista':listajoven})
	else:
		return render(request, '404.html', {})


def solicitaradelantod(request,grupo):
	g =  definegrupo(grupo)
	permisos = PermisoUnidad.objects.get(usuario=request.user)
	u = revisarpermisos(permisos)
	unidades = []
	cursostotal = []
	gru = definegrupo(Grupo.objects.get(usuario=request.user).grupo)
	gr = definegrupo(grupo)
	listaunidad = []
	listatotal=[]
	if (gru == g):
		hoy = datetime.today()
		listajoven = []
		for x in u:
			un = defineunidad(x)
			unidades.append(defineunidad(x)) 
			jovenes = Joven.objects.filter(grupo=gr,unidad=un)
			if x == "MM" or x == "MF" :
				adelantos = ['Cachorro','Lobato','Huella Fresca','Huella Alerta','Huella Agil','Huella Libre','Lobo Saltarin']
				pruebasdeadelantos =  ['LO','FR','AL','AG','LI','LS']
				insignia = ['LO','HF','HA','HG','HL','LS']
				listajoven=[]
				for j in jovenes:
					adelanto = j.adelanto
					if adelanto != "Lobo Saltarin":
						proximo = pruebasdeadelantos[adelantos.index(adelanto)]
						totalpruebas =  Prueba.objects.filter(unidad='M',adelanto=proximo).count()
						p = Prueba.objects.values_list("pk",flat=True).filter(adelanto=proximo)
						aprobados = Logro.objects.filter(dnis=j.id,prueba__in = p).count()
						if datetime.strptime(j.f_nac, '%d/%m/%Y')+ timedelta(days=11*365) < datetime.now():
							proximo = 'T'
						else:
							proximo = insignia[adelantos.index(adelanto)]
						listajoven.append([j,adelanto,proximo,aprobados,totalpruebas])
			elif x == "TM" or x == "TF" :
				adelantos = ['Novicio','Aventurero','Explorador','Pionero','Scout de Bolivar']
				pruebasdeadelantos =  ['AV','EX','PI','SB']
				insignia = ['AV','EX','PI','SB']
				listajoven=[]
				for j in jovenes:
					adelanto = j.adelanto
					if adelanto != "Scout de Bolivar":
						proximo = pruebasdeadelantos[adelantos.index(adelanto)]
						totalpruebas =  Prueba.objects.filter(unidad='T',adelanto=proximo).count()
						p = Prueba.objects.values_list("pk",flat=True).filter(adelanto=proximo)
						aprobados = Logro.objects.filter(dnis=j.id,prueba__in = p).count()
						if datetime.strptime(j.f_nac, '%d/%m/%Y')+ timedelta(days=16*365) < datetime.now():
							proximo = 'C'
						else:
							proximo = insignia[adelantos.index(adelanto)]
						listajoven.append([j,adelanto,proximo,aprobados,totalpruebas])
			elif x == "CM" or x == "CF" :
				adelantos = ['Novato','Precursor','Expedicionario','Descubridor','Fundador','Rover Ciudadano']
				pruebasdeadelantos =  ['PR','EP','DE','FU','RC']
				insignia = ['PR','EP','DE','FU','RC']
				listajoven=[]
				for j in jovenes:
					adelanto = j.adelanto
					if adelanto != "Rover Ciudadano":
						proximo = pruebasdeadelantos[adelantos.index(adelanto)]
						totalpruebas =  Prueba.objects.filter(unidad='C',adelanto=proximo).count()
						p = Prueba.objects.values_list("pk",flat=True).filter(adelanto=proximo)
						aprobados = Logro.objects.filter(dnis=j.id,prueba__in = p).count()
						if datetime.strptime(j.f_nac, '%d/%m/%Y')+ timedelta(days=21*365) < datetime.now():
							if j.gen =='M':
								proximo = 'Ah'
							else:
								proximo = 'Am'
						else:
							proximo = insignia[adelantos.index(adelanto)]
						listajoven.append([j,adelanto,proximo,aprobados,totalpruebas])
			listatotal.append([un,listajoven])
			# elif x == "TM" or x == "TF" : 
			# 	for j in jovenes:
					
			# elif x == "CM" or x == "CF" : 
			# 	for j in jovenes:
					
		return render(request,'solicitaradelanto.html',{'fotoperfil':permisos.imagen,'gru':grupo,'g':gr,'lista':listatotal})
	else:
		return render(request, '404.html', {})