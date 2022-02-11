# coding=utf-8
from djRefugioAnimalesClient.core.providers.refugio_animales.auth import AuthenticationBase


class JSONWebTokenAuthentication(AuthenticationBase):
    """
    Autentificación por JSON Web Token
    """
    def __init__(self, username, password, *args, **kwargs):
        super(JSONWebTokenAuthentication, self).__init__(*args, **kwargs)
        self.__username = username
        self.__password = password
