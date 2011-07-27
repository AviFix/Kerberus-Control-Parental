# -*- coding: utf-8 -*-

import platform, os

if  platform.uname()[0] == 'Linux':
    PATH_DB='/var/cache/kerberus/kerberus.db'
    LOG_FILENAME='/var/log/kerberus-cliente.log'    
else:
    import _winreg
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
    PATH_DB=_winreg.QueryValueEx(key,'kerberus-common')[0]+'\kerberus.db' 
    LOG_FILENAME=_winreg.QueryValueEx(key,'kerberus-common')[0]+'\kerberus-cliente.log'
    # Verifico si esta instalado el firefox y seteo el proxy
    try:
        key_path = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\Mozilla\Mozilla Firefox')
        firefox_version =  _winreg.QueryValueEx(key_path,'CurrentVersion')[0]
        firefox_key_path=r'Software\Mozilla\Mozilla Firefox\%s\Main' % firefox_version
        Firefox_path_reg = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, firefox_key_path)
        firefox_install_dir= _winreg.QueryValueEx(Firefox_path_reg,'Install Directory')[0]
    except:
        print "No esta firefox instalado"
   
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
SERVER_IP="kerberus.com.ar"
SERVER_PORT="8081"
SERVER_SINC_PORT="8083"
MAX_CACHE_URLS_ACEPTADAS=10
MAX_CACHE_URLS_DENEGADAS=10
