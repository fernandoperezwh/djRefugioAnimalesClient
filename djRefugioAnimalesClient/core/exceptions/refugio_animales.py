# coding=utf-8
class DjRefugioAnimalesServerUnknowError(Exception):
    def __str__(self):
        return 'Ha ocurrido un error desconocido'


class DjRefugioAnimalesServerConnectionError(Exception):
    def __str__(self):
        return 'Un error ha ocurrido intentando conectar con el servidor'


class DjRefugioAnimalesAuthError(Exception):
    def __str__(self):
        return 'Las credenciales proporcionadas son incorrectas'


class DjRefugioAnimalesRefreshTokenError(Exception):
    def __str__(self):
        return 'El refresh_token no esta definido o es incorrecto'


class DjRefugioAnimalesForbiddenError(Exception):
    def __str__(self):
        return 'No cuentas con el permiso para acceder al recurso'


class DjRefugioAnimalesNotFoundError(Exception):
    def __str__(self):
        return 'No se encontro el recurso'


class DjRefugioAnimalesBadRequestError(Exception):
    def __str__(self):
        return 'Verifique los datos de su petición, hay campos incorrectos'


class DjRefugioAnimalesOAuth2_0UnknownGrantType(Exception):
    def __init__(self, grant_type):
        self.__grant_type = grant_type

    def __str__(self):
        return '{grant_type} es un grant type desconocido.' \
               ''.format(grant_type=self.__grant_type)


class DjRefugioAnimalesOAuth2_0UserActionRequired(Exception):
    def __init__(self, response_type, auth_endpoint, client_id):
        self.__response_type = response_type
        self.__auth_endpoint = auth_endpoint
        self.__client_id = client_id

    @property
    def redirect_url(self):
        """
        Construye la url para realizar el flujo de OAuth Authorization Code
        """
        oauth_endpoint = '{endpoint}/authorize/?response_type={response_type}&client_id={client_id}'
        return oauth_endpoint.format(
            endpoint=self.__auth_endpoint,
            response_type=self.__response_type,
            client_id=self.__client_id
        )

    def __str__(self):
        return 'Se requiere acción del usuario para la autorización'
