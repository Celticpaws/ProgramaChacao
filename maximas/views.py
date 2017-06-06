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
		return redirect(g+"/metas")
	elif request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None and user.is_active:
			auth.login(request, user)
			g = Grupo.objects.get(usuario=user).grupo
			return redirect(g+"/metas")
		else:
			return render(request, "login.html", {})
	else:
		return render(request, "login.html", {})

@login_required(login_url ='/')
def cuadrosmetas(request,grupo):
	g =  definegrupo(grupo)
	permisos = PermisoUnidad.objects.get(usuario=request.user)
	u = []
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
	unidades = []
	gru = definegrupo(Grupo.objects.get(usuario=request.user).grupo)
	gr = definegrupo(grupo)
	if (gru == g):
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
		return render(request, 'cuadrometas.html', 
			{'unidades':zip(unidades,u),'jovenestotal':jovenestotal,'gru':grupo,'g':gr,'hoy':hoy,'futuro':futuro,'g':grupo})
	else:
		return render(request, '404.html', {})

@login_required(login_url ='/')
def cip(request,grupo):
	g =  definegrupo(grupo)
	permisos = PermisoUnidad.objects.get(usuario=request.user)
	u = []
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
						p = Participante.objects.get(evento=g.nombre,dnis=j.id)
						e = Certificado.objects.get(razon=p.evento)
						listagrupo.append([p.numero,e.codigo])
					except:
						listagrupo.append([0,0])
				for g in distrital:
					try:
						p = Participante.objects.get(evento=g.nombre,dnis=j.id)
						e = Certificado.objects.get(razon=p.evento)
						listadistrito.append([p.numero,e.codigo])
					except:
						listadistrito.append([0,0])
				for g in regional:
					try:
						p = Participante.objects.get(evento=g.nombre,dnis=j.id)
						e = Certificado.objects.get(razon=p.evento)
						listaregnac.append([p.numero,e.codigo])
					except:
						listaregnac.append([0,0])
				for g in nacional:
					try:
						p = Participante.objects.get(evento=g.nombre,dnis=j.id)
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
		return render(request,'cip.html',{'gru':grupo,'g':gr,'cips':zip(unidades,grupaltotal,distritaltotal,regionaltotal,nacionaltotal,listadogtotal,listadodtotal,listadorntotal)})
	else:
		return render(request, '404.html', {})

@login_required(login_url ='/')
def condecoraciones(request,grupo):
	g =  definegrupo(grupo)
	permisos = PermisoUnidad.objects.get(usuario=request.user)
	u = []
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
		return render(request,'condecoraciones.html',{'gru':grupo,'g':g,'u':u,'condecoraciones':zip(unidades,nudostotal,barrastotal,meritototal),'hoy':hoy})
	else:
		return render(request, '404.html', {})


@login_required(login_url ='/')
def adelantos(request,grupo):
	g =  definegrupo(grupo)
	permisos = PermisoUnidad.objects.get(usuario=request.user)
	u = []
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
	unidades = []
	gru = definegrupo(Grupo.objects.get(usuario=request.user).grupo)
	if (gru == g):
		pruebastotal = []
		jovenestotal = []
		for x in u:
			unidades.append(defineunidad(x))
			if x == 'MM':
				adelantos = ['Lobato','Huella Fresca','Huella Alerta','Huellas Agil','Huella Libre','Lobo Saltarin']
				gr = definegrupo(grupo)
				un = defineunidad(x)
				jovenes = Joven.objects.filter(grupo=g,unidad=defineunidad(x))
				jovenestotal.append(jovenes)
				plobato = Prueba.objects.filter(unidad='M',adelanto='LO')
				pfresca = Prueba.objects.filter(unidad='M',adelanto='FR')
				palerta = Prueba.objects.filter(unidad='M',adelanto='AL')
				pagil = Prueba.objects.filter(unidad='M',adelanto='AG')
				plibre = Prueba.objects.filter(unidad='M',adelanto='LI')
				plobo = Prueba.objects.filter(unidad='M',adelanto='LS')
				pruebas = [plobato,pfresca,palerta,pagil,plibre,plobo]
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
			elif x == 'MF':
				adelantos = ['Lobezna','Huella Fresca','Huella Alerta','Huellas Agil','Huella Libre','Lobo Saltarin']
				gr = definegrupo(grupo)
				un = defineunidad(x)
				jovenes = Joven.objects.filter(grupo=g,unidad=un)
				jovenestotal.append(jovenes)
				plobato = Prueba.objects.filter(unidad='M',adelanto='LO')
				pfresca = Prueba.objects.filter(unidad='M',adelanto='FR')
				palerta = Prueba.objects.filter(unidad='M',adelanto='AL')
				pagil = Prueba.objects.filter(unidad='M',adelanto='AG')
				plibre = Prueba.objects.filter(unidad='M',adelanto='LI')
				plobo = Prueba.objects.filter(unidad='M',adelanto='LS')
				pruebas = [plobato,pfresca,palerta,pagil,plibre,plobo]
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
			elif (x == 'TM' or x == 'TF') :
				adelantos = ['Aventurero','Explorador','Pionero','Scout de Bolivar']
				gr = definegrupo(grupo)
				un = defineunidad(x)
				jovenes = Joven.objects.filter(grupo=g,unidad=un)
				jovenestotal.append(jovenes)
				paventurero = Prueba.objects.filter(unidad='T',adelanto='AV')
				pexplorador = Prueba.objects.filter(unidad='T',adelanto='EX')
				ppionero = Prueba.objects.filter(unidad='T',adelanto='PI')
				pscoutdebolivar = Prueba.objects.filter(unidad='T',adelanto='SB')
				pruebas = [paventurero,pexplorador,ppionero,pscoutdebolivar]
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
				{'total':total,'gru':grupo,'g':gr,})
	else:
		return render(request, '404.html', {})

@login_required(login_url ='/')
def modificaradelantoajax(request):
	# try:
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
	# except:
	# 	resultado = 0
	return HttpResponse(json.dumps(resultado),content_type='application/json')	

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
    
    logo = ImageReader("/home/programachacao/ProgramaChacao/static/certificados/"+evento.certificado.codigo+".jpg")
    
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