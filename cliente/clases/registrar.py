# -*- coding: utf-8 -*-
#
"""Modulo que permite registrar el cliente, local y remotamente"""

# Modulos externos
import sqlite3, sys, logging

# Modulos propios
sys.path.append('../conf')
sys.path.append('../')

import config
import funciones
import administradorDeUsuarios

# Clase
class Registradores:
    def __init__(self):
        self.conexion_db = sqlite3.connect(config.PATH_DB)
        self.cursor=self.conexion_db.cursor()
        self.logger = funciones.logSetup (config.LOG_FILENAME, config.LOGLEVEL, config.LOG_SIZE_MB, config.LOG_CANT_ROTACIONES,"registrar")

    def __del__(self):
        self.cursor.close()

    def checkRegistradoRemotamente(self):
        """Verifica y trata de registrar remotamente a la instalacion"""
        #TODO: hacer funcion checkRegistradoRemotamente
        pass

    def checkRegistradoLocalmente(self):
        """Verifica si estan registrado los datos del usuario"""
        try:
            registrado=self.cursor.execute('select count(*) from instalacion where nombretitular <> ""').fetchone()[0]
        except sqlite3.OperationalError, msg:
            self.logger.log(logging.ERROR,"No se pudieron verificar los datos de instalacion. Tal vez no esta la base de datos instalada.\nERROR: %s" % msg)
            registrado=False
        if registrado >= 1:
            return True
        else:
            return False

    def registrarLocalmente(self,nombre,email,password,version):
        """Registra localmente los datos solicitados al momento de la instalacion"""
        try:
            #TODO: despues de que envie la contrasena se deberia borrar
            self.cursor.execute('update instalacion set nombretitular=?, email=?, password=?, version=?', (str(nombre),str(email),str(password),str(version)))
            self.conexion_db.commit()
            admUser=administradorDeUsuarios.AdministradorDeUsuarios()
            admUser.setPassword('admin', str(password))
            self.logger.log(logging.INFO,"Password seteada correctamente")
        except sqlite3.OperationalError, msg:
            self.logger.log(logging.ERROR,"No se pudo registrar la instalacion localmente. Tal vez no esta la base de datos instalada.\nERROR: %s" % msg)

    def registrarRemotamente(self):
        """Registra localmente los datos solicitados al momento de la instalacion"""
        #TODO: hacer funcion registrarRemotamente

        pass

    def obtenerDatosRegistrados(self):
        """Devuelve id, nombre, email y version"""
        try:
            id, nombre, email, version, password = self.cursor.execute('select id, nombretitular, email, version, password from instalacion').fetchone()
        except sqlite3.OperationalError, msg:
            self.logger.log(logging.ERROR,"No se pudieron obtener los datos locales de la instalacion. Tal vez no esta la base de datos instalada.\nError: %s" % msg)
            id=-1
            nombre=""
            email=""
            version=""
            password=""
        return id, nombre, email, version, password
