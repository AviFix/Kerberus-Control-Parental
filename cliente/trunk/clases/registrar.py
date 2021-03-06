# -*- coding: utf-8 -*-
#
"""Modulo que permite registrar el cliente, local y remotamente"""

# Modulos externos
import sqlite3
import sys
import logging

modulo_logger = logging.getLogger('kerberus.' + __name__)

sys.path.append('../conf')
sys.path.append('../')

# Modulos propios
import config
import administradorDeUsuarios
import peticion


# Clase
class Registradores:
    def __init__(self, peticion=peticion.Peticion()):
        self.conexion_db = sqlite3.connect(config.PATH_DB)
        self.cursor = self.conexion_db.cursor()
        self.peticionRemota = peticion

    def __del__(self):
        self.cursor.close()

    def checkRegistradoRemotamente(self):
        """Verifica si esta registrado remotamente"""
        id, nombre, email, version, password = self.obtenerDatosRegistrados()
        if id > 0:
            registrado = self.peticionRemota.usuarioRegistrado(id, email)
            return (registrado != 'False')
        else:
            return False

    def checkRegistradoLocalmente(self):
        """Verifica si estan registrado los datos del usuario"""
        try:
            registrado = self.cursor.execute('select count(*) from instalacion'
            ' where nombretitular <> ""').fetchone()[0]
        except sqlite3.OperationalError, msg:
            modulo_logger.log(logging.ERROR, "No se pudieron verificar los "
            "datos de instalacion. Tal vez no esta la base de datos instalada."
            "\nERROR: %s" % msg)
            registrado = False
        if registrado >= 1:
            return True
        else:
            return False

    def registrarLocalmente(self, nombre, email, password):
        """Registra localmente los datos solicitados al momento de la
        instalacion"""
        try:
            #TODO: despues de que envie la contrasena se deberia borrar
            self.cursor.execute('update instalacion set nombretitular=?, '
            'email=?, password=?', (nombre, email, password))
            self.conexion_db.commit()
            admUser = administradorDeUsuarios.AdministradorDeUsuarios()
            admUser.setPassword('admin', password)
            modulo_logger.log(logging.INFO, "Password seteada correctamente")
        except sqlite3.OperationalError, msg:
            modulo_logger.log(logging.ERROR, "No se pudo registrar la "
            "instalacion localmente. Tal vez no esta la base de datos "
            "instalada.\nERROR: %s" % msg)

    def registrarRemotamente(self):
        """Registra remotamente los datos solicitados al momento de la
        instalacion"""
        id, nombre, email, version, password = self.obtenerDatosRegistrados()
        id_obtenido, server_id = self.peticionRemota.registrarUsuario(nombre,
            email, password, version)
        modulo_logger.log(logging.INFO, 'ID OBTENIDO: %s, server_id: %s' %
            (id_obtenido, server_id))
        if (int(id_obtenido) > 0):
            self.cursor.execute('update instalacion set id =?, serverid =?, '
                'passwordnotificada=1', (id_obtenido, server_id,))
            self.conexion_db.commit()
            modulo_logger.log(logging.INFO, 'Se registro correctamente la '
            'instalacion')
        else:
            modulo_logger.log(logging.ERROR, 'Hubo un error al tratar de '
            'registrarse remotamente')

    def eliminarRemotamente(self):
        """Ejecutado cuando un usuario desinstala el soft"""
        self.peticionRemota.eliminarUsuario()

    def obtenerDatosRegistrados(self):
        """Devuelve id, nombre, email y version"""
        try:
            userid, nombre, email, version, password = self.cursor.execute(
                'select id, nombretitular, email, version, password from '
                'instalacion'
                ).fetchone()
        except sqlite3.OperationalError, msg:
            modulo_logger.log(logging.ERROR, "No se pudieron obtener los datos"
            " locales de la instalacion. Tal vez no esta la base de datos "
            "instalada.\nError: %s" % msg)
            userid = 0
            nombre = ""
            email = ""
            version = ""
            password = ""
        return userid, nombre, email, version, password
