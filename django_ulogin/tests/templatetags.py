# coding: utf-8

from django import test
from django.template import Template, Context
from django_ulogin import settings


class UloginWidgetTest(test.TestCase):
    """"""


class ULoginMediaTest(test.TestCase):
    """"""
    TEMPLATE = Template('{% load ulogin_tags %}{% ulogin_media %}')

    def test_1(self):
        t = self.TEMPLATE.render(Context())
        self.assertIn(settings.WIDGET_URL, t)
