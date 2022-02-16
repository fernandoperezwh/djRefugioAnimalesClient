# coding=utf-8
# django packages
from django.contrib import messages
from django.http import HttpResponseRedirect

# local packages
from django.shortcuts import render
from django.urls import reverse

from djRefugioAnimalesClient.core.providers import RefugioAnimalesProvider


def oauth_callback(request):
    """
    Pagina de redireccionamiento de OAuth 2.0
    """
    #
    if request.GET:
        # Obtenemos la instancia del singleton de RefugioAnimalesProvider y mandamos a llamar el metodo
        # 'handle_callback'. Este metodo se encargara de ver que parametros en la url tomar para continuar con el flujo
        # de 'Authorization Code' o 'Implicit'
        api = RefugioAnimalesProvider()
        api.auth.handle_callback(request.GET)
        # Posteriormente, ya podemos redirigir al home
        messages.success(request, 'Se ha completado el flujo OAuth 2.0')
        return HttpResponseRedirect(reverse('home'))

    # Cuando no hay parametros en la url entonces es el flujo "Implicit Grant".
    # Esto lo identificamos porque la url viene con el simbolo "#" y no como en el flujo "Authorizacion Code Grant" que
    # tiene el simbolo "?".
    #
    # Ejemplo
    # Authorizacion Code Grant --> /oauth/callback#?code=uVqLxiHDKIirldDZQfSnDsmYW1Abj2
    # Implicit Grant --> /oauth/callback#access_token=Mg4SkFuTYLeRq4QcUNgvaymHk1INtq&token_type=Bearer&state=&expires_in=36000&scope=read+write
    #
    # Por lo tanto desde javascript obtenemos los valores en el hash y redireccionamos a esta misma view pero ahora si
    # pasamos los datos en la url para que puede entrar a la condicional de arriba
    return render(request, 'oauth_callback.html', {})
