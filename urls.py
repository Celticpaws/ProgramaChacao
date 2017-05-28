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
    url(r'^metas/(?P<grupo>[\w\-]+)/(?P<unidad>[\w\-]+)$', views.cuadrosmetasunidad, name='cuadrosunidad'),
    url(r'^metas/(?P<grupo>[\w\-]+)/$', views.cuadrosmetas, name='cuadrosgrupo'),
    url(r'^logout$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),      
]

urlpatterns += staticfiles_urlpatterns()
