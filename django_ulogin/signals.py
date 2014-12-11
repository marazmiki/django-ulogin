# coding: utf-8

from django.dispatch import Signal

assign = Signal(providing_args=['request', 'user', 'ulogin_user',
                                'ulogin_data', 'registered'])
