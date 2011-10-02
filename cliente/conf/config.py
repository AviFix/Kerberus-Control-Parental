# -*- coding: utf-8 -*-
"""Modulo encargado de cargar (y recargar) la configuracion del servidor leyendo la misma desde server.conf"""

#Modulos externos
import platform, os
from configobj import ConfigObj

if  platform.uname()[0] == 'Linux':
    PATH_DB='/var/cache/kerberus/kerberus.db'
    LOG_FILENAME='/var/log/kerberus-cliente.log'
    archivo_de_configuracion='/home/mboscovich/proyectos/control_parental/cliente/cliente.conf'
else:
    import _winreg, subprocess
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
    path_common = _winreg.QueryValueEx(key,'kerberus-common')[0]
    PATH_DB= path_common +'\kerberus.db'
    LOG_FILENAME= path_common +'\kerberus-cliente.log'
    archivo_de_configuracion= path_common +'\cliente.conf'

config = ConfigObj(archivo_de_configuracion)

# Constantes de debug
DEBUG_EXTENSIONES=config['debug']['debug_extensiones']
DEBUG_DOM_PERM=config['debug']['debug_dominios_permitidos']
DEBUG_DOM_DENG=config['debug']['debug_deminios_denegados']
DEBUG_DOM_PUB_PERM=config['debug']['debug_dominios_publicamente_permitidos']
DEBUG_DOM_PUB_DENG=config['debug']['debug_dominios_publicamente_denegados']
DEBUG_CACHEADA_PERM=config['debug']['debug_cacheada_permitida']
DEBUG_CACHEADA_DENG=config['debug']['debug_cacheada_denegada']
DEBUG_VALIDA_REM=config['debug']['debug_valida_remotamente']
DEBUG_NO_VALIDA_REM=config['debug']['debug_denegada_remotamente']
DEBUG_TIEMPO_REMOTO=config['debug']['debug_tiempo_validacion_remota']
DEBUG_IS_ADMIN=config['debug']['debug_peticiones_admin']
LOG_TIEMPOS_MAYORES_A=config['debug']['debug_tiempos_mayores_a']

# Log
LOG_SIZE_MB =config['log']['log_size_mb']
LOG_CANT_ROTACIONES =config['log']['cantidad_de_rotaciones']

#Cliente
BIND_ADDRESS = config['client']['bind_address']
BIND_PORT = config['client']['bind_port']
USAR_PROXY=config['client']['usar_proxy']
PROXY_IP=config['client']['proxy_ip']
PROXY_PORT=config['client']['proxy_port']

# Server
SERVER_IP=config['server']['server_ip']
SERVER_PORT=config['server']['port']
SERVER_SINC_PORT=config['server']['sinc_port']
MAX_CACHE_URLS_ACEPTADAS=config['server']['max_urls_aceptadas_cacheadas']
MAX_CACHE_URLS_DENEGADAS=config['server']['max_urls_denegadas_cacheadas']


