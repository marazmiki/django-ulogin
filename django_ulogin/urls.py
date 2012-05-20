# coding: utf-8

from django.conf.urls import url
from django_ulogin.views import PostBackView, CrossDomainView, \
    IdentityListView, IdentityDeleteView

urlpatterns = [
    url('^identities/$',
        view=IdentityListView.as_view(),
        name='ulogin_identities_list'),
    url('^identities/(?P<pk>\d+)/delete/$',
        view=IdentityDeleteView.as_view(),
        name='ulogin_identities_delete'),
    url('^postback/$',
        view=PostBackView.as_view(),
        name='ulogin_postback'),
    url('^ulogin_xd.html$',
        view=CrossDomainView.as_view(),
        name='ulogin_xd'),
]
