#!/usr/bin/env python
import time, sqlite3
#from pysqlite2 import dbapi2 as sqlite3

from clases import *

# Constantes de self.debug
DEBUG_EXTENSIONES=False
DEBUG_DOM_PERM=False
DEBUG_DOM_DENG=True
DEBUG_DOM_PUB_PERM=False
DEBUG_DOM_PUB_DENG=True
DEBUG_CACHEADA_PERM=False
DEBUG_CACHEADA_DENG=True
DEBUG_VALIDA_REM=True
DEBUG_NO_VALIDA_REM=True
DEBUG_TIEMPO_REMOTO=True
DEBUG_IS_ADMIN=False


# Codigo central

class Consultor:
    def __init__(self):
        self.usuarios=AdministradorDeUsuarios()        
        
    def debug(self, texto, activo):
        if activo:
            fin=time.time()
            tiempototal=fin-self.inicio
            print  texto
            print "Tiempo: %s segs." % tiempototal
            
    def extensionValida(self, url):
        url=url.lower()
        return re.match(".*\.(gif|jpeg|jpg|png|js|css|swf|ico|json|mp3|wav|rss|rar|zip|pdf|xml)$",url)   
        
    def validarUrl(self, username, password, url):
        if not self.usuarios.usuario_valido(username, password):
            return False, "Usuario no valido"
            
        usuario=self.usuarios.obtenerUsuario(username)
        self.inicio=time.time()
        if usuario.es_admin:
            return True,  "Usuario administrador"
            self.debug("Usuario Administrador\n", DEBUG_IS_ADMIN)
            
        elif usuario.dominioDenegado(url):
            self.debug("Dominio denegado: " + url+"\n", DEBUG_DOM_DENG)
            return False, "Dominio Denegado"
            
        elif usuario.dominioPermitido(url):
            self.debug("Dominio permitido: " + url+"\n", DEBUG_DOM_PERM)
            return True,  "Dominio permitido"
            
        elif usuario.dominioPublicamentePermitido(url):
            self.debug("Dominio publicamente permitido: " + url+"\n", DEBUG_DOM_PUB_DENG)
            return True, "Dominio publicamente permitido"
            
        elif usuario.dominioPublicamenteDenegado(url):
            self.debug("Dominio publicamente denegado: " + url+"\n", DEBUG_DOM_PUB_PERM)
            return False, "Dominio publicamente denegado"
            
        elif self.extensionValida(url):
            self.debug("Exension valida: " + url +"\n", DEBUG_EXTENSIONES)
            return True, "Exension valida"
            
        elif usuario.cacheAceptadas(url):
            self.debug("CACHEADA, Autorizada: " + url+"\n", DEBUG_CACHEADA_PERM)
            return True, "CACHEADA, Autorizada"
            
        elif usuario.cacheDenegadas(url):
            self.debug("CACHEADA, Denegada: " + url+"\n", DEBUG_CACHEADA_PERM)
            return False, "CACHEADA, Denegada"
            
        elif usuario.validarRemotamente(url):
            self.debug("Url validada remotamente : " + url+"\n", DEBUG_VALIDA_REM)
            return True,  "Url validada remotamente"
            
        else:
            self.debug("Url denegada remotamente : " + url+"\n", DEBUG_NO_VALIDA_REM)
            return False, "Url denegada remotamente"
