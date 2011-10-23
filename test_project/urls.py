from django.conf.urls.defaults import patterns, include, url

try:
    from  django.shortcuts import render
except ImportError:
    from django.views.generic.simple import render_to_view as render

def index(request):
    return render(request, 'index.html')

urlpatterns = patterns('',
    url(r'^$', index, name='home'),
    url(r'^ulogin/', include('django_ulogin.urls')),
    url(r'^logout/', 'django.contrib.auth.views.logout', name='logout')
)
