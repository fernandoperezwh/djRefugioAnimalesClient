# coding=utf-8
import requests

from djRefugioAnimalesClient.core.exceptions.refugio_animales import (
    DjRefugioAnimalesAuthError,
    DjRefugioAnimalesServerConnectionError,
)
from djRefugioAnimalesClient.core.providers.refugio_animales.auth import AuthenticationBase

CONNECTION_ERROR = (
    requests.ConnectTimeout,
    requests.ConnectionError,
)


class JSONWebTokenAuthentication(AuthenticationBase):
    """
    Autentificación por JSON Web Token
    """
    def __init__(self, username, password, *args, **kwargs):
        super(JSONWebTokenAuthentication, self).__init__(*args, **kwargs)
        self.__username = username
        self.__password = password

    def __get_access_token_via_refresh_token(self):
        """
        Intenta obtener un nuevo access_token mediante el refresh_token
        """
        endpoint = '{endpoint}/refresh/'.format(endpoint=self.auth_endpoint)
        response = requests.post(endpoint, data={
            'refresh': self._refresh_token,
        })
        # Verificamos si ocurrió algún error, eso significara que las credenciales de acceso son incorrectas
        if response.status_code != 200:
            return
        return response.json()

    def __get_access_token_via_username_and_password(self):
        """
        Intenta obtener un nuevo access_token mediante el username y password del usuario
        """
        endpoint = '{endpoint}/'.format(endpoint=self.auth_endpoint)
        response = requests.post(endpoint, data={
            'username': self.__username,
            'password': self.__password,
        })
        # Verificamos si ocurrio algun error, eso significara que las credenciales de acceso son incorrectas
        if response.status_code != 200:
            return
        return response.json()

    def get_access_token(self):
        """
        Intenta obtener un nuevo access_token para la consulta del api de refugio de animales.

        Este tipo de autentificación soporta refresh_token
        """
        try:

            # Primero intentamos obtener un nuevo access_token mediante el refresh_token. De esta manera no requerimos
            # las credenciales del usuario para no comprometerlo aun más
            response = self.__get_access_token_via_refresh_token()
            # En caso de que el refresh_token no funciono, entonces recurrimos en enviar las credenciales del usuario
            # para obtener un nuevo access_token
            if not response:
                response = self.__get_access_token_via_username_and_password()
            # Si no funciono ninguno de las dos alternativas entonces el username y password son incorrectos y
            # la excepción
            if not response:
                raise DjRefugioAnimalesAuthError
            # En este punto el token se pudo obtener correctamente asi que podemos actualizar su valor
            self._token_type = 'Bearer'
            self._access_token = response.get('access')
            self._refresh_token = response.get('refresh')
        except CONNECTION_ERROR:
            # Error estableciendo conexión con el servidor
            raise DjRefugioAnimalesServerConnectionError
