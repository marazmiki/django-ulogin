# -*- coding: utf-8 -*-

from django import template
from django.core.urlresolvers import reverse as r
from django.contrib.auth import REDIRECT_FIELD_NAME as FLD
from django_ulogin import settings as s
import urllib
import string, random

def get_redirect_url(request):
    if getattr(s, 'REDIRECT_URL'):
        return s.REDIRECT_URL

    # Current URL
    return_url = request.build_absolute_uri(request.path_info)

    # Hack the request.GET
    if FLD not in request.GET:
        get = request.GET.copy()
        get.update({ FLD: request.build_absolute_uri(request.path_info) })
        request.GET = get
    
    return urllib.quote(u"{request_url}?{query_string}".format(
        request_url  = request.build_absolute_uri(r('ulogin_postback')),
        query_string = urllib.unquote(request.GET.urlencode())
        ))

def ulogin_widget(context, name="default"):
    """
    """
    scheme = s.get_scheme(name)
    return {
        'WIDGET_URL'   : s.WIDGET_URL,
        'CALLBACK'     : s.CALLBACK,
        'DISPLAY'      : scheme['DISPLAY'],
        'PROVIDERS'    : ','.join([p for p in scheme['PROVIDERS']]),
        'HIDDEN'       : ','.join([h for h in scheme['HIDDEN']]),
        'FIELDS'       : ','.join([f for f in s.FIELDS]),
        'OPTIONAL'     : ','.join([o for o in s.OPTIONAL]),
        'REDIRECT_URL' : get_redirect_url(context['request']),
        'RAND'         : ''.join(random.choice(string.ascii_lowercase) for x in range(5)),
    }

register = template.Library()
register.inclusion_tag('django_ulogin/ulogin_widget.html',
                       takes_context=True)(ulogin_widget)