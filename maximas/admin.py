# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


from import_export.resources import ModelResource
from import_export.admin import ImportExportMixin, ImportMixin, ExportActionModelAdmin

from .models import *
# Register your models here.

class JovenResource(ModelResource):

    class Meta:
        model = Joven

    def for_delete(self, row, instance):
        return self.fields['id'].clean(row) == ''


class JovenAdmin(ImportExportMixin, admin.ModelAdmin):
    list_filter = ['unidad', 'grupo']
    resource_class = JovenResource

class ParticipanteResource(ModelResource):

    class Meta:
        model = Participante

    def for_delete(self, row, instance):
        return self.fields['id'].clean(row) == ''


class ParticipanteAdmin(ImportExportMixin, admin.ModelAdmin):
    list_filter = ['primer_apellido', 'numero']
    resource_class = ParticipanteResource

class PruebaResource(ModelResource):

    class Meta:
        model = Prueba

    def for_delete(self, row, instance):
        return self.fields['id'].clean(row) == ''


class PruebaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_filter = ['nombre', 'unidad']
    resource_class = PruebaResource



class AdultoAdmin(ImportMixin, admin.ModelAdmin):
    pass

admin.site.register(Joven, JovenAdmin)
admin.site.register(Adulto, AdultoAdmin)
admin.site.register(Grupo)
admin.site.register(Evento)
admin.site.register(Condecoraciones)
admin.site.register(CIP)
admin.site.register(Certificado)
admin.site.register(Logro)
admin.site.register(PermisoUnidad)
admin.site.register(Participante,ParticipanteAdmin)
admin.site.register(Prueba,PruebaAdmin)
