# -*- coding: utf-8 -*-

import platform, os

if  platform.uname()[0] == 'Linux':
    PATH_DB='/var/cache/kerberus/kerberus.db'
    LOG_FILENAME='/var/log/kerberus-cliente.log'    
else:
    PATH_DB='..\kerberus.db'
    LOG_FILENAME='..\kerberus-cliente.log'
   
# Constantes de debug
DEBUG_EXTENSIONES=False
DEBUG_DOM_PERM=False
DEBUG_DOM_DENG=False
DEBUG_DOM_PUB_PERM=False
DEBUG_DOM_PUB_DENG=False
DEBUG_CACHEADA_PERM=False
DEBUG_CACHEADA_DENG=False
DEBUG_VALIDA_REM=False
DEBUG_NO_VALIDA_REM=False
DEBUG_TIEMPO_REMOTO=False
DEBUG_IS_ADMIN=False
LOG_TIEMPOS_MAYORES_A=1

#Cliente
BIND_ADDRESS = "0.0.0.0"
BIND_PORT = 8080
LOG_SIZE_MB =20
LOG_CANT_ROTACIONES =5
SERVER_IP="kerberus.com.ar"
SERVER_PORT="8081"
MAX_CACHE_URLS_ACEPTADAS=10
MAX_CACHE_URLS_DENEGADAS=10
