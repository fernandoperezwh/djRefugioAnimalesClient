# coding=utf-8
# python packages
import requests
#django packages
from django.conf import settings
# local packages
from djRefugioAnimalesClient.core.exceptions.refugio_animales import (
    DjRefugioAnimalesAuthError,
    DjRefugioAnimalesServerConnectionError,
)
from djRefugioAnimalesClient.core.providers.refugio_animales.auth import AuthenticationBase

CONNECTION_ERROR = (
    requests.ConnectTimeout,
    requests.ConnectionError,
)


class TokenAuthentication(AuthenticationBase):
    """
    Autentificacion por Basic Token
    """
    def __init__(self, username, password, access_token=None, *args, **kwargs):
        super(TokenAuthentication, self).__init__(*args, **kwargs)
        self.__username = username
        self.__password = password
        self._token_type = 'Token'
        self._access_token = access_token

    def __get_access_token_via_username_and_password(self):
        """
        Intenta obtener un nuevo access_token mediante el username y password del usuario
        """
        endpoint = '{endpoint}/'.format(endpoint=self.auth_endpoint)
        response = requests.post(endpoint, data={
            'username': self.__username,
            'password': self.__password,
        })
        # Verificamos si ocurrió algún error, eso significara que las credenciales de acceso son incorrectas
        if response.status_code != 200:
            return
        return response.json()

    def get_access_token(self):
        config = settings.DJREFUGIOANIMALES.get('servers').get('token_auth_server')
        # Si no esta configurado el intentar autentificar cuando el token falla entonces levantamos directamente la
        # exception
        if self._access_token and not config.get('try_auth_in_token_fail'):
            raise DjRefugioAnimalesAuthError

        # Intentamos realizar la autentificacion por el username y password
        try:
            response = self.__get_access_token_via_username_and_password()
            # Si no regreso ningún valor entonces el username y password son incorrectos y levantamos la excepción
            if not response:
                raise DjRefugioAnimalesAuthError
            # En este punto el token se pudo obtener correctamente asi que podemos actualizar su valor
            self._token_type = response.get('token_type')
            self._access_token = response.get('access_token')

        except CONNECTION_ERROR:
            # Error estableciendo conexión con el servidor
            raise DjRefugioAnimalesServerConnectionError
