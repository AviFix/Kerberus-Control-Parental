# -*- coding: utf-8 -*-

"""Modulo encargado de cargar (y recargar) la configuracion del servidor
leyendo la misma desde server.conf"""

#Modulos externos
from configobj import ConfigObj


#Excepciones
class serverConfigError(Exception):
    pass


# Clase
class serverConfig:
    def __init__(self, archivo_de_configuracion='/srv/kerberus/server.conf'):
        config = ConfigObj(archivo_de_configuracion)
        # SERVERID!!!!
        self.serverID = config['server']['server_id']
        # Log
        self.log_filename = config['log']['log_filename']
        self.log_size = config['log']['log_size']
        self.log_rotaciones = config['log']['log_rotaciones']

        # Caches
        self.cache_max_urls_aceptadas = \
            config['caches']['cache_max_urls_aceptadas']
        self.cache_max_urls_denegadas = \
            config['caches']['cache_max_urls_denegadas']
        self.cache_max_dominios_aceptados = \
            config['caches']['cache_max_dominios_aceptados']
        self.cache_max_dominios_denegados = \
            config['caches']['cache_max_dominios_denegados']
        self.cache_denegadas_duracion = \
            float(config['caches']['cache_denegadas_duracion'])
        self.cache_aceptadas_duracion = \
            float(config['caches']['cache_aceptadas_duracion'])

        # db
        self.db_host = config['db']['db_host']
        self.db_user = config['db']['db_user']
        self.db_password = config['db']['db_password']
        self.db_name = config['db']['db_name']

        # Server
        self.server_path = config['server']['server_path']
        self.log_daemon = config['server']['log_daemon']
        self.daemon_stderr_file = config['server']['daemon_stderr_file']
        self.daemon_stdout_file = config['server']['daemon_stdout_file']
        self.bind_address = config['server']['bind_address']
        self.bind_port = int(config['server']['bind_port'])
        self.dansguardian_ip = config['server']['dansguardian_ip']
        self.dansguardian_port = config['server']['dansguardian_port']

        # Constantes de debug
        self.debug_cacheados_aceptados = \
            config['debug']['debug_cacheados_aceptados']
        self.debug_cacheados_denegados = \
            config['debug']['debug_cacheados_denegados']
        self.debug_aceptados = config['debug']['debug_aceptados']
        self.debug_denegados = config['debug']['debug_denegados']
        self.debug_conversiones_https = \
            config['debug']['debug_conversiones_https']
        self.debug_urllib2_except = config['debug']['debug_urllib2_except']
        self.debug_borrado_urls_viejas = \
            config['debug']['debug_cacheados_aceptados']
        self.debug_server_reload = config['debug']['debug_server_reload']


class sincronizadorConfig:
    def __init__(self,
                archivo_de_configuracion='/srv/kerberus/sincronizador.conf'
                ):
        config = ConfigObj(archivo_de_configuracion)

        # Log
        self.log_filename = config['log']['log_filename']
        self.log_size = config['log']['log_size']
        self.log_rotaciones = config['log']['log_rotaciones']
        self.log_level = config['log']['log_level']
        # db
        self.db_host = config['db']['db_host']
        self.db_user = config['db']['db_user']
        self.db_password = config['db']['db_password']
        self.db_name = config['db']['db_name']

        # Sincronizador
        self.path = config['sincronizador']['path']
        self.periodo_chequeo = float(config['sincronizador']['periodo_chequeo'])
        self.log_daemon = config['sincronizador']['log_daemon']
        self.daemon_stderr_file = config['sincronizador']['daemon_stderr_file']
        self.daemon_stdout_file = config['sincronizador']['daemon_stdout_file']
        self.bind_address = config['sincronizador']['bind_address']
        self.bind_port = int(config['sincronizador']['bind_port'])

        # Debug
        self.debug_server_reload = config['debug']['debug_server_reload']
