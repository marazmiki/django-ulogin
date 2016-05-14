# coding: utf-8

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, DeleteView
from django.utils.decorators import method_decorator
from django_ulogin import settings
from django_ulogin.models import ULoginUser, create_user
from django_ulogin.signals import assign
from django_ulogin.forms import PostBackForm
from django_ulogin.utils import import_by_path
import requests
import json
import logging
import sys


logger = logging.getLogger('django_ulogin.views')


def get_user(request):
    return getattr(request, settings.REQUEST_USER)


if settings.LOGIN_CALLBACK:
    login = import_by_path(settings.LOGIN_CALLBACK)
else:
    from django.contrib.auth import login


class CsrfExemptMixin(object):
    """
    A mixin that provides a way to exempt view class out of CSRF validation
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(request, *args, **kwargs)


class LoginRequiredMixin(object):
    """
    A mixin that provides a way to restrict anonymous access
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request,
                                                        *args,
                                                        **kwargs)


class ULoginMixin(LoginRequiredMixin):
    """
    A mixin that provides a set of all identities for current
    authenticated user
    """
    def get_queryset(self):
        return ULoginUser.objects.filter(user=get_user(self.request))


class PostBackView(CsrfExemptMixin, FormView):
    """
    Accepts the post back data from ULOGIN service and authenticates the user
    """

    form_class = PostBackForm
    http_method_names = ['post']
    error_template_name = 'django_ulogin/error.html'

    def handle_authenticated_user(self, response):
        """
        Handles the ULogin response if user is already
        authenticated
        """
        current_user = get_user(self.request)

        ulogin, registered = ULoginUser.objects.get_or_create(
            uid=response['uid'],
            network=response['network'],
            defaults={'identity': response['identity'],
                      'user': current_user})

        if not registered:
            ulogin_user = ulogin.user
            logger.debug('uLogin user already exists')

            if current_user != ulogin_user:
                logger.debug(
                    "Mismatch: %s is not a %s. Take over it!" % (current_user,
                                                                 ulogin_user)
                )
                ulogin.user = current_user
                ulogin.save()

        return get_user(self.request), ulogin, registered

    def handle_anonymous_user(self, response):
        """
        Handles the ULogin response if user is not authenticated (anonymous)
        """
        try:
            ulogin = ULoginUser.objects.get(network=response['network'],
                                            uid=response['uid'])
        except ULoginUser.DoesNotExist:
            user = create_user(request=self.request,
                               ulogin_response=response)
            ulogin = ULoginUser.objects.create(user=user,
                                               network=response['network'],
                                               identity=response['identity'],
                                               uid=response['uid'])
            registered = True
        else:
            user = ulogin.user
            registered = False

        # Authenticate user
        if not hasattr(user, 'backend'):
            user.backend = settings.AUTHENTICATION_BACKEND
        login(self.request, user)

        return user, ulogin, registered

    def form_valid(self, form):
        """
        The request from ulogin service is correct
        """
        response = self.ulogin_response(form.cleaned_data['token'],
                                        self.request.get_host())

        if 'error' in response:
            return render(self.request, self.error_template_name,
                          {'json': response})

        if get_user(self.request).is_authenticated():
            user, identity, registered = \
                self.handle_authenticated_user(response)
        else:
            user, identity, registered = \
                self.handle_anonymous_user(response)

        assign.send(sender=ULoginUser,
                    user=get_user(self.request),
                    request=self.request,
                    registered=registered,
                    ulogin_user=identity,
                    ulogin_data=response)
        return redirect(self.request.GET.get(REDIRECT_FIELD_NAME) or '/')

    def form_invalid(self, form):
        """
        Bad request from service
        """
        return HttpResponseBadRequest()

    def ulogin_response(self, token, host):
        """
        Makes a request to ULOGIN
        """
        response = requests.get(
            settings.TOKEN_URL,
            params={
                'token': token,
                'host': host
            })
        content = response.content

        if sys.version_info >= (3, 0):
            content = content.decode('utf8')

        return json.loads(content)


class CrossDomainView(TemplateView):
    """
    Document for avoid cross domain security policies
    """
    template_name = 'django_ulogin/ulogin_xd.html'


class IdentityListView(ULoginMixin, ListView):
    """
    The list of all social identities for current authenticated user
    """
    template_name = 'django_ulogin/identities.html'
    context_object_name = 'identities'


class IdentityDeleteView(ULoginMixin, DeleteView):
    """
    Deletes the given social identity from current authenticated user
    """
    template_name = 'django_ulogin/confirm_delete.html'
    context_object_name = 'identity'

    def get_success_url(self):
        return reverse('ulogin_identities_list')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {'instance': self.get_object()
                       })
