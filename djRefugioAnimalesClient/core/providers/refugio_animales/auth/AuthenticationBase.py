# coding=utf-8
from djRefugioAnimalesClient.core.providers.refugio_animales.classes import RefugioAnimalesBase


class AuthenticationBase(RefugioAnimalesBase):
    def __init__(self, *args, **kwargs):
        super(AuthenticationBase, self).__init__(*args, **kwargs)
        self._token_type = None
        self._access_token = None
        self._refresh_token = None

    @property
    def auth_endpoint(self):
        """
        Endpoint base para autentificación de API Refugio de Animales
        """
        return "{endpoint}/api/auth".format(endpoint=self._base_endpoint)

    @property
    def token_type(self):
        """
        Token type para API de Refugio de animales
        """
        return self._token_type

    @property
    def access_token(self):
        """
        Access token para API de Refugio de animales
        """
        return self._access_token

    @property
    def refresh_token(self):
        """
        Refresh token para API de Refugio de animales
        """
        return self._refresh_token

    @property
    def fmt_access_token(self):
        """
        Formato del header 'Authorization'
        :return:
        """
        return '{token_type} {access_token}' \
               ''.format(token_type=self._token_type,
                         access_token=self._access_token)

    # def verify_access_token(self, refresh=False):
    #     """
    #     Verifica el estado del access_token consultando a la API. Si el token no es valido se levantara un raise del
    #     tipo DjRefugioAnimalesForbiddenError indicando que el token es invalido.
    #
    #     En caso contrario el metodo terminara con exito sin retornar ningun valor.
    #
    #     :param refresh: Indica si consulta el servicio para hacer refresh del access_token y obtener uno valido
    #     :return: Regresa una tupla donde el primer elemento corresponde al access_token y el segundo al refresh_token
    #     """
    #     endpoint = "{endpoint}/verify/".format(endpoint=self.auth_endpoint)
    #     if not self.access_token:
    #         raise DjRefugioAnimalesForbiddenError
    #     try:
    #         response = requests.post(endpoint, data={
    #             'token': self.access_token
    #         })
    #         # Comprueba el status code de la respuesta para validar si el access_token es incorrecto
    #         if response.status_code == 401:
    #             # Si no esta habilitado el refresh_token entonces levantamos directamente la excepcion
    #             if not refresh:
    #                 raise DjRefugioAnimalesForbiddenError
    #             # La bandera de refresh esta activa. Por lo tanto intentamos hacer el refresh
    #             self.refresh_access_token()
    #         return self.access_token, self.refresh_token
    #     except CONNECTION_ERROR:
    #         raise DjRefugioAnimalesServerConnectionError
    #
    # def refresh_access_token(self):
    #     """
    #     Realiza el refresh del access_token.
    #
    #     :return: Regresa una tupla donde el primer elemento corresponde al access_token y el segundo al refresh_token
    #     """
    #     endpoint = "{endpoint}/refresh/".format(endpoint=self.auth_endpoint)
    #     # Se comprueba si el refresh_token se encuentra definido
    #     if not self.refresh_token:
    #         raise DjRefugioAnimalesRefreshTokenError
    #     # Consultamos el recurso para refrescar el access_token
    #     try:
    #         response = requests.post(endpoint, data={
    #             'refresh': self.refresh_token
    #         })
    #         # El refresh_token es incorrecto
    #         if response.status_code == 401:
    #             raise DjRefugioAnimalesRefreshTokenError
    #         # En este punto se pudo obtener un nuevo access_token
    #         response_data = response.json()
    #         self.access_token = response_data.get('access')
    #         self.refresh_token = response_data.get('refresh')
    #         return self.access_token, self.refresh_token
    #     except CONNECTION_ERROR:
    #         raise DjRefugioAnimalesServerConnectionError
    #
