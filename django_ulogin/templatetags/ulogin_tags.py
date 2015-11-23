# coding: utf-8

from django import template
from django.core.urlresolvers import reverse as r
from django.contrib.auth import REDIRECT_FIELD_NAME as FLD
from django_ulogin import settings as s
from django_ulogin.exceptions import SchemeNotFound
from django.utils.http import urlquote
import urllib
import string
import random


try:
    from django.utils.encoding import smart_unicode
except ImportError:
    from django.utils.encoding import smart_text as smart_unicode


def get_redirect_url(request):
    if getattr(s, 'REDIRECT_URL'):
        return s.REDIRECT_URL

    # Hack the request.GET
    if FLD not in request.GET:
        get = request.GET.copy()
        get.update({
            FLD: request.build_absolute_uri(request.path_info)
        })
        request.GET = get

    if hasattr(urllib, 'unquote'):
        unquote = urllib.unquote
    else:
        unquote = urllib.parse.unquote

    return urlquote(u"{request_url}?{query_string}".format(
        request_url=request.build_absolute_uri(r('ulogin_postback')),
        query_string=smart_unicode(unquote(request.GET.urlencode()))
    ))


def ulogin_widget(context, name="default"):
    """
    """
    try:
        scheme = s.get_scheme(name)
    except SchemeNotFound:
        return {
            'SCHEME_NOT_FOUND': True,
            'NAME': name
        }

    def glue(key):
        return ','.join([p for p in scheme.get(key, getattr(s, key))])

    rand = ''.join(random.choice(string.ascii_lowercase) for x in range(5))

    return {
        'NAME': name,
        'WIDGET_URL': s.WIDGET_URL,
        'CALLBACK': scheme.get('CALLBACK', s.CALLBACK),
        'DISPLAY': scheme.get('DISPLAY', s.DISPLAY),
        'PROVIDERS': glue('PROVIDERS'),
        'HIDDEN': glue('HIDDEN'),
        'FIELDS': glue('FIELDS'),
        'OPTIONAL': glue('OPTIONAL'),
        'REDIRECT_URL': get_redirect_url(context['request']),
        'RAND': rand,
        'LOAD_SCRIPT_AT_ONCE': s.LOAD_SCRIPT_AT_ONCE
    }

register = template.Library()
register.inclusion_tag('django_ulogin/ulogin_widget.html',
                       takes_context=True)(ulogin_widget)


def ulogin_media(context):
    return {
        'WIDGET_URL': s.WIDGET_URL,
    }


register.inclusion_tag('django_ulogin/ulogin_media.html',
                       takes_context=True)(ulogin_media)
