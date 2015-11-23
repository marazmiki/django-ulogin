# coding: utf-8
import sys
from importlib import import_module
from django.core.exceptions import ImproperlyConfigured
from django.utils import six


try:
    from django.utils.module_loading import import_string as import_by_path
except ImportError:
    from django.utils.module_loading import import_by_path
