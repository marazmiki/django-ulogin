#!/usr/bin/env python
# coding: utf-8

from django.conf import settings
from django.core.management import call_command
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


settings.configure(ROOT_URLCONF='django_ulogin.tests.urls',
                   INSTALLED_APPS=('django.contrib.auth',
                                   'django.contrib.contenttypes',
                                   'django.contrib.sessions',
                                   'django_ulogin',),
                   DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                                          'NAME': ':MEMORY:'}
                              })

if __name__ == '__main__':
    call_command('test', 'django_ulogin')
