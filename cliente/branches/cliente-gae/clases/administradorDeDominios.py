# -*- coding: utf-8 -*-
#
"""Modulo que carga la configuracion particular del usuario ingresado"""

# Modulos externos
import re
import sqlite3
import sys
import logging
import time

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
        self.recargarDominios()

    def recargarDominios(self):
        self.cargarDominiosDenegados()
        self.cargarDominiosPermitidos()
        self.cargarDominiosPublicamentePermitidos()
        self.cargarDominiosPublicamenteDenegados()
        self.borrarDominiosViejosCache()
        self.cargarDominiosCacheados()

    def recargarDominiosUsuario(self):
        self.cargarDominiosDenegados()
        self.cargarDominiosPermitidos()
        modulo_logger.info("Dominios Permitidos: %s", self.dominios_permitidos)
        modulo_logger.info("Dominios Denegados: %s", self.dominios_denegados)

    def cargarDominiosDenegados(self):
        """Carga desde la base de datos a memoria los dominios denegados"""
        modulo_logger.info("Recargando dominios denegados por el usuario")
        self.dominios_denegados = []
        try:
            conexion = sqlite3.connect(config.PATH_DB)
            cursor = conexion.cursor()
            usuario_nobody = 2
            respuesta = cursor.execute(
                'select url from dominios_usuario du, estado e where '
                'du.estado = e.id and '
                'du.usuario=? and e.estado=?', (usuario_nobody, 'Denegado')
            ).fetchall()
            modulo_logger.info(respuesta)
            for fila in respuesta:
                self.dominios_denegados.append(fila[0])
            conexion.close()
        except sqlite3.OperationalError, msg:
            modulo_logger.error('Error cargando dominios denegados: %s', msg)
            conexion.close()

    def cargarDominiosPermitidos(self):
        """Carga desde la base de datos a memoria los dominios permitidos"""
        modulo_logger.info("Recargando dominios permitidos por el usuario")
        self.dominios_permitidos = []
        try:
            conexion = sqlite3.connect(config.PATH_DB)
            cursor = conexion.cursor()
            usuario_nobody = 2
            respuesta = cursor.execute(
                'select url from dominios_usuario du, estado e where '
                'du.estado=e.id and '
                'du.usuario=? and e.estado=?', (usuario_nobody, 'Permitido')
            ).fetchall()
            for fila in respuesta:
                self.dominios_permitidos.append(fila[0])
            conexion.close()
        except sqlite3.OperationalError, msg:
            modulo_logger.error('Error cargando dominios permitidos: %s', msg)
            conexion.close()

    def cargarDominiosPublicamentePermitidos(self):
        """Carga desde la base de datos a memoria los dominios
        Publicamente permitidos"""
        modulo_logger.debug("Recargando dominios publicamente "
        "permitidos")
        self.dominios_publicamente_permitidos = []
        try:
            conexion = sqlite3.connect(config.PATH_DB)
            cursor = conexion.cursor()
            respuesta = cursor.execute(
            'select url from dominios_kerberus dk, estado e where '
            'dk.estado=e.id and e.estado=?', ('Permitido',)
            ).fetchall()
            for fila in respuesta:
                self.dominios_publicamente_permitidos.append(fila[0])
            conexion.close()
        except sqlite3.OperationalError, msg:
            modulo_logger.error('Error cargando dominios publicamente '
                                    'permitidos: %s', msg)
            conexion.close()

    def cargarDominiosPublicamenteDenegados(self):
        """Carga desde la base de datos a memoria los dominios
        Publicamente denegados"""
        modulo_logger.debug("Recargando dominios publicamente denegados")
        self.dominios_publicamente_denegados = []
        try:
            conexion = sqlite3.connect(config.PATH_DB)
            cursor = conexion.cursor()
            respuesta = cursor.execute(
                'select url from dominios_kerberus dk, estado e where '
                'dk.estado=e.id and e.estado=?', ('Denegado',)
                ).fetchall()
            for fila in respuesta:
                self.dominios_publicamente_denegados.append(fila[0])
            conexion.close()
        except sqlite3.OperationalError, msg:
            modulo_logger.error('Error cargando dominios publicamente '
                                    'denegados: %s', msg)
            conexion.close()

    def cargarDominiosCacheados(self):
        """Carga desde la base de datos a memoria los dominios
        cacheados"""
        modulo_logger.debug("Recargando dominios cacheados")
        try:
            # Dominios permitidos
            conexion = sqlite3.connect(config.PATH_DB)
            cursor = conexion.cursor()
            respuesta = cursor.execute(
                'select dominio from cache_dominios cd, estado e where '
                'cd.estado=e.id and e.estado=?', ('Permitido',)
                ).fetchall()
            for fila in respuesta:
                self.dominios_publicamente_permitidos.append(fila[0])
            # Dominios denegados
            respuesta = cursor.execute(
                'select dominio from cache_dominios cd, estado e where '
                'cd.estado=e.id and e.estado=?', ('Denegado',)
                ).fetchall()
            for fila in respuesta:
                self.dominios_publicamente_denegados.append(fila[0])
            conexion.close()
        except sqlite3.OperationalError, msg:
            modulo_logger.error('Error cargando dominios cacheados:', msg)
            conexion.close()

    def borrarDominiosViejosCache(self):
        """Elimina los dominios cacheados viejos"""
        modulo_logger.debug("Eliminando dominios cacheados viejos")
        try:
            # Dominios permitidos
            hora_actual = time.time()
            # edad_cache esta en segundos
            limite = hora_actual - config.EDAD_CACHE
            conexion = sqlite3.connect(config.PATH_DB)
            cursor = conexion.cursor()
            cursor.execute('delete from cache_dominios where hora < ?',
                                (limite,))
            conexion.commit()
            conexion.close()
        except sqlite3.OperationalError, msg:
            modulo_logger.error('Error mientras se borraban los dominios'
                                ' viejos de la cache. Error: %s', msg)
            conexion.rollback()
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

    def cachearDominio(self, dominio, estado):
        if estado == 'Permitido':
            estado_num = 1
        else:
            estado_num = 2
        hora = time.time()
        try:
            conexion = sqlite3.connect(config.PATH_DB)
            cursor = conexion.cursor()
            cursor.execute('insert into cache_dominios(dominio, hora, estado) '
                            'values(?,?,?)', (dominio, hora, estado_num))
            conexion.commit()
            conexion.close()
        except:
            conexion.rollback()
            conexion.close()

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
                    self.cachearDominio(dominio, 'Permitido')

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
                    self.cachearDominio(dominio, 'Denegado')
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