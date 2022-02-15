# coding=utf-8
# django packages
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

# local packages
from django.urls import reverse

from djRefugioAnimalesClient.core.providers import RefugioAnimalesProvider


def oauth_callback(request):
    """
    Pagina de redireccionamiento de OAuth 2.0
    """
    # Obtenemos el code desde el GET y lo asignamos al singleton para que pueda continuar con la authentificacion
    oauth_code = request.GET.get('code')
    api = RefugioAnimalesProvider()
    api.auth.set_code(oauth_code)
    # Estableciendo el code ahora podra realizar la autentificación para obtener acceso a los recursos protegidos
    messages.success(request, 'Se ha completado el flujo Authorization Code de oauth')
    return HttpResponseRedirect(reverse('home'))
