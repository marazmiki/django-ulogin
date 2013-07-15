# coding: utf-8

from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import get_random_string
from django.utils.module_loading import import_by_path
from django_ulogin import settings as s
import uuid

try:
    from django.contrib.auth import get_user_model
except ImportError:
    def get_user_model():
        from django.contrib.auth.models import User
        return User

try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now


class ULoginUser(models.Model):
    user = models.ForeignKey(get_user_model(),
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

    def __unicode__(self):
        return unicode(self.user)

    @models.permalink
    def get_delete_url(self):
        return 'ulogin_identities_delete', [self.pk]

    class Meta(object):
        verbose_name = _('ulogin user')
        verbose_name_plural = _('ulogin users')
        unique_together = [('network', 'uid')]

def create_user(request, ulogin_response):
    """
    Creates user
    """
    # Custom behaviour
    if settings.CREATE_USER_CALLBACK is not None:
        callback = import_by_path(settings.CREATE_USER_CALLBACK)
        if callable(callback):
            return callback(request=request, ulogin_response=ulogin_response)
        raise ImproperlyConfigured("The ULOGIN_CREATE_USER_CALLBACK isn't a callable")

    # Default behavior
    User = get_user_model()
    return User.objects.create_user(username=uuid.uuid4().hex,
                                    password=get_random_string(10, '0123456789abcdefghijklmnopqrstuvwxyz'),
                                    email='')


