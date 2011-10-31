# -*- coding: utf-8 -*-

from django.contrib.auth import login
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django_ulogin import settings
from django_ulogin.models import ULoginUser
from django_ulogin.signals import assign
import requests
import uuid

try:
    from django.shortcuts import render
except ImportError:
    from django.views.generic.simple import direct_to_template as render

def ulogin_response(token, host):
    """
    """
    return simplejson.loads(requests.get(settings.TOKEN_URL, params={
                               'token' : token,
                               'host'  : host
                           }).content)

@csrf_exempt
def postback(request):
    """
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    if 'token' not in request.POST:
        return HttpResponseBadRequest()

    response = ulogin_response(request.POST['token'], request.get_host())

    if 'error' in response:
        return render(request, 'django_ulogin/error.html', {'json': response})

    if request.user.is_authenticated():
        user = request.user
        registered = False
        ulogin = None

        if not request.user.ulogin_users.count():
            ulogin = ULoginUser.objects.create(network  = response['network'],
                                               uid      = response['uid'],
                                               identity = response['identity'],
                                               user     = user)
            registered = True
    # Not authenticated
    else:
        try:
            ulogin = ULoginUser.objects.get(network=response['network'],
                                            uid=response['uid'])
            registered = False
            user = ulogin.user

        except ULoginUser.DoesNotExist:
            user = User()
            user.username=uuid.uuid4().hex[:30]
            user.set_unusable_password()
            user.save()

            ulogin = ULoginUser.objects.create(network  = response['network'],
                                               uid      = response['uid'],
                                               identity = response['identity'],
                                               user     = user)
            registered = True

        # Authenticate user
        if not hasattr(user, 'backend'):
            user.backend = 'django.contrib.auth.backends.ModelBackend'

        login(request, user)

    # End of not authenticated
    assign.send(sender=ULoginUser, request=request, user=user,
                registered=registered,
                ulogin_user=ulogin, ulogin_data=response)

    return redirect('/')

def ulogin_xd(request):
    """
    Document for avoid cross domain security policies
    """
    return render(request, 'django_ulogin/ulogin_xd.html')