from django.conf import settings


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
