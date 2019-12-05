import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from django_ulogin import settings as s
from django_ulogin.compat import py2_unicode_compatible, reverse, text_type
from django_ulogin.utils import import_by_path

AUTH_USER_MODEL = (
    getattr(settings, 'ULOGIN_USER_MODEL', None) or
    getattr(settings, 'AUTH_USER_MODEL', None) or
    'auth.User'
)


@py2_unicode_compatible
class ULoginUser(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,
                             related_name='ulogin_users',
                             verbose_name=_('user'),
                             on_delete=models.CASCADE)
    network = models.CharField(_('network'),
                               db_index=True,
                               max_length=255,
                               choices=s.ALLOWED_PROVIDERS)
    identity = models.URLField(_('identity'),
                               db_index=True,
                               max_length=255)
    uid = models.CharField(_('uid'),
                           db_index=True,
                           max_length=255)
    date_created = models.DateTimeField(_('date created'),
                                        editable=False,
                                        default=now)

    def __str__(self):
        return text_type(self.user)

    def get_delete_url(self):
        return reverse('ulogin_identities_delete', args=[self.pk])

    class Meta(object):
        app_label = 'django_ulogin'
        verbose_name = _('ulogin user')
        verbose_name_plural = _('ulogin users')
        unique_together = [('network', 'uid')]


def create_user(request, ulogin_response):
    """
    This function creates a new "user" instance based on response
    we got from ULOGIN.

    You can invent your own behavior and make django-ulogin to use
    it by specifing it in your Django's project settings module:


    # settings.py
    # ... a bunch of other settings
    ULOGIN_CREATE_USER_CALLBACK = 'my_app.utils.my_own_ulogin_create_user'

    Note, the function should accept two arguments named "request"
    and "ulogin_response"


    """
    # Custom behaviour
    if s.CREATE_USER_CALLBACK is not None:
        callback = import_by_path(s.CREATE_USER_CALLBACK)

        if callable(callback):
            return callback(request=request,
                            ulogin_response=ulogin_response)

        raise ImproperlyConfigured(
            "The ULOGIN_CREATE_USER_CALLBACK isn't a callable"
        )

    # Default behavior
    User = get_user_model()

    return User.objects.create_user(
        username=uuid.uuid4().hex[:30],
        password=get_random_string(10, '0123456789abcdefghijklmnopqrstuvwxyz'),
        email=''
    )
