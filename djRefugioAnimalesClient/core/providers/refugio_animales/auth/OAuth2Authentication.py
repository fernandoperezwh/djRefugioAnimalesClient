# coding=utf-8
import base64
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


class OAuth2Authentication(AuthenticationBase):
    """
    Autentificación por OAuth
    """
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super(OAuth2Authentication, self).__init__(*args, **kwargs)
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__expires_in = None
        self.__scope = None

    @property
    def __credential(self):
        """
        Se realiza encode del cliente_id y cliente_secret para convertirlo en HTTP base authentication encoded in base64

        Para mas información consultar en la documentacion
        https://django-oauth-toolkit.readthedocs.io/en/latest/getting_started.html#client-credential

        :return: HTTP base authentication encoded in base64
        """
        credential = "{client_id}:{client_secret}".format(client_id=self.__client_id,
                                                          client_secret=self.__client_secret)
        return base64.b64encode(credential.encode("utf-8"))

    def __get_access_token_via_client_id_and_client_secret(self):
        """
        Intenta obtener un nuevo access_token mediante el client_id y client_secret del usuario
        """
        endpoint = '{endpoint}/token/'.format(endpoint=self.auth_endpoint)
        response = requests.post(endpoint, data={'grant_type': 'client_credentials'}, headers={
            'Authorization': 'Basic {credential}'.format(credential=self.__credential),
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
        })
        # Verificamos si ocurrió algún error, eso significara que las credenciales de acceso son incorrectas
        if response.status_code != 200:
            return
        return response.json()

    def get_access_token(self):
        """
        Intenta obtener un nuevo access_token para la consulta del api de refugio de animales.
        """
        try:
            response = self.__get_access_token_via_client_id_and_client_secret()
            # Si no regreso ningún valor entonces el username y password son incorrectos y levantamos la excepción
            if not response:
                raise DjRefugioAnimalesAuthError
            # En este punto el token se pudo obtener correctamente asi que podemos actualizar su valor
            self._token_type = response.get('token_type')
            self._access_token = response.get('access_token')
            self._refresh_token = None
            self.__expires_in = None
            self.__scope = None
        except CONNECTION_ERROR:
            # Error estableciendo conexión con el servidor
            raise DjRefugioAnimalesServerConnectionError
