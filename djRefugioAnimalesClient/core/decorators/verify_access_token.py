# coding=utf-8
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from djRefugioAnimalesClient.core.exceptions.refugio_animales import DjRefugioAnimalesForbiddenError, \
    DjRefugioAnimalesRefreshTokenError, DjRefugioAnimalesServerConnectionError, DjRefugioAnimalesServerUnknowError
from djRefugioAnimalesClient.core.providers import RefugioAnimalesProvider


def verify_access_token(view_func):
    """
    Verifica que el access token se encuentre en las cookies del request, posteriormente se consulta un endpoint del api
    djRefugioAnimales para verificar el estado del token.

    Si el token no es valido se redirige a la vista de login para que introduzca de nuevo las credenciales
    :param view_func:
    :return:
    """
    def wrap(request, *args, **kwargs):
        REDIRECT_URL = reverse('forbidden_error')

        # Se valida que el access token se encuentre presente en las cookies del request
        # if not request.COOKIES.get('access_token'):
        #     try:
        #         if request.COOKIES.get('refresh_token'):
        #             # TODO: Si hay un refresh_token podemos intentar actualizar
        #             pass
        #         # TODO: obtener uno nuevo token
        #         pass
        #     except DjRefugioAnimalesForbiddenError:
        #         # Las credenciales para la autentificación son incorrectas
        #         return HttpResponseRedirect(REDIRECT_URL)

        # Se valida que el token sea correcto haciendo una peticion a la API
        api = RefugioAnimalesProvider()
        try:
            access_token, refresh_token = api.auth.verify_access_token(refresh=True)
            # Pasamos en la view la instancia actualizada del cliente RefugioAnimales
            kwargs['api_tokens'] = {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        except (DjRefugioAnimalesForbiddenError, DjRefugioAnimalesRefreshTokenError):
            return HttpResponseRedirect(REDIRECT_URL)
        except DjRefugioAnimalesServerConnectionError:
            messages.error(request, 'No ha sido posible establecer conexión con el servidor.')
            return HttpResponseRedirect('home')

        # El access token esta presente en la peticion y no presenta ningun error
        return view_func(request, *args, **kwargs)
    return wrap
