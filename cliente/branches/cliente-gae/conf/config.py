# -*- coding: utf-8 -*-
"""Modulo encargado de cargar (y recargar) la configuracion del servidor
leyendo la misma desde server.conf"""

#Modulos externos
import platform
#import os
import sys
from configobj import ConfigObj, flatten_errors
from validate import Validator
import logging
import logging.handlers

sys.path.append('../')

# FIXME: Deberia estar en loguear en vez de aca
def logSetup(logfile, loglevel=5, logsize=1, cant_rotaciones=1,
                cabecera_log=""):
    logger = logging.getLogger(cabecera_log)
    logger.setLevel(loglevel * 10)
    handler = logging.handlers.RotatingFileHandler(
            logfile,
            maxBytes=(logsize * (1 << 20)),
            backupCount=cant_rotaciones)
    fmt = logging.Formatter(
                                "[%(asctime)-12s.%(msecs)03d] "
                                "%(levelname)-4s {%(name)s %(threadName)s}"
                                " %(message)s",
                                "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger
####

#FIXME: Esto se deberia sacar de otro lado
VERSION = 1.1
#
# Poner en false esta variable a la hora de pasar a produccion
ENTORNO_DE_DESARROLLO = True

if platform.uname()[0] == 'Linux':
    PLATAFORMA = 'Linux'
else:
    PLATAFORMA = 'Windows'

if ENTORNO_DE_DESARROLLO:
    PATH_COMMON = '/home/mboscovich/proyectos/control_parental/cliente/branches/cliente-gae/entorno_prueba'
    archivo_de_configuracion = PATH_COMMON + '/cliente.conf'
    archivo_de_spec = PATH_COMMON + '/confspec.ini'
    logger = logSetup(
        PATH_COMMON + '/kerberus-cliente-config.log', 1, 1, 1, "Config")
else:
    if PLATAFORMA == 'Linux':
        PATH_COMMON = '/usr/share/kerberus'
        archivo_de_configuracion = '/etc/kerberus/cliente.conf'
        archivo_de_spec = PATH_COMMON + '/confspec.ini'
        logger = logSetup(
            '/tmp/kerberus-cliente-config.log', 2, 1, 1, "Config")
    else:
        import _winreg
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
        except WindowsError:
            try:
                key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\kerberus')
            except:
                logger.log(logging.ERROR, "No se pudo leer la clave del registro kerberus-common")
        except:
            logger.log(logging.ERROR, "No se pudo leer la clave del registro kerberus-common")

        PATH_COMMON = _winreg.QueryValueEx(key, 'kerberus-common')[0]
        archivo_de_configuracion = PATH_COMMON + '\cliente.conf'
        archivo_de_spec = PATH_COMMON + '\confspec.ini'
        logger = logSetup(PATH_COMMON + '\config.log', 2, 1)

#logger.log(logging.INFO, "Plataforma detectada %s" % platform.uname()[0])
#logger.log(logging.INFO,
    #"Utiliando el archivo de configuracion: %s" % archivo_de_configuracion)
#logger.log(logging.INFO, "Utiliando el archivo de spec: %s" % archivo_de_spec)

config = ConfigObj(archivo_de_configuracion, configspec=archivo_de_spec)
validator = Validator()
result = config.validate(validator)

if result != True:
    print "Error al leer el archivo de configuracion!!!"
    for (section_list, key, _) in flatten_errors(config, result):
        if key is not None:
            print 'El parámetro "%s" de la sección "%s" es incorrecto' % \
                (key, ', '.join(section_list))
            logger.log(logging.ERROR, 'El parámetro "%s" de la sección "%s" '\
            'es incorrecto' % (key, ', '.join(section_list)))
        else:
            print 'No se encontro la sección:%s ' % ', '.join(section_list)
            logger.log(logging.ERROR,
                'No se encontro la sección:%s ' % ', '.join(section_list))
else:
    #print "Se leyo la configuración del cliente correctamente"
    #logger.log(
        #logging.DEBUG,
        #'Se leyo la configuracion del cliente correctamente'
        #)

    #revisar y arreglar para que quede mejor
    PATH_TEMPLATES = PATH_COMMON + '/templates'
    ##

    if  platform.uname()[0] == 'Linux':
        # Si estan vacio estos campos pongo default para linux
        if config['client']['path_db']:
            PATH_DB = config['client']['path_db']
        else:
            PATH_DB = PATH_COMMON + '/kerberus.db'

        if config['client']['log_filename']:
            LOG_FILENAME = config['client']['log_filename']
        else:
            LOG_FILENAME = '/var/log/kerberus-cliente.log'
        if config['sync']['log_filename']:
            SYNC_LOG_FILENAME = config['sync']['log_filename']
        else:
            SYNC_LOG_FILENAME = '/var/log/kerberus-cliente.log'
        SYSTRAY_LOGFILE = '/var/log/kerberus-systray.log'
    else:
        # Si estan vacio estos campos pongo default para windows
        if config['client']['path_db']:
            PATH_DB = config['client']['path_db']
        else:
            LOG_FILENAME = config['client']['log_filename']
            PATH_DB = PATH_COMMON + '\kerberus.db'
        if config['client']['log_filename']:
            LOG_FILENAME = config['client']['log_filename']
        else:
            LOG_FILENAME = PATH_COMMON + '\kerberus-cliente.log'
        if config['sync']['log_filename']:
            SYNC_LOG_FILENAME = config['sync']['log_filename']
        else:
            SYNC_LOG_FILENAME = PATH_COMMON + '\kerberus-syncd-cliente.log'
        SYSTRAY_LOGFILE = PATH_COMMON + '\kerberus-systray.log'

    #######
    # Asignaciones desde archivo de conf
    ########
    # Constantes de debug
    logger.log(logging.DEBUG, "PATH_DB: %s" % PATH_DB)
    logger.log(logging.DEBUG, "LOG_FILENAME: %s" % LOG_FILENAME)
    logger.log(logging.DEBUG, "SYNC_LOG_FILENAME: %s" % SYNC_LOG_FILENAME)
    DEBUG_EXTENSIONES = config['debug']['debug_extensiones']
    DEBUG_DOM_PERM = config['debug']['debug_dominios_permitidos']
    DEBUG_DOM_DENG = config['debug']['debug_deminios_denegados']
    DEBUG_DOM_PUB_PERM = \
        config['debug']['debug_dominios_publicamente_permitidos']
    DEBUG_DOM_PUB_DENG = \
        config['debug']['debug_dominios_publicamente_denegados']
    DEBUG_CACHEADA_PERM = config['debug']['debug_cacheada_permitida']
    DEBUG_CACHEADA_DENG = config['debug']['debug_cacheada_denegada']
    DEBUG_VALIDA_REM = config['debug']['debug_valida_remotamente']
    DEBUG_NO_VALIDA_REM = config['debug']['debug_denegada_remotamente']
    DEBUG_TIEMPO_REMOTO = config['debug']['debug_tiempo_validacion_remota']
    DEBUG_IS_ADMIN = config['debug']['debug_peticiones_admin']
    LOG_TIEMPOS_MAYORES_A = config['debug']['debug_tiempos_mayores_a']

    # sincronizador
    SYNC_SERVER_IP = config['sync']['ip']
    SYNC_SERVER_PORT = config['sync']['port']
    SYNC_LOG_SIZE_MB = config['sync']['log_size_mb']
    SYNC_LOG_CANT_ROTACIONES = config['sync']['log_cantidad_de_rotaciones']
    SYNC_LOGLEVEL = config['sync']['loglevel']
    logger.log(logging.DEBUG, "Sincronizador: %s:%s" %  \
        (SYNC_SERVER_IP, SYNC_SERVER_PORT,))

    #Cliente
    CLIENT_LOG_FILENAME = config['client']['log_filename']
    BIND_ADDRESS = config['client']['bind_address']
    BIND_PORT = config['client']['bind_port']
    USAR_PROXY = config['client']['usar_proxy']
    PROXY_IP = config['client']['proxy_ip']
    PROXY_PORT = config['client']['proxy_port']
    LOG_SIZE_MB = config['client']['log_size_mb']
    LOG_CANT_ROTACIONES = config['client']['log_cantidad_de_rotaciones']
    LOGLEVEL = config['client']['loglevel']
    EDAD_CACHE = config['client']['edad_cache']


    logger.log(logging.DEBUG,
        "Cliente escuchando en: %s:%s" % (BIND_ADDRESS, BIND_PORT,))
    logger.log(logging.DEBUG,
        "Cliente usando proxy: ( %s ) direccion %s:%s" %  \
        (USAR_PROXY, PROXY_IP, PROXY_PORT,))

    # Server
    SERVER_IP = config['server']['ip']
    SERVER_PORT = config['server']['port']
    MAX_CACHE_URLS_ACEPTADAS = config['server']['max_urls_aceptadas_cacheadas']
    MAX_CACHE_URLS_DENEGADAS = config['server']['max_urls_denegadas_cacheadas']
    logger.log(logging.DEBUG, "Validador: %s:%s" % (SERVER_IP, SERVER_PORT,))
