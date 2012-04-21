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
import peticion

# Clase
class Registradores:
    def __init__(self):
        self.conexion_db = sqlite3.connect(config.PATH_DB)
        self.cursor=self.conexion_db.cursor()
        self.logger = funciones.logSetup (config.LOG_FILENAME, config.LOGLEVEL, config.LOG_SIZE_MB, config.LOG_CANT_ROTACIONES,"registrar")

    def __del__(self):
        self.cursor.close()

    #FIXME: Utilizar mysql-cluster!!!!!!! porque sino va a haber replicacion de usuarios con diferentes ids.
    def checkRegistradoRemotamente(self):
        """Verifica si esta registrado remotamente"""
        id, nombre, email, version, password=self.obtenerDatosRegistrados()
        if id > 0:
            peticionRemota=peticion.Peticion()
            registrado=peticionRemota.usuarioRegistrado(id, email)
            return (registrado <> None)
        else:
            return False

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

    def registrarLocalmente(self,nombre,email,password):
        """Registra localmente los datos solicitados al momento de la instalacion"""
        try:
            #TODO: despues de que envie la contrasena se deberia borrar
            self.cursor.execute('update instalacion set nombretitular=?, email=?, password=?', (str(nombre),str(email),str(password)))
            self.conexion_db.commit()
            admUser=administradorDeUsuarios.AdministradorDeUsuarios()
            admUser.setPassword('admin', str(password))
            self.logger.log(logging.INFO,"Password seteada correctamente")
        except sqlite3.OperationalError, msg:
            self.logger.log(logging.ERROR,"No se pudo registrar la instalacion localmente. Tal vez no esta la base de datos instalada.\nERROR: %s" % msg)

    def registrarRemotamente(self):
        """Registra localmente los datos solicitados al momento de la instalacion"""
        id, nombre, email, version, password=self.obtenerDatosRegistrados()
        peticionRemota=peticion.Peticion()
        id_obtenido=peticionRemota.registrarUsuario(nombre, email, password,version)
        if (int(id_obtenido) > 0):
            self.cursor.execute('update instalacion set id =?', (id_obtenido,))
            self.conexion_db.commit()
            self.logger.log(logging.INFO,'Se registro correctamente la instalacion')
        else:
            self.logger.log(loggin.ERROR,'Hubo un error al tratar de registrarse remotamente')

    def eliminarRemotamente(self):
        """Ejecutado cuando un usuario desinstala el soft"""
        id, nombre, email, version, password=self.obtenerDatosRegistrados()
        peticionRemota=peticion.Peticion(id)
        id_obtenido=peticionRemota.eliminarUsuario(id)

    def obtenerDatosRegistrados(self):
        """Devuelve id, nombre, email y version"""
        try:
            id, nombre, email, version, password = self.cursor.execute('select id, nombretitular, email, version, password from instalacion').fetchone()
        except sqlite3.OperationalError, msg:
            self.logger.log(logging.ERROR,"No se pudieron obtener los datos locales de la instalacion. Tal vez no esta la base de datos instalada.\nError: %s" % msg)
            id=0
            nombre=""
            email=""
            version=""
            password=""
        return id, nombre, email, version, password
