#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import os

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
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Framework :: Django'
]

install_requires = ['Django',
                    'requests',
                    'six']
tests_require = ['Django',
                 'requests',
                 'tox',
                 'six']


dl_url = 'https://github.com/marazmiki/django-ulogin/archive/master.zip'


setup(
    name='django-ulogin',
    author='Mikhail Porokhovnichenko <marazmiki@gmail.com>',
    version=version,
    author_email='marazmiki@gmail.com',
    url='https://github.com/marazmiki/django-ulogin',
    download_url=dl_url,
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
