#!/usr/bin/env python
import time, sqlite3

from clases import *

# Constantes de self.debug
DEBUG_EXTENSIONES=False
DEBUG_DOM_PERM=False
DEBUG_DOM_DENG=False
DEBUG_DOM_PUB_PERM=True
DEBUG_DOM_PUB_DENG=True
DEBUG_CACHEADA_PERM=False
DEBUG_CACHEADA_DENG=False
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
            print "Tiempo: %s segs.\n" % tiempototal
            
    def extensionValida(self, url):
        url=url.lower()
        return re.match(".*\.(gif|jpeg|jpg|png|js|css|swf|ico|json|mp3|wav|rss|rar|zip|pdf|xml)$",url)   
        
    def validarUrl(self, username, password, url):
        if not self.usuarios.usuario_valido(username, password):
            return False, "Usuario no valido"
            
        usuario=self.usuarios.obtenerUsuario(username)
        self.inicio=time.time()
        if usuario.es_admin:
            mensaje= "Usuario administrador"
            return True, mensaje
            self.debug(mensaje, DEBUG_IS_ADMIN)
            
        elif usuario.dominioDenegado(url):
            mensaje="Dominio denegado: " + url
            self.debug(mensaje, DEBUG_DOM_DENG)
            return False, mensaje
            
        elif usuario.dominioPermitido(url):
            mensaje = "Dominio permitido: " + url
            self.debug(mensaje, DEBUG_DOM_PERM)
            return True,  mensaje
            
        elif usuario.dominioPublicamentePermitido(url):
            mensaje = "Dominio publicamente permitido: " + url
            self.debug(mensaje, DEBUG_DOM_PUB_PERM)
            return True, mensaje
            
        elif usuario.dominioPublicamenteDenegado(url):
            mensaje = "Dominio publicamente denegado: " + url
            self.debug(mensaje, DEBUG_DOM_PUB_DENG)
            return False, mensaje
            
        elif self.extensionValida(url):
            mensaje = "Exension valida: " + url
            self.debug(mensaje , DEBUG_EXTENSIONES)
            return True, mensaje
            
        elif usuario.cacheAceptadas(url):
            mensaje = "CACHEADA, Autorizada: " + url
            self.debug(mensaje, DEBUG_CACHEADA_PERM)
            return True, mensaje
            
        elif usuario.cacheDenegadas(url):
            mensaje = "CACHEADA, Denegada: " + url
            self.debug(mensaje, DEBUG_CACHEADA_PERM)
            return False, mensaje
        else:
            valido, razon= usuario.validarRemotamente(url)
            if valido:
                mensaje = "Url validada remotamente : " + url
                self.debug(mensaje, DEBUG_VALIDA_REM)
                return True,  ""
            else:
                mensaje = "Url denegada remotamente : " + url+"\n"+"Motivo: "+razon
                self.debug(mensaje, DEBUG_NO_VALIDA_REM)
                return False, mensaje
