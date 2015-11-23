# coding: utf-8

try:
    from django.utils.module_loading import import_string as import_by_path
except ImportError:
    from django.utils.module_loading import import_by_path


__all__ = ['import_by_path']
