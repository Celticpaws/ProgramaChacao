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

def certificados(request,codigo):
	certificado = Certificado.objects.get(codigo=codigo)
	evento = Evento.objects.get(certificado=certificado)
	participantes = Participante.objects.filter(evento=evento.nombre)
	return render(request,'certificados.html',{'certificado':certificado,'evento':evento,'participantes':participantes})

def certificadoindividual(request,evento,nombre):
    evento = Evento.objects.get(certificado__codigo=evento)
    participante = Participante.objects.get(evento=evento.nombre,numero=nombre)
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

def certificadomop(request,codigo):
    evento = Certificado.objects.get(razon="Programa Mensajeros de Paz")
    participante = ParticipanteProgramasMundiales.objects.get(numero=codigo)
    joven = Joven.objects.get(pk=participante.dnis)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "filename='"+evento.codigo+"-"+participante.numero+".pdf'"
    
    logo = ImageReader("/home/cfarinha/Dropbox/ProgramaChacao/maximas/static/certificados/mop-"+str(participante.fecha.year)+".jpg")
    
    p = canvas.Canvas(response)
    p.setPageSize((594, 792))
    w, h = (594,792)
    p.drawImage(logo, 0,0,width=w,height=h) 
    p.setFillColorRGB(0.3,0.3,0.3)
    p.setFont("Helvetica-Bold",20)
    p.drawCentredString(w/2+15, h/2-45, joven.primer_nombre.capitalize()+" "+joven.segundo_nombre.replace(" ","").capitalize()+" "+joven.primer_apellido.capitalize()+" "+joven.segundo_apellido.capitalize())
    p.setFont("Helvetica-Bold",12)
    p.drawCentredString(w/2+15, h/2-60, "C.I. "+str(joven.cedula))
    p.setFillColorRGB(1,1,1)
    p.setFont("Helvetica-Bold",9)
    p.drawString(w/2-292, h/2-382, evento.codigo+"-"+joven.unidad[0]+participante.numero+"-"+str(participante.fecha.year))
    mes = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    p.drawString(w/2-292, h/2-392, "Caracas "+str(participante.fecha.day)+" de "+mes[participante.fecha.month-1]+" de "+str(participante.fecha.year))

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

def certificadopsma(request,codigo):
    evento = Certificado.objects.get(razon="Programa Mensajeros de Paz")
    participante = ParticipanteProgramasMundiales.objects.get(numero=codigo)
    joven = Joven.objects.get(pk=participante.dnis)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "filename='"+evento.codigo+"-"+participante.numero+".pdf'"
    
    logo = ImageReader("/home/cfarinha/Dropbox/ProgramaChacao/maximas/static/certificados/psma-"+joven.unidad[0]+"-"+str(participante.fecha.year)+".jpg")
    
    p = canvas.Canvas(response)
    p.setPageSize((594, 792))
    w, h = (594,792)
    p.drawImage(logo, 0,0,width=w,height=h) 
    if joven.unidad[0] == 'T':
        p.setFillColorRGB(0,1,0)
    if joven.unidad[0] == 'M':
        p.setFillColorRGB(0,0.5,1)
    if joven.unidad[0] == 'C':
        p.setFillColorRGB(0.3,0,1)
    p.setFont("Helvetica-Bold",24)
    p.drawCentredString(w/2, h/2+15, joven.primer_nombre.capitalize()+" "+joven.segundo_nombre.replace(" ","").capitalize()+" "+joven.primer_apellido.capitalize()+" "+joven.segundo_apellido.capitalize())
    p.setFillColorRGB(0.3,0.3,0.3)
    p.setFont("Helvetica",11)
    p.rotate(90)
    p.drawString(h/2-280, w/2-875, participante.fecha.strftime("%d/%m/%Y")+"   "+joven.region[0:3]+"-"+participante.numero)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response