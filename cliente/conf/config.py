import platform, os

if  platform.uname()[0] == 'Linux':
    PATH_DB='/var/cache/securedfamily/securedfamily.db'
    LOG_FILENAME='/var/log/securedfamily-cliente.log'    
else:
    PATH_DB='C:\securedfamily.db'
    LOG_FILENAME='C:\securedfamily-cliente.log'
    
# Constantes de debug
DEBUG_EXTENSIONES=False
DEBUG_DOM_PERM=True
DEBUG_DOM_DENG=True
DEBUG_DOM_PUB_PERM=True
DEBUG_DOM_PUB_DENG=True
DEBUG_CACHEADA_PERM=True
DEBUG_CACHEADA_DENG=True
DEBUG_VALIDA_REM=True
DEBUG_NO_VALIDA_REM=True
DEBUG_TIEMPO_REMOTO=True
DEBUG_IS_ADMIN=False
LOG_TIEMPOS_MAYORES_A=1

#Cliente
BIND_ADDRESS = "0.0.0.0"
BIND_PORT = 8080
LOG_SIZE_MB =20
LOG_CANT_ROTACIONES =5
SECUREDFAMILYSERVER="securedfamily.no-ip.org"
SECUREDFAMILYSERVER_PORT="8081"
