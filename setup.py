#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
version = __import__('django_ulogin').get_version()
CLASSIFIERS=[
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Framework :: Django'
]

setup(
    name = 'django-ulogin',
    author = 'marazmiki',
    version = version,
    author_email = 'marazmiki@gmail.com',
    url = 'http://pypi.python.org/pypi/django-ulogin',
    download_url = 'http://bitbucket.org/marazmiki/django-ulogin/get/tip.zip',
    description = 'User social authentication with ulogin.ru service',
    long_description = open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    license = 'MIT license',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'Django>=1.2.5',
        'requests',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe = False
)

