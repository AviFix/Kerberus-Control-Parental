# -*- coding: utf-8 -*-

"""Modulo encargado de verificar la aptitud de una url"""

#Modulos externos
import time, re, sys

#Modulos propios
import administradorDeUsuarios
import manejadorUrls
import usuario
import config
import logging
import funciones

#Excepciones
class ConsultorError(Exception): pass
#class nombre(ConsultorError): pass

# Logging
logger = funciones.logSetup (config.LOG_FILENAME, config.LOGLEVEL, config.LOG_SIZE_MB, config.LOG_CANT_ROTACIONES,"Modulo Consultor")

# Clase
class Consultor:
    def __init__(self):
        self.primerUrl=True
        self.kerberus_activado=True

    def extensionValida(self, url):
        url=url.lower()
        return re.match(".*\.(gif|jpeg|jpg|png|js|css|swf|ico|json|mp3|wav|rss|rar|zip|pdf|xml)$",url)

    def validarUrl(self, username, password, url):
        if "kerberus.com.ar" in url:
            mensaje = "Consulta a kerberus"
            logger.log(logging.INFO, mensaje)
            return True, mensaje

        if not self.usuarios.usuario_valido(username, password):
            return False, "Usuario no valido %s : %s" %(username, password, )

        usuario=self.usuarios.obtenerUsuario(username)
        self.inicio=time.time()
        if usuario.es_admin:
            mensaje= "Usuario administrador"
            return True, mensaje
            if config.DEBUG_IS_ADMIN:
                logger.log(logging.INFO, mensaje)

        elif usuario.dominioDenegado(url):
            mensaje="Dominio denegado: " + url
            if config.DEBUG_DOM_DENG:
                logger.log(logging.INFO, mensaje)
            return False, mensaje

        elif usuario.dominioPermitido(url):
            mensaje = "Dominio permitido: " + url
            if config.DEBUG_DOM_PERM:
                logger.log(logging.INFO, mensaje)
            return True,  mensaje

        elif usuario.dominioPublicamentePermitido(url):
            mensaje = "Dominio publicamente permitido: " + url
            if config.DEBUG_DOM_PUB_PERM:
                logger.log(logging.INFO, mensaje)
            return True, mensaje

        elif usuario.dominioPublicamenteDenegado(url):
            mensaje = "Dominio publicamente denegado: " + url
            if config.DEBUG_DOM_PUB_DENG:
                logger.log(logging.INFO, mensaje)
            return False, mensaje

        elif self.extensionValida(url):
            mensaje = "Exension valida: " + url
            if config.DEBUG_EXTENSIONES:
                logger.log(logging.INFO, mensaje)
            return True, mensaje

        elif usuario.cacheAceptadas(url):
            mensaje = "CACHEADA, Autorizada: " + url
            if config.DEBUG_CACHEADA_PERM:
                logger.log(logging.INFO, mensaje)
            return True, mensaje

        elif usuario.cacheDenegadas(url):
            mensaje = "CACHEADA, Denegada: " + url
            if config.DEBUG_CACHEADA_PERM:
                logger.log(logging.INFO, mensaje)
            return False, mensaje
        else:
            valido, razon= usuario.validarRemotamente(url)
            if valido:
                mensaje = "Url validada remotamente : " + url
                if config.DEBUG_VALIDA_REM:
                    logger.log(logging.INFO, mensaje)
                return True,  ""
            else:
                mensaje = "URL: %s <br>Motivo: %s" % (url,  razon)
                if config.DEBUG_NO_VALIDA_REM:
                    logger.log(logging.INFO, mensaje)
                return False, mensaje
