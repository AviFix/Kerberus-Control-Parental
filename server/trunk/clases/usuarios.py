#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Modulo encargado de manejar los usuarios"""

# Modulos externos
#import urllib2
#import httplib
import logging
#import time
#import re
import MySQLdb
import sys

# Modulos propios
sys.path.append('/home/mboscovich/proyectos/control_parental/server/conf')
sys.path.append('clases')

import config
import correo

modulo_logger = logging.getLogger('kerberus')

class Usuarios:

    def __init__(self):
        self.serverConfig = config.serverConfig()

    def usuarioRegistrado(self, user_id, server_id, email):
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        try:
            cursor.execute('select id from usuarios where id=%s \
                and server_id=%s and email=%s', (user_id, server_id, email))
            idUsuario = cursor.fetchone()
            conexion.close()
        except MySQLdb.Error, e:
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error %d: %s" % (e.args[0], e.args[1]))
            return False

        if idUsuario is not None:
            return True
        else:
            modulo_logger.log(logging.DEBUG,
                "Usuario No registrado: user_id:%s, server_id:%s, email:%s"
                % (user_id, server_id, email))
            return False

    def recordarPassword(self, user_id, server_id):
        email, password, nombre, idioma = self.obtenerDatos(user_id, server_id)
        enviodemail = correo.Correo()
        enviodemail.enviarCorreoRecordarPassword(email, password, nombre, idioma)
        modulo_logger.log(logging.INFO,
            "Recordando la Passwd al usuario user_id:%s, server_id:%s, "
            "email:%s" % (user_id, server_id, email))
        return 'Recordada'

    def registrarUsuario(self, nombre, email, password, version, ip="", idioma="es"):
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        try:
            cursor.execute('select IFNULL(max(id)+1,1) from usuarios where '
            'server_id=%s', (self.serverConfig.serverID,))
            nuevo_id = cursor.fetchone()[0]
            cursor.execute('insert into usuarios(nombre, email, password,'
            'version, ultima_ip, server_id, id, idioma) values '
            '(%s, %s, %s, %s, %s, %s, %s, %s)', (nombre, email, password,
            version, ip, self.serverConfig.serverID, nuevo_id, idioma))
            conexion.commit()

            cursor.execute('select count(*) from usuarios')
            cantidad_usuarios_registrados = cursor.fetchone()[0]

            conexion.close()
            id_del_usuario = nuevo_id
            modulo_logger.log(logging.INFO, "Se agrego el user_id: %s" %
                nuevo_id)
        except MySQLdb.Error, e:
            conexion.rollback()
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error al agregar un nuevo usuario: ERROR %d: %s" %
                (e.args[0], e.args[1]))
            id_del_usuario = False

        if id_del_usuario:
            enviodemail = correo.Correo()
            enviodemail.enviarCorreoBienvenida(email, nombre, password, idioma)
            enviodemail.notificarNuevoUsuario(cantidad_usuarios_registrados,
                nombre, email, ip)
            modulo_logger.log(logging.INFO,
                "Nuevo usuario en este nodo user_id: %s" % id_del_usuario)
            return id_del_usuario
        else:
            return 0

    def registrarNuevaPassword(self, user_id, server_id, password_vieja,
        password_nueva):
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        try:
            cursor.execute("update usuarios set password = %s where id=%s and "
                "server_id=%s and md5(password)=%s", (password_nueva, user_id,
                server_id, password_vieja,))
            conexion.commit()
            conexion.close()
        except MySQLdb.Error, e:
            conexion.rollback()
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error al registrar nueva password: ERROR %d: %s" %
                (e.args[0], e.args[1]))
            return 'No informada'

        respuesta = self.obtenerDatos(user_id, server_id)

        if respuesta is not None:
            email, password, nombre, idioma = respuesta
            enviodemail = correo.Correo()
            enviodemail.enviarCorreoNuevaPassword(email, password, nombre, idioma)
            return 'Informada'
        return 'No informada'

    def obtenerDatos(self, user_id, server_id):
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        print "Obteniendo datos de UserID:%s, ServerID:%s" % (user_id,server_id)
        try:
            cursor.execute("select email, password, nombre, idioma from usuarios "
            "where id=%s and server_id=%s", (user_id, server_id))
            email, password, nombre, idioma = cursor.fetchone()
            conexion.close()
        except MySQLdb.Error, e:
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error al obtener datos: ERROR %d: %s" %
                (e.args[0], e.args[1]))
            return None
        return email, password, nombre, idioma

    def eliminarUsuario(self, user_id, server_id):
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        try:
            cursor.execute("delete from usuarios where id=%s and server_id=%s",
            (user_id, server_id))
            conexion.commit()
            cursor.execute('select count(*) from usuarios')
            cantidad_usuarios_registrados = cursor.fetchone()[0]
            conexion.close()
            enviodemail = correo.Correo()
            enviodemail.notificarBajaUsuario(cantidad_usuarios_registrados)
            modulo_logger.log(logging.INFO,
                "Se elimino el usuario user_id: %s, "
                "server_id: %s" % (user_id, server_id))
            return True
        except MySQLdb.Error, e:
            conexion.rollback()
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error al eliminar un usuario: ERROR %d: %s" %
                (e.args[0], e.args[1]))
            return False
