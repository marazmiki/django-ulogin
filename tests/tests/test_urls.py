from django.http import HttpResponse
from django.template import Context, Template
from django.urls import include, path


def index(request):
    template = Template("")
    context = Context({'request': request, 'user': request.user})
    return HttpResponse(template.render(context))


urlpatterns = [
    path('django_ulogin/', include('django_ulogin.urls')),
    path('', index)
]
