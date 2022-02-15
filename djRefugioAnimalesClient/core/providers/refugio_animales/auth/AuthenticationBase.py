# coding=utf-8
from djRefugioAnimalesClient.core.exceptions.refugio_animales import DjRefugioAnimalesForbiddenError
from djRefugioAnimalesClient.core.providers.refugio_animales.classes import RefugioAnimalesBase


class AuthenticationBase(RefugioAnimalesBase):
    def __init__(self, *args, **kwargs):
        super(AuthenticationBase, self).__init__(*args, **kwargs)
        self._token_type = None
        self._access_token = None

    @property
    def auth_endpoint(self):
        """
        Endpoint base para autentificación de API Refugio de Animales
        """
        return "{endpoint}/api/auth".format(endpoint=self._base_endpoint)

    @property
    def fmt_access_token(self):
        """
        Formato del header 'Authorization'
        :return:
        """
        return '{token_type} {access_token}' \
               ''.format(token_type=self._token_type,
                         access_token=self._access_token)

    def get_access_token(self):
        """
        Intenta obtener un nuevo access_token para la consulta del api de refugio de animales

        Esta función se sobreescribe en las clases autentificación que eran de esta parent class
        """
        raise DjRefugioAnimalesForbiddenError
