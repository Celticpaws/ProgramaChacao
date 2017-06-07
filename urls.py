from __future__ import unicode_literals

from django.conf.urls import url, include
from django.contrib.auth.views import login,logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from django.contrib import admin
from maximas import views
admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.login, name='login'),
    url(r'^modificaradelanto$', views.modificaradelantoajax, name='modificaradelantoajax'),
    url(r'^(?P<grupo>[\w\-]+)/adelantos/$', views.adelantos, name='adelantos'),
    url(r'^(?P<grupo>[\w\-]+)/condecoraciones$', views.condecoraciones, name='condecoraciones'),
    url(r'^(?P<grupo>[\w\-]+)/cip$', views.cip, name='cip'),
    url(r'^(?P<grupo>[\w\-]+)/cursos$', views.cursos, name='cursos'),
    url(r'^(?P<grupo>[\w\-]+)/programasmundiales$', views.programasmundiales, name='programasmundiales'),
    url(r'^(?P<grupo>[\w\-]+)/metas/$', views.cuadrosmetas, name='metas'),
    url(r'^logout$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^certificados/(?P<codigo>[\w\-]+)$', views.certificados),
    url(r'^certificado-mop/(?P<codigo>[\w\-]+)$', views.certificadomop),
    url(r'^certificados/(?P<evento>[\w\-]+)/(?P<nombre>[\w\-]+)$', views.certificadoindividual),      
]

urlpatterns += staticfiles_urlpatterns()
