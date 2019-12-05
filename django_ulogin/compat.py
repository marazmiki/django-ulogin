from django import VERSION as DJANGO_VERSION

__all__ = [
    'reverse', 'reverse_lazy',
    'py2_unicode_compatible', 'text_type',
    'user_is_authenticated',
]


py2_unicode_compatible = lambda f: f    # NOQA
text_type = lambda s: s                 # NOQA


try:
    from django.core.urlresolvers import reverse, reverse_lazy
except ImportError:
    from django.urls import reverse, reverse_lazy

try:
    from django.utils import six
    py2_unicode_compatible = six.python_2_unicode_compatible
    text_type = six.text_type
except ImportError:
    pass


def user_is_authenticated(user):
    if DJANGO_VERSION >= (1, 10):
        return user.is_authenticated
    else:
        return user.is_authenticated()
