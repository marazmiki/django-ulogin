from django import VERSION as DJANGO_VERSION

__all__ = ['reverse', 'reverse_lazy', 'user_is_authenticated']


try:
    from django.core.urlresolvers import reverse, reverse_lazy
except ImportError:
    from django.urls import reverse, reverse_lazy


def user_is_authenticated(user):
    if DJANGO_VERSION >= (1, 10):
        return user.is_authenticated
    else:
        return user.is_authenticated()
