# coding: utf-8

from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import get_random_string
from django.utils import six
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django_ulogin import settings as s
from django_ulogin.utils import import_by_path
import uuid


AUTH_USER_MODEL = (
    getattr(settings, 'ULOGIN_USER_MODEL', None) or
    getattr(settings, 'AUTH_USER_MODEL', None) or
    'auth.User'
)


@six.python_2_unicode_compatible
class ULoginUser(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,
                             related_name='ulogin_users',
                             verbose_name=_('user'))
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
        return six.text_type(self.user)

    @models.permalink
    def get_delete_url(self):
        return 'ulogin_identities_delete', [self.pk]

    class Meta(object):
        app_label = 'django_ulogin'
        verbose_name = _('ulogin user')
        verbose_name_plural = _('ulogin users')
        unique_together = [('network', 'uid')]


def create_user(request, ulogin_response):
    """
    Creates user
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
