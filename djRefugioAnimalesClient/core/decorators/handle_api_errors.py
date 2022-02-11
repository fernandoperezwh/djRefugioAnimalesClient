# coding=utf-8
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from djRefugioAnimalesClient.core.exceptions.refugio_animales import DjRefugioAnimalesForbiddenError, \
    DjRefugioAnimalesRefreshTokenError, DjRefugioAnimalesServerConnectionError


def handle_api_errors(view_func):
    def wrap(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except (DjRefugioAnimalesForbiddenError, DjRefugioAnimalesRefreshTokenError):
            return HttpResponseRedirect(reverse('forbidden_error'))
        except DjRefugioAnimalesServerConnectionError:
            messages.error(request, 'Un error ha ocurrido intentando conectar con el servidor')
            return HttpResponseRedirect(reverse('home'))
    return wrap
