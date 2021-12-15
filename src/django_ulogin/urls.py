from django.urls import path

from django_ulogin.views import (CrossDomainView, IdentityDeleteView,
                                 IdentityListView, PostBackView)

urlpatterns = [
    path('identities/', IdentityListView.as_view(),
         name='ulogin_identities_list'),
    path('identities/<int:pk>/delete/', IdentityDeleteView.as_view(),
         name='ulogin_identities_delete'),
    path('postback/', PostBackView.as_view(), name='ulogin_postback'),
    path('ulogin_xd.html', CrossDomainView.as_view(), name='ulogin_xd'),
]
