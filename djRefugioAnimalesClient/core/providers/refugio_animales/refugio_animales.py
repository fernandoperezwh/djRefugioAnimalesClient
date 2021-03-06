# coding=utf-8
# django packages
from django.conf import settings
# third party packages
import requests
# local packages
from djRefugioAnimalesClient.core.exceptions.refugio_animales import (
    DjRefugioAnimalesServerConnectionError,
    DjRefugioAnimalesServerUnknowError,
    DjRefugioAnimalesNotFoundError,
    DjRefugioAnimalesBadRequestError,
    DjRefugioAnimalesAuthError,
)
from djRefugioAnimalesClient.core.providers.refugio_animales.auth import (
    TokenAuthentication,
    JSONWebTokenAuthentication,
    OAuth2Authentication,
)
from djRefugioAnimalesClient.core.providers.refugio_animales.classes import RefugioAnimalesBase

CONNECTION_ERROR = (
    requests.ConnectTimeout,
    requests.ConnectionError,
)


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


class RefugioAnimalesProvider(RefugioAnimalesBase):
    """
    Wrapper de la API de Refugio de Animales
    """
    __metaclass__ = RefugioAnimalesMeta

    def __init__(self, auth=None, *args, **kwargs):
        super(RefugioAnimalesProvider, self).__init__(*args, **kwargs)
        self.__auth = auth or self.__default_auth_class
        # Maximo numero de intentos de autentificacion seguidos
        self.__max_auth_attempts = 3

    @property
    def auth(self):
        """
        Instancia de la clase de autentificación
        """
        return self.__auth

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
                                       password=server_cfg.get('password'),
                                       access_token=server_cfg.get('access_token'))

        elif default_server == 'jwt_server':
            server_cfg = api_settings.get('servers').get('jwt_server')
            return JSONWebTokenAuthentication(host=server_cfg.get('host'),
                                              port=server_cfg.get('port'),
                                              username=server_cfg.get('username'),
                                              password=server_cfg.get('password'),
                                              access_token=server_cfg.get('access_token'),
                                              refresh_token=server_cfg.get('refresh_token'))

        elif default_server == 'oauth_server':
            server_cfg = api_settings.get('servers').get('oauth_server')
            return OAuth2Authentication(host=server_cfg.get('host'),
                                        port=server_cfg.get('port'),
                                        client_id=server_cfg.get('client_id'),
                                        client_secret=server_cfg.get('client_secret'),
                                        grant_type=server_cfg.get('grant_type'),
                                        username=server_cfg.get('username'),
                                        password=server_cfg.get('password'))

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

    def __get_resource(self, endpoint, auth_attempts=1):
        """
        Funcion generica que consulta algun recurso.
        Si un error ocurre esta funcion generica maneja los errores
        :param endpoint: Endpoint del recurso
        :return:
        """
        try:
            response = requests.get(endpoint, headers=self.headers)
            # No se encontro el recurso solicitado
            if response.status_code == 404:
                raise DjRefugioAnimalesNotFoundError
            # No tiene permisos para acceder al recurso
            if response.status_code in (401, 403):
                # Intentamos obtener un nuevo access_token. Si las credenciales en el settings son incorrectas entonces
                # levantara una excepcion.
                self.__auth.get_access_token()
                # Se verifica si se ha sobrepasado el numero de intentos
                if auth_attempts >= self.__max_auth_attempts:
                    raise DjRefugioAnimalesAuthError
                auth_attempts += 1
                # En este punto deberia poder obtenerse un nuevo access_token y podemos volver a intentar
                return self.__get_resource(endpoint, auth_attempts)
            return response.json()
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerConnectionError

    def __create_resource(self, endpoint, payload, auth_attempts=1):
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
            # No tiene permisos para acceder al recurso
            if response.status_code == 401:
                # Intentamos obtener un nuevo access_token. Si las credenciales en el settings son incorrectas entonces
                # levantara una excepcion.
                self.__auth.get_access_token()
                # Se verifica si se ha sobrepasado el numero de intentos
                if auth_attempts >= self.__max_auth_attempts:
                    raise DjRefugioAnimalesAuthError
                auth_attempts += 1
                # En este punto se pudo obtener un nuevo access_token y podemos volver a intentar
                return self.__create_resource(endpoint, payload, auth_attempts)
            # verifica algun error desconocido
            if response.status_code != 201:
                raise DjRefugioAnimalesServerUnknowError
            # En este punto pudo editar correctamente el registro
            return
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerConnectionError

    def __edit_resource(self, endpoint, payload, auth_attempts=1):
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
            # Forbidden error
            if response.status_code == 401:
                # Intentamos obtener un nuevo access_token. Si las credenciales en el settings son incorrectas entonces
                # levantara una excepcion.
                self.__auth.get_access_token()
                # Se verifica si se ha sobrepasado el numero de intentos
                if auth_attempts >= self.__max_auth_attempts:
                    raise DjRefugioAnimalesAuthError
                auth_attempts += 1
                # En este punto se pudo obtener un nuevo access_token y podemos volver a intentar
                return self.__edit_resource(endpoint, payload, auth_attempts)
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

    def __delete_resource(self, endpoint, auth_attempts=1):
        """
        Funcion generica que elimina un recurso en especifico.
        Si un error ocurre esta funcion generica maneja los errores
        :param endpoint: Endpoint del recurso
        :return:
        """
        try:
            response = requests.delete(endpoint, headers=self.headers)
            if response.status_code == 401:
                # Intentamos obtener un nuevo access_token. Si las credenciales en el settings son incorrectas entonces
                # levantara la excepcion
                self.__auth.get_access_token()
                # Se verifica si se ha sobrepasado el numero de intentos
                if auth_attempts >= self.__max_auth_attempts:
                    raise DjRefugioAnimalesAuthError
                auth_attempts += 1
                # En este punto se pudo obtener un nuevo access_token y podemos volver a intentar
                return self.__delete_resource(endpoint, auth_attempts)
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
