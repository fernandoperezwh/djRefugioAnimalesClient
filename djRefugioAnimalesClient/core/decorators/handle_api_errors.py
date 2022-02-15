# coding=utf-8
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from djRefugioAnimalesClient.core.exceptions.refugio_animales import (
    DjRefugioAnimalesForbiddenError,
    DjRefugioAnimalesRefreshTokenError,
    DjRefugioAnimalesServerConnectionError,
    DjRefugioAnimalesOAuth2_0UserActionRequired,
)


def handle_api_errors(view_func):
    def wrap(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except (DjRefugioAnimalesForbiddenError, DjRefugioAnimalesRefreshTokenError):
            return HttpResponseRedirect(reverse('forbidden_error'))
        except DjRefugioAnimalesServerConnectionError:
            messages.error(request, 'Un error ha ocurrido intentando conectar con el servidor')
            return HttpResponseRedirect(reverse('home'))
        except DjRefugioAnimalesOAuth2_0UserActionRequired as err:
            # Cuando llega esta excepcion redireccionamos al servidor de OAuth2.0 de la API de refugio de animales para
            # hacer el flow de Authorization code
            return HttpResponseRedirect(err.redirect_url)
    return wrap
