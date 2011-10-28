from django.conf import settings
from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url

try:
    from  django.shortcuts import render
except ImportError:
    from django.views.generic.simple import render_to_view as render

def index(request):
    return render(request, 'index.html')

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index, name='home'),
    url(r'^admin/',   include(admin.site.urls)),
    url(r'^ulogin/',  include('django_ulogin.urls')),
    url(r'^logout/',  'django.contrib.auth.views.logout', name='logout'),
    url(r'^media/(?P<path>.*)',   'django.views.static.serve', kwargs={'document_root': settings.MEDIA_ROOT}),
)
