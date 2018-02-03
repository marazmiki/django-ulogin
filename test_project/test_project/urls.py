# coding: utf-8

from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

admin.autodiscover()


urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ulogin/',  include('django_ulogin.urls')),
    url(r'^logout/',  'django.contrib.auth.views.logout', name='logout'),
    url(r'^media/(?P<path>.*)', 'django.views.static.serve', kwargs={'document_root': settings.MEDIA_ROOT}),
]

