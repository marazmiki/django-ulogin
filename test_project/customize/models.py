from django.db import models
from django_ulogin.models import ULoginUser
from django_ulogin.signals import assign

def catch_ulogin_signal(*args, **kwargs):
    print kwargs

assign.connect(receiver = catch_ulogin_signal,
               sender   = ULoginUser,
               dispatch_uid = 'customize.models')

