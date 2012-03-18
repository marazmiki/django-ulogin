# -*- coding: utf-8 -*-

from django.conf import settings as s
from django_ulogin.exceptions import SchemeNotFound

# URL
WIDGET_URL = getattr(s, 'ULOGIN_WIDGET_URL', 'http://ulogin.ru/js/ulogin.js')

# URL to get token
TOKEN_URL = getattr(s, 'ULOGIN_TOKEN_URL', 'http://ulogin.ru/token.php')

REDIRECT_URL = getattr(s, 'ULOGIN_REDIRECT_URL', None)

################################################################################
# Currently ULOGIN supports these fields                                       #
################################################################################
#
#    first_name
#    last_name
#    email
#    nickname
#    bdate      - user birthday in 'DD.MM.YYYY' format;
#    sex        - user gender in integer: 1 for "Female", 2 for Male;
#    photo      - Square avatar (up to 100x100);
#    photo_big  - Bigest photo provided by social network;
#    city
#    country
#
################################################################################

# Required fields
FIELDS = getattr(s, 'ULOGIN_FIELDS', ['email'])

# Optional fields
OPTIONAL = getattr(s, 'ULOGIN_OPTIONAL', [])

# Display type. The variants 'panel', 'small' and 'button' are available
DISPLAY = getattr(s, 'ULOGIN_DISPLAY', 'small')

# Featured providers
PROVIDERS = getattr(s, 'ULOGIN_PROVIDERS', 
                'vkontakte,facebook,twitter,google,livejournal'.split(','))

# Providers in dropdown list
HIDDEN = getattr(s, 'ULOGIN_HIDDEN',
                 'yandex,odnoklassniki,mailru,openid'.split(','))

# Callback function
CALLBACK = getattr(s, 'ULOGIN_CALLBACK', None)

DEFAULT_SCHEME = {
    'FIELDS'    : FIELDS,
    'OPTIONAL'  : OPTIONAL,
    'DISPLAY'   : DISPLAY,
    'PROVIDERS' : PROVIDERS,
    'HIDDEN'    : HIDDEN,
    'CALLBACK'  : CALLBACK,
}

SCHEMES = getattr(s, 'ULOGIN_SCHEMES', {'default': DEFAULT_SCHEME })

def get_scheme(name):
    try:
        scheme = SCHEMES[name]
    except KeyError:
        raise SchemeNotFound, "Scheme with name {name} not found".format(name=name)
    return {
        'FIELDS'    : scheme.get('FIELDS',    FIELDS),
        'OPTIONAL'  : scheme.get('OPTIONAL',  OPTIONAL),
        'DISPLAY'   : scheme.get('DISPLAY',   DISPLAY),
        'PROVIDERS' : scheme.get('PROVIDERS', PROVIDERS),
        'HIDDEN'    : scheme.get('HIDDEN',    HIDDEN),
        'CALLBACK'  : scheme.get('CALLBACK',  CALLBACK),
    }