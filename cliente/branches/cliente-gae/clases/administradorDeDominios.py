# -*- coding: utf-8 -*-
#
"""Modulo que carga la configuracion particular del usuario ingresado"""

# Modulos externos
import re
import sqlite3
import sys
import logging

sys.path.append('../conf')

modulo_logger = logging.getLogger('kerberus.' + __name__)

# Modulos propios
import config


# Clase
class Handler:
    def __init__(self, peticionRemota=None, usuario='NoBody'):
        if peticionRemota is None:
            import peticion
            peticionRemota = peticion.Peticion()
        self.peticionRemota = peticionRemota
        self.usuario = usuario
        conexion = sqlite3.connect(config.PATH_DB)
        self.cursor = conexion.cursor()
        self.cargarDominiosDenegados()
        self.cargarDominiosPermitidos()
        self.cargarDominiosPublicamentePermitidos()
        self.cargarDominiosPublicamenteDenegados()

    #def agregarDominio(self, url, estado):

    def cargarDominiosDenegados(self):
        """Carga desde la base de datos a memoria los dominios denegados"""
        modulo_logger.debug("Recargando dominios denegados")
        self.dominios_denegados = []
        respuesta = self.cursor.execute(
            'select url from dominios_usuario du, estado e where '
            'du.estado = e.id and '
            'du.usuario=? and e.estado=?', (self.usuario, 'Denegado')
            ).fetchall()
        for fila in respuesta:
            self.dominios_denegados.append(fila[0])

    def cargarDominiosPermitidos(self):
        """Carga desde la base de datos a memoria los dominios permitidos"""
        modulo_logger.debug("Recargando dominios permitidos")
        self.dominios_permitidos = []
        respuesta = self.cursor.execute(
            'select url from dominios_usuario du, estado e where '
            'du.estado=e.id and '
            'du.usuario=? and e.estado=?', (self.usuario, 'Permitido')
            ).fetchall()
        for fila in respuesta:
            self.dominios_permitidos.append(fila[0])

    def cargarDominiosPublicamentePermitidos(self):
        """Carga desde la base de datos a memoria los dominios
        Publicamente permitidos"""
        modulo_logger.debug("Recargando dominios publicamente "
        "permitidos")
        conexion = sqlite3.connect(config.PATH_DB)
        cursor = conexion.cursor()
        self.dominios_publicamente_permitidos = []
        respuesta = cursor.execute(
            'select url from dominios_kerberus dk, estado e where '
            'dk.estado=e.id and e.estado=?', ('Permitido',)
            ).fetchall()
        for fila in respuesta:
            self.dominios_publicamente_permitidos.append(fila[0])
        conexion.close()

    def cargarDominiosPublicamenteDenegados(self):
        """Carga desde la base de datos a memoria los dominios
        Publicamente denegados"""
        modulo_logger.debug("Recargando dominios publicamente denegados")
        conexion = sqlite3.connect(config.PATH_DB)
        cursor = conexion.cursor()
        self.dominios_publicamente_denegados = []
        respuesta = cursor.execute(
            'select url from dominios_kerberus dk, estado e where '
            'dk.estado=e.id and e.estado=?', ('Denegado',)
            ).fetchall()
        for fila in respuesta:
            self.dominios_publicamente_denegados.append(fila[0])
        conexion.close()

    def dominioPermitido(self, url):
        """Verifica si el dominio esta en la lista de dominios permitidos"""
        for dominio in self.dominios_permitidos:
            if re.search(dominio, url):
                return True
        return False

    def dominioDenegado(self, url):
        """Verifica si el dominio esta en la lista de dominios denegados"""
        for dominio in self.dominios_denegados:
            if re.search(str(dominio), url):
                return True
        return False

    def dominioPublicamentePermitido(self, url):
        """Verifica si el dominio esta en la lista de dominios
        Publicamente permitidos"""
        try:
            dominio = url.split('/')[2]
            return dominio in self.dominios_publicamente_permitidos
        except:
            modulo_logger.error("Error al tratar de obtener el dominio desde "
                "la url: %s" % url)
            return True

    def dominioPublicamenteDenegado(self, url):
        """Verifica si el dominio esta en la lista de dominios
        Publicamente denegados"""
        try:
            dominio = url.split('/')[2]
            return dominio in self.dominios_publicamente_denegados
        except:
            modulo_logger.error("Error al tratar de obtener el dominio desde "
                "la url: %s" % url)
            return False

    def validarRemotamente(self, url):
        """Consulta al servidor por la url, porque no pudo determinar
        su aptitud"""

        modulo_logger.info("Validando remotamente: %s" % url)
        permitido, mensaje = self.peticionRemota.validarUrl(url)

        if permitido:
            try:
                dominio = url.split('/')[2]
                if dominio not in self.dominios_permitidos:
                    self.dominios_permitidos.append(dominio)
                    modulo_logger.info("Se agrega el dominio %s a la cache de"
                        " dominios locales permitidos" % dominio)
            except:
                modulo_logger.error("No se pudo agrega el dominio %s a la "
                    "cache de dominios locales permitidos" % dominio)
        else:
            try:
                dominio = url.split('/')[2]
                if dominio not in self.dominios_denegados:
                    self.dominios_denegados.append(dominio)
                    modulo_logger.info("Se agrega el dominio %s a la cache de"
                        " dominios locales denegados" % dominio)
            except:
                modulo_logger.error("No se pudo agrega el dominio %s a la "
                    "cache de dominios locales denegados" % dominio)
        return permitido, mensaje


def main():
    pass

# Importante: los módulos no deberían ejecutar
# código al ser importados
if __name__ == '__main__':
    main()