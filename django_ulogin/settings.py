# coding: utf-8

from django.conf import settings as s
from django.utils.translation import ugettext_lazy as _
from django_ulogin.exceptions import SchemeNotFound


ALLOWED_PROVIDERS = (
    ('vkontakte', _('V Kontakte')),
    ('odnoklassniki', _('Odnoklassniki')),
    ('mailru', _('Mail.Ru')),
    ('yandex', _('Yandex')),
    ('lastfm', _('Last.FM')),
    ('linkedin', _('LinkedIn')),
    ('google', _('Google')),
    ('soundcloud', _('SoundCloud')),
    ('steam', _('Steam')),
    ('liveid', _('Windows Live ID')),
    ('vimeo', _('Vimeo')),
    ('openid', _('OpenID')),
    ('webmoney', _('WebMoney')),
    ('flickr', _('Flickr')),
    ('youtube', _('YouTube')),
    ('livejournal', _('LiveJournal')),
    ('twitter', _('Twitter')),
    ('facebook', _('Facebook')),
    ('foursquare', _('Foursquare')),
    ('googleplus', _('Google+')),
    ('tumblr', _('Tumblr')),
    ('dudu', _('Dudu')),
)


ALLOWED_FIELDS = (
    ('first_name', _('First name')),
    ('last_name', _('Last name')),
    ('email', _('E-mail')),
    ('nickname', _('Nickname')),
    ('bdate', _('Birthday')),
    ('sex', _('Sex')),
    ('photo', _('Photo')),
    ('photo_big', _('Big photo')),
    ('city', _('City')),
    ('country', _('Country')),
    ('phone', _('Phone')),
)


SEX_CHOICES = (
    (1, _('female')),
    (2, _('male')),
)


# URL of widget
WIDGET_URL = getattr(s, 'ULOGIN_WIDGET_URL', '//ulogin.ru/js/ulogin.js')

# URL to get token
TOKEN_URL = getattr(s, 'ULOGIN_TOKEN_URL', 'https://ulogin.ru/token.php')

REDIRECT_URL = getattr(s, 'ULOGIN_REDIRECT_URL', None)

LOAD_SCRIPT_AT_ONCE = getattr(s, 'ULOGIN_LOAD_SCRIPT_AT_ONCE', False)

#
# Default settings
#

# Required fields
FIELDS = getattr(s, 'ULOGIN_FIELDS', ['email'])

# Optional fields
OPTIONAL = getattr(s, 'ULOGIN_OPTIONAL', [])

# Display type. The variants 'panel', 'small' and 'button' are available
DISPLAY = getattr(s, 'ULOGIN_DISPLAY', 'small')

# Featured providers
PROVIDERS = getattr(s, 'ULOGIN_PROVIDERS', ['vkontakte', 'facebook',
                                            'twitter', 'google',
                                            'livejournal'])

# Providers in dropdown list
HIDDEN = getattr(s, 'ULOGIN_HIDDEN', ['yandex', 'odnoklassniki', 'mailru',
                                      'openid'])

# Callback function
CALLBACK = getattr(s, 'ULOGIN_CALLBACK', None)

DEFAULT_SCHEME = {
    'FIELDS': FIELDS,
    'OPTIONAL': OPTIONAL,
    'DISPLAY': DISPLAY,
    'PROVIDERS': PROVIDERS,
    'HIDDEN': HIDDEN,
    'CALLBACK': CALLBACK,
}

VERIFY_EMAIL = getattr(s, 'ULOGIN_VERIFY_EMAIL', False)

SCHEMES = getattr(s, 'ULOGIN_SCHEMES', {'default': DEFAULT_SCHEME})

AUTHENTICATION_BACKEND = getattr(s,
                                 'ULOGIN_AUTHENTICATION_BACKEND',
                                 'django.contrib.auth.backends.ModelBackend')

CREATE_USER_CALLBACK = getattr(s, 'ULOGIN_CREATE_USER_CALLBACK', None)
LOGIN_CALLBACK = getattr(s, 'ULOGIN_LOGIN_CALLBACK', None)

REQUEST_USER = getattr(s, 'ULOGIN_REQUEST_USER', 'user')


def get_scheme(name):
    try:
        scheme = SCHEMES[name]
    except KeyError:
        raise SchemeNotFound(
            "Scheme with name {name} not found".format(name=name))
    return {
        'FIELDS': scheme.get('FIELDS', FIELDS),
        'OPTIONAL': scheme.get('OPTIONAL', OPTIONAL),
        'DISPLAY': scheme.get('DISPLAY', DISPLAY),
        'PROVIDERS': scheme.get('PROVIDERS', PROVIDERS),
        'HIDDEN': scheme.get('HIDDEN', HIDDEN),
        'CALLBACK': scheme.get('CALLBACK', CALLBACK),
    }
