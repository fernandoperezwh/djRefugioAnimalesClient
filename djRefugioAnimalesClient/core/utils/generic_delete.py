# django packages
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
# local packages
from djRefugioAnimalesClient.core.exceptions.refugio_animales import DjRefugioAnimalesServerUnknowError


def generic_api_delete(request, delete_function, instance, redirect, custom_messages={}):
    """
    Funcion generica para eliminar registros mediante llama a api

    :param request: Django Request Object
    :param delete_function: Metodo del provider RefugioAnimales a llamar para eliminar el registro
    :param instance: Datos del registro
    :param redirect: url name a redireccionar
    :param custom_messages: Diccionario de imagenes personalizados del error
    :return:
    """
    DEFAULT_SUCCESS_MESSAGE = 'Se elimino el registro correctamente.'
    DEFAULT_UNKNOW_ERROR_MESSAGE = 'Ha ocurrido un error desconocido'

    if request.method == 'POST':
        try:
            # Se ejecuta el metodo para eliminar algun registro de djRefugioAnimales
            delete_function(instance.get('id'))
            messages.success(request, custom_messages.get('success') or DEFAULT_SUCCESS_MESSAGE)
            return HttpResponseRedirect(redirect)
        except DjRefugioAnimalesServerUnknowError:
            messages.error(request, custom_messages.get('unknow_error', DEFAULT_UNKNOW_ERROR_MESSAGE))
            return HttpResponseRedirect(redirect)

    return render(request, 'generic_delete.html', {
        'object': instance,
        'redirect': redirect
    })