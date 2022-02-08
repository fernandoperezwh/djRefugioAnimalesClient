# coding=utf-8
# django packages
from django.conf import settings
# third party packages
import requests
# local packages
from djRefugioAnimalesClient.core.exceptions.refugio_animales import (
    DjRefugioAnimalesServerConnectionError,
    DjRefugioAnimalesForbiddenError,
    DjRefugioAnimalesServerUnknowError,
    DjRefugioAnimalesNotFoundError,
    DjRefugioAnimalesBadRequestError,
)

CONNECTION_ERROR = (
    requests.ConnectTimeout,
    requests.ConnectionError,
)


# region Base classes
class RefugioAnimalesBase(object):
    """
    Clase base del API Refugio de Animales
    """
    def __init__(self, host=None, port=None):
        self._host = host or self.__default_server_host
        self._port = port or self.__default_server_port

    @property
    def __default_server_host(self):
        """
        Host del servidor default.

        Su valor se obtiene dependiendo del servidor definido en settings.DJREFUGIOANIMALES.default_server
        """
        api_settings = settings.DJREFUGIOANIMALES
        default_server = api_settings.get('default_server')
        return api_settings.get('servers').get(default_server).get('host')

    @property
    def __default_server_port(self):
        """
        Puerto default del servidor.

        Su valor se obtiene dependiendo del servidor definido en settings.DJREFUGIOANIMALES.default_server
        """
        api_settings = settings.DJREFUGIOANIMALES
        default_server = api_settings.get('default_server')
        return api_settings.get('servers').get(default_server).get('port')

    @property
    def _base_endpoint(self):
        """
        Endpoint base del API de Refugio de Animales
        """
        return "{host}:{port}".format(host=self._host, port=self._port)


class RefugioAnimalesAuthBase(RefugioAnimalesBase):
    def __init__(self, *args, **kwargs):
        super(RefugioAnimalesAuthBase, self).__init__(*args, **kwargs)
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
    # def login(self, username, password):
    #     """
    #     Realiza la autentificacion de un usuario admin de Django mediante username y password
    #
    #     :param username: User name perteneciente a usuario admin de django
    #     :param password: Password perteneciente a usuario admin de django
    #     :return: Regresa una tupla donde el primer elemento corresponde al access_token y el segundo al refresh_token
    #     """
    #     endpoint = "{endpoint}/".format(endpoint=self.auth_endpoint)
    #     try:
    #         response = requests.post(endpoint, data={
    #             'username': username,
    #             'password': password,
    #         })
    #         # Credenciales invalidas
    #         if response.status_code != 200:
    #             raise DjRefugioAnimalesAuthError
    #         response_data = response.json()
    #         # Inicio de sesión exitoso, retornamos los dos tokens
    #         self.access_token = response_data.get('access')
    #         self.refresh_token = response_data.get('refresh')
    #         return self.access_token, self.refresh_token
    #     except CONNECTION_ERROR:
    #         raise DjRefugioAnimalesServerConnectionError


class RefugioAnimalesMeta(type):
    """
    Singleton del wrapper de la API de Refugio de Animales
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(RefugioAnimalesMeta, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
# endregion


# region Authentication classes
class TokenAuthentication(RefugioAnimalesAuthBase):
    """
    Autentificacion por Basic Token
    """
    def __init__(self, username, password, *args, **kwargs):
        super(TokenAuthentication, self).__init__(*args, **kwargs)
        self.__username = username
        self.__password = password


class JSONWebTokenAuthentication(RefugioAnimalesAuthBase):
    """
    Autentificación por JSON Web Token
    """
    def __init__(self, username, password, *args, **kwargs):
        super(JSONWebTokenAuthentication, self).__init__(*args, **kwargs)
        self.__username = username
        self.__password = password


class OAuth2Authentication(RefugioAnimalesAuthBase):
    """
    Autentificación por OAuth
    """
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super(OAuth2Authentication, self).__init__(*args, **kwargs)
        self.__client_id = client_id
        self.__client_secret = client_secret
# endregion


class RefugioAnimalesProvider(RefugioAnimalesBase):
    """
    Wrapper de la API de Refugio de Animales
    """
    __metaclass__ = RefugioAnimalesMeta

    def __init__(self, auth=None, *args, **kwargs):
        super(RefugioAnimalesProvider, self).__init__(*args, **kwargs)
        self.__auth = auth or self.__default_auth_class

    @property
    def __default_auth_class(self):
        """
        Retorna el objeto para utilizar en la autentificación en base a la configuracion en
        'DJREFUGIOANIMALES.default_server'
        """
        api_settings = settings.DJREFUGIOANIMALES
        default_server = api_settings.get('default_server')

        if default_server == 'token_auth_server':
            server_cfg = api_settings.get('servers').get('token_auth_server')
            return TokenAuthentication(host=server_cfg.get('host'),
                                       port=server_cfg.get('port'),
                                       username=server_cfg.get('username'),
                                       password=server_cfg.get('password'))

        elif default_server == 'jwt_server':
            server_cfg = api_settings.get('servers').get('jwt_server')
            return JSONWebTokenAuthentication(host=server_cfg.get('host'),
                                              port=server_cfg.get('port'),
                                              username=server_cfg.get('username'),
                                              password=server_cfg.get('password'))

        elif default_server == 'oauth_server':
            server_cfg = api_settings.get('servers').get('oauth_server')
            return OAuth2Authentication(host=server_cfg.get('host'),
                                        port=server_cfg.get('port'),
                                        client_id=server_cfg.get('client_id'),
                                        client_secret=server_cfg.get('client_secret'))

    @property
    def api_endpoint(self):
        """
        Endpoint base de la API djRefugioAnimales
        """
        return "{endpoint}/api".format(endpoint=self._base_endpoint)

    @property
    def headers(self):
        """
        Diccionario con los headers enviados en cada request hacia la API
        """
        return {
            'Authorization': self.__auth.fmt_access_token,
        }

    def __get_resource(self, endpoint):
        """
        Funcion generica que consulta algun recurso.
        Si un error ocurre esta funcion generica maneja los errores
        :param endpoint: Endpoint del recurso
        :return:
        """
        try:
            response = requests.get(endpoint, headers=self.headers)
            if response.status_code == 404:
                raise DjRefugioAnimalesNotFoundError
            if response.status_code == 401:
                raise DjRefugioAnimalesForbiddenError
            return response.json()
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerConnectionError

    def __create_resource(self, endpoint, payload):
        """
        Funcion generica que crea nuevo registro en un recurso especifico.
        Si un error ocurre esta funcion generica maneja los errores
        :param endpoint: Endpoint del recurso
        :param payload: Campos del formulario para crear este nuevo registro
        :return:
        """
        try:
            response = requests.post(endpoint, data=payload, headers=self.headers)
            # Error por body incorrecto del request
            if response.status_code == 400:
                raise DjRefugioAnimalesBadRequestError
            # Error en permisos
            if response.status_code == 401:
                raise DjRefugioAnimalesForbiddenError
            # verifica algun error desconocido
            if response.status_code != 201:
                raise DjRefugioAnimalesServerUnknowError
            # En este punto pudo editar correctamente el registro
            return
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerConnectionError

    def __edit_resource(self, endpoint, payload):
        """
        Funcion generica que edita un registro de un recurso especifico.
        Si un error ocurre esta funcion generica maneja los errores
        :param endpoint: Endpoint del recurso
        :param payload: Campos del formulario para crear este nuevo registro
        :return:
        """
        try:
            response = requests.put(endpoint, data=payload, headers=self.headers)
            # Error por body incorrecto del request
            if response.status_code == 400:
                # NOTE: Podria especificarse los campos para dar información al cliene
                raise DjRefugioAnimalesBadRequestError
            # Error en permisos
            if response.status_code == 401:
                raise DjRefugioAnimalesForbiddenError
            # Elemento no encontrado
            if response.status_code == 404:
                raise DjRefugioAnimalesNotFoundError
            # verifica algun error desconocido
            if response.status_code != 200:
                raise DjRefugioAnimalesServerUnknowError
            # En este punto pudo editar correctamente el registro
            return
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerConnectionError

    def __delete_resource(self, endpoint):
        """
        Funcion generica que elimina un recurso en especifico.
        Si un error ocurre esta funcion generica maneja los errores
        :param endpoint: Endpoint del recurso
        :return:
        """
        try:
            response = requests.delete(endpoint, headers=self.headers)
            if response.status_code == 401:
                raise DjRefugioAnimalesForbiddenError
            if response.status_code == 404:
                raise DjRefugioAnimalesNotFoundError
            # verifica algun error desconocido
            if response.status_code != 204:
                raise DjRefugioAnimalesServerUnknowError
            # En este punto pudo eliminar correctamente el registro
            return
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerConnectionError

    def get_pet(self, pk):
        """
        Obtiene el registro de una mascota mediante su pk consultando la API de djRefugioAnimales
        :param pk: Id del registro de mascota a eliminar
        :return:
        """
        endpoint = "{endpoint}/mascota/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        return self.__get_resource(endpoint)

    def get_pets(self):
        """
        Obtiene la lista de mascotas consultando la API de djRefugioAnimales
        :return:
        """
        endpoint = "{endpoint}/mascota/".format(endpoint=self.api_endpoint)
        return self.__get_resource(endpoint)

    def create_pet(self, payload):
        """
        Crea un nuevo registro de la mascota consultando la API de djRefugioAnimales
        """
        endpoint = "{endpoint}/mascota/".format(endpoint=self.api_endpoint)
        self.__create_resource(endpoint, payload)

    def edit_pet(self, pk, payload):
        """
        Edita un registro de la mascota por su id consultando la API de djRefugioAnimales
        """
        endpoint = "{endpoint}/mascota/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        self.__edit_resource(endpoint, payload)

    def delete_pet(self, pk):
        """
        Elimina un registro de la mascota por su id consultando la API de djRefugioAnimales
        """
        endpoint = "{endpoint}/mascota/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        self.__delete_resource(endpoint)

    def get_vaccine(self, pk):
        """
        Obtiene el registro de una mascota mediante su pk consultando la API de djRefugioAnimales
        :param pk: Id del registro de mascota a eliminar
        :return:
        """
        endpoint = "{endpoint}/vacuna/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        return self.__get_resource(endpoint)

    def get_vaccines(self):
        """
        Obtiene la lista de vacunas consultando la API de djRefugioAnimales
        :return:
        """
        endpoint = "{endpoint}/vacuna/".format(endpoint=self.api_endpoint)
        return self.__get_resource(endpoint)

    def create_vaccine(self, payload):
        """
        Crea un nuevo registro de vacuna consultando la API de djRefugioAnimales
        """
        endpoint = "{endpoint}/vacuna/".format(endpoint=self.api_endpoint)
        self.__create_resource(endpoint, payload)

    def edit_vaccine(self, pk, payload):
        """
        Edita un registro de vacuna por su id consultando la API de djRefugioAnimales
        """
        endpoint = "{endpoint}/vacuna/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        self.__edit_resource(endpoint, payload)

    def delete_vaccine(self, pk):
        """
        Elimina un registro de vacuna por su id consultando la API de djRefugioAnimales
        """
        endpoint = "{endpoint}/vacuna/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        self.__delete_resource(endpoint)

    def get_owner(self, pk):
        """
        Obtiene el registro de un dueño/dueña mediante su pk consultando la API de djRefugioAnimales
        :param pk: Id del registro de mascota a eliminar
        :return:
        """
        endpoint = "{endpoint}/persona/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        return self.__get_resource(endpoint)

    def get_owners(self):
        """
        Obtiene la lista de dueños/dueñas de mascotas consultando la API de djRefugioAnimales
        :return:
        """
        endpoint = "{endpoint}/persona/".format(endpoint=self.api_endpoint)
        return self.__get_resource(endpoint)

    def create_owner(self, payload):
        """
        Crea un nuevo registro del dueño/dueña de mascota consultando la API de djRefugioAnimales
        """
        endpoint = "{endpoint}/persona/".format(endpoint=self.api_endpoint)
        self.__create_resource(endpoint, payload)

    def edit_owner(self, pk, payload):
        """
        Edita un registro del dueño/dueña de mascota por su id consultando la API de djRefugioAnimales
        """
        endpoint = "{endpoint}/persona/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        self.__edit_resource(endpoint, payload)

    def delete_owner(self, pk):
        """
        Elimina un registro del dueño/dueña de la mascota por su id consultando la API de djRefugioAnimales
        """
        endpoint = "{endpoint}/persona/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        self.__delete_resource(endpoint)
