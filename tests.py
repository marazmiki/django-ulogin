#!/usr/bin/env python
# coding: utf-8

from django.conf import settings
from django import VERSION as DJANGO_VERSION
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


class DisableMigrations:
    """
    Migration disable class
    """
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return 'no_migrations_here' if DJANGO_VERSION < (1, 11) else None


TESTS_SETTINGS = {
    'DEBUG': False,
    'ROOT_URLCONF': 'django_ulogin.tests.urls',
    'MIGRATION_MODULES': DisableMigrations(),
    'MIDDLEWARE_CLASSES': (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    ),
    'INSTALLED_APPS': (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django_ulogin',
    ),
    'PASSWORD_HASHERS': [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    'TEMPLATES': [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
        },
    ]
}

if DJANGO_VERSION >= (1, 10):
    TESTS_SETTINGS['MIDDLEWARE'] = TESTS_SETTINGS.pop('MIDDLEWARE_CLASSES')

settings.configure(**TESTS_SETTINGS)


def main():
    from django.test.utils import get_runner
    import django

    if hasattr(django, 'setup'):
        django.setup()

    find_pattern = 'django_ulogin.tests'

    test_runner = get_runner(settings)(verbosity=2, interactive=True)
    failed = test_runner.run_tests([find_pattern])
    sys.exit(failed)


if __name__ == '__main__':
    main()
