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

class ParticipanteCIPResource(ModelResource):

    class Meta:
        model = ParticipanteCIP

    def for_delete(self, row, instance):
        return self.fields['id'].clean(row) == ''


class ParticipanteCIPAdmin(ImportExportMixin, admin.ModelAdmin):
    list_filter = ['numero']
    resource_class = ParticipanteCIPResource    

class ParticipanteCursosResource(ModelResource):

    class Meta:
        model = ParticipanteCursos

    def for_delete(self, row, instance):
        return self.fields['id'].clean(row) == ''


class ParticipanteCursosAdmin(ImportExportMixin, admin.ModelAdmin):
    list_filter = ['numero']
    resource_class = ParticipanteCursosResource   

class ParticipantePM(ModelResource):

    class Meta:
        model = ParticipanteProgramasMundiales

    def for_delete(self, row, instance):
        return self.fields['id'].clean(row) == ''


class ParticipantePMAdmin(ImportExportMixin, admin.ModelAdmin):
    list_filter = ['numero']
    resource_class = ParticipantePM 

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

class AdelantoResource(ModelResource):

    class Meta:
        model = Adelanto
    def for_delete(self, row, instance):
        return self.fields['id'].clean(row) == ''


class AdelantoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_filter = ['insignia']
    resource_class = AdelantoResource   

admin.site.register(Joven, JovenAdmin)
admin.site.register(Adulto, AdultoAdmin)
admin.site.register(Grupo)
admin.site.register(Evento)
admin.site.register(Adelanto, AdelantoAdmin)
admin.site.register(Especialidades)
admin.site.register(Condecoraciones)
admin.site.register(CIP)
admin.site.register(Certificado)
admin.site.register(Logro)
admin.site.register(PermisoUnidad)
admin.site.register(Participante,ParticipanteAdmin)
admin.site.register(ParticipanteCIP,ParticipanteCIPAdmin)
admin.site.register(ParticipanteCursos,ParticipanteCursosAdmin)
admin.site.register(ParticipanteProgramasMundiales,ParticipantePMAdmin)
admin.site.register(Prueba,PruebaAdmin)
