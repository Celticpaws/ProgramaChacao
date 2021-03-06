from __future__ import unicode_literals

from django.conf.urls import url, include
from django.contrib.auth.views import login,logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from django.contrib import admin
from maximas import views
admin.autodiscover()


urlpatterns = [
# Acceso
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.login, name='login'),
    url(r'^dnis$', views.dnis, name='dnis'),
    url(r'^dnis/(?P<dnis>[\w\-]+)/(?P<fecha>[\w\-]+)$', views.perfil, name='perfil'),
    url(r'^cambiarcontrasena$', views.cambiarcontraajax),
    url(r'^logout$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    
# AJAX
    url(r'^modificaradelanto$', views.modificaradelantoajax, name='modificaradelantoajax'),
    url(r'^desvinculando$', views.desvinculandoajax, name='desvinculando'),
    url(r'^adelantar$', views.adelantarajax, name='adelantar'),
    url(r'^modificarespecialidad$', views.modificarespecialidadajax, name='modificarespecialidadajax'),
    
# Grupal
    url(r'^(?P<grupo>[\w\-]+)/adelantos/$', views.adelantos, name='adelantos'),
    url(r'^(?P<grupo>[\w\-]+)/condecoraciones$', views.condecoraciones, name='condecoraciones'),
    url(r'^(?P<grupo>[\w\-]+)/especialidades$', views.especialidades, name='especialidades'),
    url(r'^(?P<grupo>[\w\-]+)/cip$', views.cip, name='cip'),
    url(r'^(?P<grupo>[\w\-]+)/cursos$', views.cursos, name='cursos'),
    url(r'^(?P<grupo>[\w\-]+)/programasmundiales$', views.programasmundiales, name='programasmundiales'),
    url(r'^(?P<grupo>[\w\-]+)/metas/$', views.cuadrosmetas, name='metas'),
    url(r'^(?P<grupo>[\w\-]+)/solicitaradelanto$', views.solicitaradelanto, name='solicitaradelanto'),
    url(r'^(?P<grupo>[\w\-]+)/estadisticas-maximas$', views.maximasalerta, name='maximasalertas'),
    url(r'^(?P<grupo>[\w\-]+)/desvinculaciones$', views.desvinculaciones, name='desvinculaciones'),
    
# Distrital
    url(r'^adelantos$', views.adelantosd, name='adelantosd'),
    url(r'^condecoraciones$', views.condecoracionesd, name='condecoracionesd'),
    url(r'^especialidades$', views.especialidadesd, name='especialidadesd'),
    url(r'^cip$', views.cipd, name='cipd'),
    url(r'^cursos$', views.cursosd, name='cursosd'),
    url(r'^programasmundiales$', views.programasmundialesd, name='programasmundialesd'),
    url(r'^metas$', views.cuadrosmetasd, name='metasd'),
    url(r'^solicitaradelanto$', views.solicitaradelantod, name='solicitaradelantod'),
    url(r'^estadisticas-maximas$', views.maximasalertad, name='maximasalertasd'),
    url(r'^desvinculaciones$', views.desvinculacionesd, name='desvinculacionesd'),

# Certificados
    url(r'^certificados/(?P<codigo>[\w\-]+)$', views.certificados),
    url(r'^certificado-mop/(?P<codigo>[\w\-]+)$', views.certificadomop),
    url(r'^certificado-psma/(?P<codigo>[\w\-]+)$', views.certificadopsma),
    url(r'^certificados/(?P<evento>[\w\-]+)/(?P<nombre>[\w\-]+)$', views.certificadoindividual),      
]

urlpatterns += staticfiles_urlpatterns()
