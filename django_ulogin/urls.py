try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


from django_ulogin.views import (CrossDomainView, IdentityDeleteView,
                                 IdentityListView, PostBackView)

urlpatterns = [
    re_path(r'^identities/$', IdentityListView.as_view(),
            name='ulogin_identities_list'),
    re_path(r'^identities/(?P<pk>\d+)/delete/$', IdentityDeleteView.as_view(),
            name='ulogin_identities_delete'),
    re_path(r'^postback/$', PostBackView.as_view(), name='ulogin_postback'),
    re_path(r'^ulogin_xd.html$', CrossDomainView.as_view(), name='ulogin_xd'),
]
