# coding=utf-8
import base64
import requests

from djRefugioAnimalesClient.core.exceptions.refugio_animales import (
    DjRefugioAnimalesAuthError,
    DjRefugioAnimalesServerConnectionError,
    DjRefugioAnimalesOAuth2_0UserActionRequired,
    DjRefugioAnimalesOAuth2_0UnknownGrantType,
)
from djRefugioAnimalesClient.core.providers.refugio_animales.auth import AuthenticationBase

CONNECTION_ERROR = (
    requests.ConnectTimeout,
    requests.ConnectionError,
)


class OAuthGranTypes:
    """
    Contiene los grant types de OAuth 2.0
    """
    AUTHORIZATION_CODE = 'authorization_code'
    IMPLICIT = 'implicit'
    RESOURCE_OWNER_PASSWORD = 'resource_owner_password'
    CLIENT_CREDENTIALS = 'client_credentials'

    LIST_GRANT_TYPES = (
        AUTHORIZATION_CODE,
        IMPLICIT,
        RESOURCE_OWNER_PASSWORD,
        CLIENT_CREDENTIALS,
    )


class OAuth2Authentication(AuthenticationBase):
    """
    Autentificación por OAuth
    """
    def __init__(self, client_id, client_secret, grant_type=None, *args, **kwargs):
        super(OAuth2Authentication, self).__init__(*args, **kwargs)
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__expires_in = None
        self.__scope = None

        # Contiene el codigo para seguir el Authorization Code Grant Type
        self.__code = None
        # Se verifica que el grant_type de entrada sea valido
        grant_type = grant_type or OAuthGranTypes.CLIENT_CREDENTIALS
        if grant_type in OAuthGranTypes.LIST_GRANT_TYPES:
            self.__grant_type = grant_type
        else:
            raise DjRefugioAnimalesOAuth2_0UnknownGrantType(grant_type)

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

    def set_code(self, code):
        """
        Establece el code para seguir el Authentication Code Grant Type
        """
        self.__code = code

    def __get_access_token_via_client_credentials(self):
        """
        Intenta obtener un nuevo access_token siguiendo el Client Credentials Grant Type
        """
        endpoint = '{endpoint}/token/'.format(endpoint=self.auth_endpoint)
        response = requests.post(endpoint, data={'grant_type': OAuthGranTypes.CLIENT_CREDENTIALS}, headers={
            'Authorization': 'Basic {credential}'.format(credential=self.__credential),
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
        })
        # Verificamos si ocurrió algún error, eso significara que las credenciales de acceso son incorrectas
        if response.status_code != 200:
            return
        return response.json()

    def __get_access_token_via_authorization_code(self):
        """
        Intenta obtener un nuevo access_token siguiendo el Authorization Code Grant Type
        """
        # Se verifica si ya contamos con el code para seguir este grant type. Si aun no contamos con uno entonces
        # levantamos la excepcion ya que dependemos de que el resource owner de la autorizacion desde el servidor que
        # tiene la API
        if not self.__code:
            raise DjRefugioAnimalesOAuth2_0UserActionRequired(self.auth_endpoint, self.__client_id)

        # El resource owner ya nos autorizo y tenemos el code para obtener el access_token
        # noinspection DuplicatedCode
        endpoint = '{endpoint}/token/'.format(endpoint=self.auth_endpoint)
        response = requests.post(endpoint, data={
            'grant_type': OAuthGranTypes.AUTHORIZATION_CODE,
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'code': self.__code,
        }, headers={
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded',
        })
        # Verificamos si ocurrió algún error, eso significara que las credenciales de acceso son incorrectas
        if response.status_code != 200:
            return
        return response.json()

    def __get_access_token(self):
        """
        Aplica el flujo de OAuth 2.0 conforme a la configuración del proyecto
        """
        response = None
        if self.__grant_type == OAuthGranTypes.CLIENT_CREDENTIALS:
            # Client Credentials Grant Type
            response = self.__get_access_token_via_client_credentials()
        elif self.__grant_type == OAuthGranTypes.AUTHORIZATION_CODE:
            # Authorization Code Grant Type
            response = self.__get_access_token_via_authorization_code()
        elif self.__grant_type == OAuthGranTypes.RESOURCE_OWNER_PASSWORD:
            # Resouce owner password
            pass
        elif self.__grant_type == OAuthGranTypes.IMPLICIT:
            # Implicit Grant Type
            pass
        return response

    def get_access_token(self):
        """
        Intenta obtener un nuevo access_token para la consulta del api de refugio de animales.
        """
        try:
            response = self.__get_access_token()
            # Si no regreso ningún valor entonces el username y password son incorrectos y levantamos la excepción
            if not response:
                raise DjRefugioAnimalesAuthError
            # En este punto el token se pudo obtener correctamente asi que podemos actualizar su valor
            self._token_type = response.get('token_type')
            self._access_token = response.get('access_token')
            self.__expires_in = None
            self.__scope = None
        except CONNECTION_ERROR:
            # Error estableciendo conexión con el servidor
            raise DjRefugioAnimalesServerConnectionError
