# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('django_ulogin.views',
    url('^postback/$', 'postback', name='ulogin_postback'),
    url('^ulogin_xd.html$', 'ulogin_xd', name='ulogin_xd'),
)