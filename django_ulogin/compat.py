# coding: utf-8

from django import VERSION as DJANGO_VERSION


def user_is_authenticated(user):
    if DJANGO_VERSION >= (1, 10):
        return user.is_authenticated
    else:
        return user.is_authenticated()
