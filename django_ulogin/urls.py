# coding: utf-8

from django.conf.urls import url
from django_ulogin.views import (PostBackView, CrossDomainView,
                                 IdentityListView, IdentityDeleteView)

urlpatterns = [
    url('^identities/$', IdentityListView.as_view(),
        name='ulogin_identities_list'),
    url('^identities/(?P<pk>\d+)/delete/$', IdentityDeleteView.as_view(),
        name='ulogin_identities_delete'),
    url('^postback/$', PostBackView.as_view(), name='ulogin_postback'),
    url('^ulogin_xd.html$', CrossDomainView.as_view(), name='ulogin_xd'),
]
