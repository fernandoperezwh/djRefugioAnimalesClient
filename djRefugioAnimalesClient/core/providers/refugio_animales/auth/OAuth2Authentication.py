# coding=utf-8
from djRefugioAnimalesClient.core.providers.refugio_animales.auth import AuthenticationBase


class OAuth2Authentication(AuthenticationBase):
    """
    Autentificación por OAuth
    """
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super(OAuth2Authentication, self).__init__(*args, **kwargs)
        self.__client_id = client_id
        self.__client_secret = client_secret
