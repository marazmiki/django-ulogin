# coding: utf-8

import uuid
import sys
from importlib import import_module
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


try:
    from django.utils.crypto import get_random_string
except ImportError:
    import string
    import random
    import hashlib
    import time

    try:
        random = random.SystemRandom()
        using_sysrandom = True
    except NotImplementedError:
        import warnings
        warnings.warn('A secure pseudo-random number generator is not available '
                      'on your system. Falling back to Mersenne Twister.')
        using_sysrandom = False

    def get_random_string(length=12, allowed_chars=string.letters + string.digits):
        if not using_sysrandom:
            random.seed(hashlib.sha256(("%s%s%s" % (random.getstate(),
                                                    time.time(),
                                                    settings.SECRET_KEY)).encode('utf-8')
                                       ).digest())
        return ''.join([random.choice(allowed_chars) for i in range(length)])


from django_ulogin import settings as s

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User as DjUser
    get_user_model = lambda: DjUser

try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now


try:
    AUTH_USER_MODEL = settings.AUTH_USER_MODEL
except AttributeError:
    AUTH_USER_MODEL = 'auth.User'


try:
    from django.utils.module_loading import import_by_path
except ImportError:
    import six

    def import_by_path(dotted_path, error_prefix=''):
        """
        Import a dotted module path and return the attribute/class designated by the
        last name in the path. Raise ImproperlyConfigured if something goes wrong.
        """
        try:
            module_path, class_name = dotted_path.rsplit('.', 1)
        except ValueError:
            raise ImproperlyConfigured("%s%s doesn't look like a module path" % (
                                       error_prefix, dotted_path))
        try:
            module = import_module(module_path)
        except ImportError as e:
            msg = '%sError importing module %s: "%s"' % (
                error_prefix, module_path, e)
            six.reraise(ImproperlyConfigured, ImproperlyConfigured(msg),
                        sys.exc_info()[2])
        try:
            attr = getattr(module, class_name)
        except AttributeError:
            raise ImproperlyConfigured('%sModule "%s" does not define a "%s" attribute/class' % (
                error_prefix, module_path, class_name))
        return attr


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
    if s.CREATE_USER_CALLBACK is not None:
        callback = import_by_path(s.CREATE_USER_CALLBACK)
        if callable(callback):
            return callback(request=request, ulogin_response=ulogin_response)
        raise ImproperlyConfigured("The ULOGIN_CREATE_USER_CALLBACK isn't a callable")

    # Default behavior
    User = get_user_model()
    return User.objects.create_user(username=uuid.uuid4().hex,
                                    password=get_random_string(10, '0123456789abcdefghijklmnopqrstuvwxyz'),
                                    email='')
