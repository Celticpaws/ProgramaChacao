# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


from import_export.resources import ModelResource
from import_export.admin import ImportExportMixin, ImportMixin, ExportActionModelAdmin

from .models import *
# Register your models here.

class ChildAdmin(ImportMixin, admin.ModelAdmin):
    pass


class JovenResource(ModelResource):

    class Meta:
        model = Joven

    def for_delete(self, row, instance):
        return self.fields['id'].clean(row) == ''


class JovenAdmin(ImportExportMixin, admin.ModelAdmin):
    list_filter = ['unidad', 'grupo']
    resource_class = JovenResource

class AdultoAdmin(ImportMixin, admin.ModelAdmin):
    pass

admin.site.register(Joven, JovenAdmin)
admin.site.register(Adulto, AdultoAdmin)
admin.site.register(Grupo)
