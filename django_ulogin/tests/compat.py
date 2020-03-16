from django import test
from django.contrib.auth.models import User

from django_ulogin import compat


class TextTypeTest(test.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='j.doe')

    def test_(self):
        self.assertEqual(compat.text_type(self.user), self.user.username)
