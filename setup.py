#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import os
import sys

py_version = sys.version_info
version = __import__('django_ulogin').get_version()
readme = os.path.join(os.path.dirname(__file__), 'README.rst')

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Framework :: Django'
]

install_requires = ['Django',
                    'requests',
                    'mock>=0.8.0',
                    'six']
tests_require = ['Django',
                 'requests',
                 'six']


if isinstance(py_version, tuple):
    if py_version < (2, 7):
        install_requires.append('importlib')


setup(
    name='django-ulogin',
    author='Mikhail Porokhovnichenko <marazmiki@gmail.com>',
    version=version,
    author_email='marazmiki@gmail.com',
    url='http://pypi.python.org/pypi/django-ulogin',
    download_url='http://bitbucket.org/marazmiki/django-ulogin/get/tip.zip',
    description='User social authentication with ulogin.ru service',
    long_description=open(readme).read(),
    license='MIT license',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=install_requires,
    packages=find_packages(exclude=['test_project', 'test_project.*']),
    test_suite='tests.main',
    tests_require=tests_require,
    include_package_data=True,
    zip_safe=False)
