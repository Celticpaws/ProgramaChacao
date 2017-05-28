from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login,logout
from django.conf import settings
from maximas import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
