# -*- coding: utf-8 -*-
"""Modulo encargado de cargar (y recargar) la configuracion del servidor leyendo la misma desde server.conf"""

#Modulos externos
import platform, os
from configobj import ConfigObj, flatten_errors
from validate import Validator



if  platform.uname()[0] == 'Linux':
    archivo_de_configuracion='/home/mboscovich/proyectos/control_parental/cliente/cliente.conf'
    archivo_de_spec= '/home/mboscovich/proyectos/control_parental/cliente/conf/confspec.ini'
else:
    import _winreg, subprocess
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
    path_common = _winreg.QueryValueEx(key,'kerberus-common')[0]
    archivo_de_configuracion= path_common +'\cliente.conf'
    archivo_de_spec= path_common +'\confspec.ini'

config = ConfigObj(archivo_de_configuracion, configspec=archivo_de_spec)
validator = Validator()
result = config.validate(validator)

if result != True:
    print "Error al leer el archivo de configuración!!!"
    for (section_list, key, _) in flatten_errors(config, result):
        if key is not None:
            print 'El parámetro "%s" de la sección "%s" es incorrecto' % (key, ', '.join(section_list))
        else:
            print 'No se encontro la sección:%s ' % ', '.join(section_list)
else:
    #print "Se leyo la configuración del cliente correctamente"

    if  platform.uname()[0] == 'Linux':
        # Si estan vacio estos campos pongo default para linux
        if config['client']['path_db']:
            PATH_DB=config['client']['path_db']
        else:
            PATH_DB='/var/cache/kerberus/kerberus.db'
        if config['client']['log_filename']:
            LOG_FILENAME=config['client']['log_filename']
        else:
            LOG_FILENAME='/var/log/kerberus-cliente.log'
        if config['sync']['log_filename']:
            SYNC_LOG_FILENAME=config['sync']['log_filename']
        else:
            SYNC_LOG_FILENAME='/var/log/kerberus-syncd-cliente.log'
    else:
        # Si estan vacio estos campos pongo default para windows
        if config['client']['path_db']:
            PATH_DB=config['client']['path_db']
        else:
            LOG_FILENAME=config['client']['log_filename']
            PATH_DB=path_common +'\kerberus.db'
        if config['client']['log_filename']:
            LOG_FILENAME=config['client']['log_filename']
        else:
            LOG_FILENAME=path_common +'\kerberus-cliente.log'
        if config['sync']['log_filename']:
            SYNC_LOG_FILENAME=config['sync']['log_filename']
        else:
            SYNC_LOG_FILENAME=path_common +'\kerberus-syncd-cliente.log'
    #######
    # Asignaciones desde archivo de conf
    ########
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

    # sincronizador
    SYNC_SERVER_IP = config['sync']['ip']
    SYNC_SERVER_PORT = config['sync']['port']
    SYNC_LOG_SIZE_MB = config['sync']['log_size_mb']
    SYNC_LOG_CANT_ROTACIONES = config['sync']['log_cantidad_de_rotaciones']

    #Cliente
    CLIENT_LOG_FILENAME = config['client']['log_filename']
    BIND_ADDRESS = config['client']['bind_address']
    BIND_PORT = config['client']['bind_port']
    USAR_PROXY=config['client']['usar_proxy']
    PROXY_IP=config['client']['proxy_ip']
    PROXY_PORT=config['client']['proxy_port']
    LOG_SIZE_MB = config['client']['log_size_mb']
    LOG_CANT_ROTACIONES = config['client']['log_cantidad_de_rotaciones']

    # Server
    SERVER_IP=config['server']['ip']
    SERVER_PORT=config['server']['port']
    MAX_CACHE_URLS_ACEPTADAS=config['server']['max_urls_aceptadas_cacheadas']
    MAX_CACHE_URLS_DENEGADAS=config['server']['max_urls_denegadas_cacheadas']
