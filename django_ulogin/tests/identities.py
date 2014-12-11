# coding: utf-8

from django import test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django_ulogin.models import ULoginUser


JOHN, PASSWORD, EMAIL = 'john', 'demo', 'user@example.com'
JANE = 'jane'


class LoginRequiredTest(test.TestCase):
    """
    Base class for testing features available to authenticated users
    """

    def setUp(self):
        self.john = User.objects.create_user(username=JOHN, password=PASSWORD,
                                             email=EMAIL)
        self.jane = User.objects.create_user(username=JANE, password=PASSWORD,
                                             email=EMAIL)
        self.client = test.Client()
        self.url = reverse('ulogin_identities_list')

        for u in [self.john, self.jane]:
            for i in ['vkontakte', 'twitter', 'facebook']:
                u.ulogin_users.create(
                    network=i,
                    uid=u.username + i,
                    identity='http://' + i + '/' + u.username + i
                )
        self.client.login(username=self.john.username, password=PASSWORD)

    def test_login_required_if_user_not_authenticated(self):
        self.client.logout()
        page = self.client.get(self.url)
        self.assertEquals(302, page.status_code)


class TestIdentityList(LoginRequiredTest):
    def test_1(self):
        page = self.client.get(self.url)

        self.assertEquals(200, page.status_code)
        self.assertIn('identities', page.context)
        self.assertEquals(3, page.context['identities'].count())

        for i in page.context['identities'].all():
            self.assertEquals(self.john, i.user)

    def test_2(self):
        page = self.client.get(self.url)
        self.assertEquals(
            0,
            page.context['identities'].filter(user=self.jane).count()
        )


class TestIdentifyDelete(LoginRequiredTest):
    def test_1(self):
        page = self.client.get(self.url)

        self.assertEquals(200, page.status_code)
        self.assertIn('identities', page.context)
        self.assertEquals(3, page.context['identities'].count())

    def test_2(self):
        page = self.client.get(self.url)

        self.assertEquals(200, page.status_code)

        for account in page.context['identities'].all():
            url = account.get_delete_url()

            page = self.client.get(url)
            self.assertEquals(200, page.status_code)
            self.client.post(account.get_delete_url())
            page = self.client.get(url)
            self.assertEquals(404, page.status_code)

    def test_3(self):
        for foreign_account in ULoginUser.objects.filter(user=self.jane):
            page = self.client.get(foreign_account.get_delete_url())
            self.assertEquals(404, page.status_code)
