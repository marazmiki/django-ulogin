# -*- coding: utf-8 -*-

from django import template
from django_ulogin import settings as s
from django.core.urlresolvers import reverse as r


def get_redirect_url(request):
    if getattr(s, 'REDIRECT_URL'):
        return s.REDIRECT_URL
    return request.build_absolute_uri( r('ulogin_postback') ) 

def ulogin_widget(context):
    """
    """
    return {
        'WIDGET_URL'   : s.WIDGET_URL,
        'CALLBACK'     : s.CALLBACK,
        'DISPLAY'      : s.DISPLAY,
        'REDIRECT_URL' : get_redirect_url(context['request']),
        'FIELDS'       : ','.join([f for f in s.FIELDS]),
        'OPTIONAL'     : ','.join([o for o in s.OPTIONAL]),
        'PROVIDERS'    : ','.join([p for p in s.PROVIDERS]),
        'HIDDEN'       : ','.join([h for h in s.HIDDEN]),
    }

register = template.Library()
register.inclusion_tag('django_ulogin/ulogin_widget.html',
                       takes_context=True)(ulogin_widget)
