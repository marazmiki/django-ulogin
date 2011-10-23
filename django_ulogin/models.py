# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django_ulogin import settings as s
import datetime

class ULoginUser(models.Model):
    user = models.ForeignKey(User,
        related_name = 'ulogin_users',
        verbose_name = _('user'))
    network = models.CharField(_('network'),
        db_index = True,
        max_length = 255,
        choices = [(n, n) for n in (s.PROVIDERS + s.OPTIONAL)])
    identity = models.URLField(_('identity'),
        db_index = True,
        max_length = 255)
    uid = models.CharField(_('uid'),
        db_index = True,
        max_length = 255)
    date_created = models.DateTimeField(_('date created'),
        editable = False,
        default = datetime.datetime.now)

    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = _('ulogin user')
        verbose_name_plural = _('ulogin users')
        unique_together = [('network', 'uid')]
