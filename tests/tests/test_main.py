# -*- coding: utf-8 -*-

from django import test
from django.template import Template, Context
from django.contrib.auth.models import User
from django_ulogin import views
from django_ulogin.exceptions import SchemeNotFound
from django_ulogin.models import ULoginUser
from django_ulogin.signals import assign
from django_ulogin.settings import get_scheme
from django.urls import reverse

# class Test(test.TestCase):
#     """
#     """
#     urls = 'django_ulogin.tests.urls'
#
#     def setUp(self):
#         self.client = test.Client()
#         self.url = reverse('ulogin_postback')
#         views.PostBackView.ulogin_response = \
#             lambda cls, token, host: response(None)


def test_has_error(client, ulogin_postback_url):
    expected_error = {'error': 'Token expired'}

    resp = client.post(ulogin_postback_url, data={'token': '31337'})

    assert resp.status_code == 200
    assert resp.json() == expected_error


def test_405_if_not_post(client, ulogin_postback_url):
    resp = client.get(ulogin_postback_url)
    assert resp.status_code == 405


def test_400_if_no_token_given(client, ulogin_postback_url):
    resp = client.post(ulogin_postback_url)
    assert resp.status_code == 400


def test_302_if_post_and_token_given(client, ulogin_postback_url):
    resp = client.post(ulogin_postback_url, data={'token': '31337'})
    assert resp.status_code == 302


def test_user_is_created(client, ulogin_postback_url):
    """
    Test that user is created
    """
    assert User.objects.count() == ULoginUser.objects.count() == 0
    client.post(ulogin_postback_url, data={'token': '31337'})
    assert User.objects.count() == ULoginUser.objects.count() == 1


def test_assign_user(client, ulogin_postback_url):
    username, password = 'demo', 'demo'

    User.objects.create_user(username=username,
                             password=password,
                             email='demo@demo.de')

    assert User.objects.count() == 1
    assert ULoginUser.objects.count() == 0

    client.login(username=username, password=password)
    client.post(ulogin_postback_url, data={'token': '31337'})

    assert User.objects.count() == ULoginUser.objects.count() == 1


def test_no_duplicates_when_posting_twice(client, ulogin_postback_url):
    assert User.objects.count() == ULoginUser.objects.count() == 0

    client.post(ulogin_postback_url, data={'token': '31337'})
    client.post(ulogin_postback_url, data={'token': '31337'})

    assert User.objects.count() == ULoginUser.objects.count() == 1


def test_user_logged(client, ulogin_postback_url):
    resp = client.post(ulogin_postback_url, data={'token': 31331}, follow=True)
    assert resp.status_code == 200
    assert resp.context['request'].user.is_authenticated


def test_user_authenticated_ulogin_not_exists(client, ulogin_postback_url):
    username, password = 'demo', 'demo'
    User.objects.create_user(username=username,
                             password=password,
                             email='demo@demo.de')

    def handler(**kwargs):
        assert kwargs['registered']

    assign.connect(receiver=handler, sender=ULoginUser, dispatch_uid='test')

    client.login(username=username, password=password)
    client.post(ulogin_postback_url, data={'token': '31337'})
    assign.disconnect(receiver=handler, sender=ULoginUser, dispatch_uid='test')


def test_user_authenticated_ulogin_exists(client, ulogin_postback_url,
                                          response_mocker):
    username, password = 'demo', 'demo'
    user = User.objects.create_user(username=username, password=password,
                                    email='demo@demo.de')

    def handler(**kwargs):
        assert not kwargs['registered']

    response_mocker.apply()
    data = response_mocker.response_data

    ULoginUser.objects.create(user=user, network=data['network'],
                              uid=data['uid'])

    assign.connect(receiver=handler, sender=ULoginUser, dispatch_uid='test')
    client.login(username=username, password=password)
    client.post(ulogin_postback_url, data={'token': '31337'})
    assign.disconnect(receiver=handler, sender=ULoginUser, dispatch_uid='test')


def test_user_authenticated_and_some_ulogins(client, ulogin_postback_url):
    username, password = 'demo', 'demo'
    user = User.objects.create_user(username=username,
                                    password=password,
                                    email='demo@demo.de')
    client.login(username=username, password=password)
    # First account
    client.post(ulogin_postback_url, data={'token': '31337'})

    views.PostBackView.ulogin_response = \
        lambda cls, token, host: response({'network': 'twitter',
                                           'uid': 'django',
                                           'identity': ('http://twitter.'
                                                        'com/django')})

    # Second account
    qset = ULoginUser.objects.filter(user=user)
    client.post(ulogin_postback_url, data={'token': '31337'})
    self.assertEquals(2, qset.count())
    self.assertEquals(1, qset.filter(network='vkontakte').count())
    self.assertEquals(1, qset.filter(network='twitter').count())

def test_user_not_authenticated_ulogin_exists(client, ulogin_postback_url):
    """
    Tests received from view data when user is not authenticated and
    ulogin exists
    """
    def handler(**kwargs):
        ''
        self.assertFalse(kwargs['registered'])

    username, password = 'demo', 'demo'
    user = User.objects.create_user(username=username,
                                    password=password,
                                    email='demo@demo.de')
    ULoginUser.objects.create(user=user,
                              network=response()['network'],
                              uid=response()['uid'])

    assign.connect(receiver=handler, sender=ULoginUser,
                   dispatch_uid='test')
    client.post(ulogin_postback_url, data={'token': '31337'})
    assign.disconnect(receiver=handler, sender=ULoginUser,
                      dispatch_uid='test')

def test_user_not_authenticated_ulogin_not_exists(client, ulogin_postback_url):
    """
    Tests received from view data when user is not authenticated and
    ulogin not exists
    """
    username, password = 'demo', 'demo'
    User.objects.create_user(username=username,
                             password=password,
                             email='demo@demo.de')

    def handler(**kwargs):
        self.assertTrue(kwargs['registered'])

    assign.connect(receiver=handler, sender=ULoginUser,
                   dispatch_uid='test')
    client.post(ulogin_postback_url, data={'token': '31337'})
    assign.disconnect(receiver=handler, sender=ULoginUser,
                      dispatch_uid='test')

def test_wrong_scheme(client, ulogin_postback_url):
    def exception():
        get_scheme('unknown_scheme')
    self.assertRaises(SchemeNotFound, exception)

def test_wrong_scheme_in_template(client, ulogin_postback_url):
    t = Template(
        """{% load ulogin_tags %}{% ulogin_widget "unknown_scheme" %}"""
    ).render(Context({}))
    self.assertIn('[ulogin]: scheme unknown_scheme not found', t)

def test_default_scheme(client, ulogin_postback_url):
    s = get_scheme('default')

    for i in ['PROVIDERS', 'FIELDS', 'CALLBACK', 'HIDDEN',
              'OPTIONAL', 'DISPLAY']:
        self.assertIn(i, s)


from tests.tests.identities import (LoginRequiredTest,   # NOQA
                                    TestIdentityList,    # NOQA
                                    TestIdentifyDelete)  # NOQA
from tests.tests.templatetags import ULoginMediaTest  # NOQA
