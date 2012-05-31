# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django_ulogin import settings as s


try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now


class ULoginUser(models.Model):
    user = models.ForeignKey(User,
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
        default = now)

    def __unicode__(self):
        return unicode(self.user)

    @models.permalink
    def get_delete_url(self):
        return 'ulogin_identities_delete', [self.pk]

    class Meta:
        verbose_name = _('ulogin user')
        verbose_name_plural = _('ulogin users')
        unique_together = [('network', 'uid')]
