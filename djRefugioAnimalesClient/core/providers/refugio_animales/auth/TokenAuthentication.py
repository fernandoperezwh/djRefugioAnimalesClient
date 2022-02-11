# coding=utf-8
from djRefugioAnimalesClient.core.providers.refugio_animales.auth import AuthenticationBase


class TokenAuthentication(AuthenticationBase):
    """
    Autentificacion por Basic Token
    """
    def __init__(self, username, password, *args, **kwargs):
        super(TokenAuthentication, self).__init__(*args, **kwargs)
        self.__username = username
        self.__password = password

    def authenticate(self):
        """
        Realiza la autentificacion de un usuario admin de Django mediante username y password

        :param username: User name perteneciente a usuario admin de django
        :param password: Password perteneciente a usuario admin de django
        :return: Regresa una tupla donde el primer elemento corresponde al access_token y el segundo al refresh_token
        """
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
