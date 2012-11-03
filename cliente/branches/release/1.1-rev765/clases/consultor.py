# -*- coding: utf-8 -*-

"""Modulo encargado de verificar la aptitud de una url"""

#Modulos externos
import time
import re
#import sys

#Modulos propios
import administradorDeUsuarios
#import manejadorUrls
#import usuario
import config
#import servidores
import logging


modulo_logger = logging.getLogger('kerberus.' + __name__)


#Excepciones
class ConsultorError(Exception):

    def __init__(self):
        super(ConsultorError, self).__init__()
        pass


# Clase
class Consultor:
    def __init__(self):
        self.primerUrl = True
        self.kerberus_activado = True
        self.usuarios = administradorDeUsuarios.AdministradorDeUsuarios()

    def extensionValida(self, url):
        url = url.lower()
        return re.match(".*\.(gif|jpeg|jpg|png|js|css|swf|ico|json|mp3|wav|"\
        "rss|rar|zip|pdf|xml)$", url)

    def urlBienFormada(self, url):
        url = url.lower()
        return re.match(".*\..*/.*", url)

    def validarUrl(self, username, password, url):
        if not self.urlBienFormada(url):
            mensaje = "URL mal formada"
            modulo_logger.log(logging.DEBUG, mensaje)
            return True, mensaje

        #TODO: No se si esto esta bien, revisar
        if "kerberus.com.ar" in url:
            mensaje = "Consulta a kerberus"
            modulo_logger.log(logging.DEBUG, mensaje)
            return True, mensaje

        if not self.usuarios.usuario_valido(username, password):
            return False, "Usuario no valido"

        usuario = self.usuarios.obtenerUsuario(username)
        self.inicio = time.time()
        if usuario.es_admin:
            mensaje = "Usuario administrador"
            return True, mensaje
            if config.DEBUG_IS_ADMIN:
                modulo_logger.log(logging.INFO, mensaje)

        elif usuario.dominioDenegado(url):
            mensaje = "Dominio no permitido."
            if config.DEBUG_DOM_DENG:
                modulo_logger.log(logging.INFO, mensaje)
            return False, mensaje

        elif usuario.dominioPermitido(url):
            mensaje = "Dominio permitido"
            if config.DEBUG_DOM_PERM:
                modulo_logger.log(logging.INFO, mensaje)
            return True, mensaje

        elif usuario.dominioPublicamentePermitido(url):
            mensaje = "Dominio permitido"
            if config.DEBUG_DOM_PUB_PERM:
                modulo_logger.log(logging.INFO, mensaje)
            return True, mensaje

        elif usuario.dominioPublicamenteDenegado(url):
            mensaje = "Dominio denegado: "
            if config.DEBUG_DOM_PUB_DENG:
                modulo_logger.log(logging.INFO, mensaje)
            return False, mensaje

        elif self.extensionValida(url):
            mensaje = "Exension valida: " + url
            if config.DEBUG_EXTENSIONES:
                modulo_logger.log(logging.INFO, mensaje)
            return True, mensaje

        elif usuario.cacheAceptadas(url):
            mensaje = "CACHEADA, Autorizada: " + url
            if config.DEBUG_CACHEADA_PERM:
                modulo_logger.log(logging.INFO, mensaje)
            return True, mensaje

        elif usuario.cacheDenegadas(url):
            mensaje = "CACHEADA, Denegada: " + url
            if config.DEBUG_CACHEADA_PERM:
                modulo_logger.log(logging.INFO, mensaje)
            return False, mensaje
        else:
            valido, razon = usuario.validarRemotamente(url)
            if valido:
                mensaje = "Url validada remotamente : " + url
                if config.DEBUG_VALIDA_REM:
                    modulo_logger.log(logging.INFO, mensaje)
                return True, ""
            else:
                mensaje = "URL: %s <br>Motivo: %s" % (url, razon)
                if config.DEBUG_NO_VALIDA_REM:
                    modulo_logger.log(logging.INFO, mensaje)
                return False, mensaje
