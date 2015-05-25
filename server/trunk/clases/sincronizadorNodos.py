#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Modulo encargado de manejar las urls"""

# Modulos externos
import urllib2
import MySQLdb
import sys
import hashlib

# Modulos propios
sys.path.append('/home/mboscovich/proyectos/control_parental/server/conf')
import cluster
import config
import logging


modulo_logger = logging.getLogger('Kerberus-cluster')


class SincronizadorNodos:

    def __init__(self, configuracion=''):
        if configuracion == '':
            self.config = config.sincronizadorConfig()
        else:
            self.config = configuracion
        self.cluster = cluster.Cluster()

    def obtenerRespuesta(self, headers, server):
        proxy = {}
        proxy_handler = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        # FIXME: Deberia sacarlo de la base de datos
        credencial = hashlib.md5('k3rb3r4sk3rb3r4s').hexdigest()
        headers['Credencial'] = credencial
        modulo_logger.log(logging.DEBUG, "Headers enviados: %s" % headers)
        req = urllib2.Request(server, headers=headers)
        timeout = 10
        try:
            respuesta = urllib2.urlopen(req, timeout=timeout).read()
        except:
            modulo_logger.log(logging.DEBUG,
                "Error en conectarse a %s" % server)
            respuesta = "Fallo"

        return respuesta

    def informarCambios(self):
        modulo_logger.log(logging.DEBUG,
            "Chequeando si existen cambios a informar")
        self.reportarBajasDeUsuarios()
        self.reportarCambiosDePassword()
        self.reportarNuevosUsuarios()

    def recargarConfig(self, config):
        self.config = config

    def cambioDePasswordInformado(self, nodo, user_id, server_id):
        conexion = MySQLdb.connect(host=self.config.db_host,
                                    user=self.config.db_user,
                                    passwd=self.config.db_password,
                                    db=self.config.db_name)
        cursor = conexion.cursor()
        try:
            cursor.execute("delete from informar_cambios_de_password where "\
            "nodo=%s and user_id=%s and server_id=%s",
                (nodo, user_id, server_id,))
            conexion.commit()
            conexion.close()
        except MySQLdb.Error, e:
            conexion.rollback()
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error en cambioDePasswordInformado: ERROR %d: %s" % \
                (e.args[0], e.args[1]))

    def nuevoUsuarioInformado(self, nodo, user_id, server_id):
        conexion = MySQLdb.connect(host=self.config.db_host,
                                    user=self.config.db_user,
                                    passwd=self.config.db_password,
                                    db=self.config.db_name)
        cursor = conexion.cursor()
        try:
            cursor.execute("delete from informar_nuevo_usuario where "\
            "nodo=%s and user_id=%s and server_id=%s",
                (nodo, user_id, server_id,))
            conexion.commit()
            conexion.close()
        except MySQLdb.Error, e:
            conexion.rollback()
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error en nuevoUsuarioInformado: ERROR %d: %s" % \
                (e.args[0], e.args[1]))

    def bajaUsuarioInformada(self, nodo, user_id, server_id):
        conexion = MySQLdb.connect(host=self.config.db_host,
                                    user=self.config.db_user,
                                    passwd=self.config.db_password,
                                    db=self.config.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        try:
            cursor.execute("delete from informar_baja_usuario where "\
            "nodo=%s and user_id=%s and server_id=%s",
                (nodo, user_id, server_id,))
            conexion.commit()
            conexion.close()
        except MySQLdb.Error, e:
            conexion.rollback()
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error en bajaUsuarioInformada: ERROR %d: %s" % \
                (e.args[0], e.args[1]))

    def reportarCambiosDePassword(self):
        conexion = MySQLdb.connect(host=self.config.db_host,
                                    user=self.config.db_user,
                                    passwd=self.config.db_password,
                                    db=self.config.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        try:
            cursor.execute('select nodo, user_id, server_id, nuevaPassword '\
            'from informar_cambios_de_password')
            respuesta = cursor.fetchall()
            conexion.close()
        except MySQLdb.Error, e:
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error en reportarCambiosDePassword: ERROR %d: %s" % \
                (e.args[0], e.args[1]))
            respuesta = None

        if respuesta:
            manejadorCluster = cluster.Cluster()
            for fila in respuesta:
                nodo, user_id, server_id, password = fila
                password = urllib2.quote(password.encode('utf8'), safe='/')
                modulo_logger.log(logging.INFO,
                    "Informando cambio de password a %s,  el user_id: %s, "\
                    "server_id: %s, password: %s " % (nodo, user_id, server_id,
                                                    password))
                ip, puerto = manejadorCluster.obtenerDatosNodo(nodo)
                server = "http://%s:%s" % (ip, puerto)
                modulo_logger.log(logging.DEBUG, "Conectando a %s" % server)
                headers = {
                            "Peticion": "cambioDePassword",
                            "UserID": int(user_id),
                            "ServerID": int(server_id),
                            "NuevaPassword": password
                            }
                respuesta = self.obtenerRespuesta(headers, server)
                modulo_logger.log(logging.DEBUG,
                    "Respuesta obtenida: %s" % respuesta)
                if respuesta == 'OK':
                    self.cambioDePasswordInformado(nodo, user_id, server_id)
        else:
            modulo_logger.log(logging.INFO,
                "No hay cambios de password para informar")

    def reportarNuevosUsuarios(self):
        conexion = MySQLdb.connect(host=self.config.db_host,
                                    user=self.config.db_user,
                                    passwd=self.config.db_password,
                                    db=self.config.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        try:
            cursor.execute("select nodo, server_id, user_id, ip, nombre, "\
            "email, password, version, idioma from informar_nuevo_usuario")
            respuesta = cursor.fetchall()
            conexion.close()
        except MySQLdb.Error, e:
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error en reportarNuevosUsuarios: ERROR %d: %s" % \
                (e.args[0], e.args[1]))
            respuesta = None

        if respuesta:
            manejadorCluster = cluster.Cluster()
            for fila in respuesta:
                nodo, server_id, user_id, ip_cliente, nombre, email, password,\
                version, idioma = fila
                nombre = urllib2.quote(nombre.encode('utf8'), safe='/')
                password = urllib2.quote(password.encode('utf8'), safe='/')
                email = urllib2.quote(email.encode('utf8'), safe='/')
                modulo_logger.log(logging.INFO,
                    "Informando nuevo usuario a %s,  el user_id: %s, "\
                    "server_id: %s" % (nodo, user_id, server_id))
                ip, puerto = manejadorCluster.obtenerDatosNodo(nodo)
                server = "http://%s:%s" % (ip, puerto)
                modulo_logger.log(logging.DEBUG, "Conectando a %s" % server)
                headers = {
                            "Peticion": "nuevoUsuario",
                            "UserID": int(user_id),
                            "ServerID": int(server_id),
                            "UltimaIp": ip_cliente,
                            "Nombre": nombre,
                            "Email": email,
                            "Password": password,
                            "Version": version,
                            "Idioma": idioma
                            }
                respuesta = self.obtenerRespuesta(headers, server)
                if respuesta == 'OK':
                    self.nuevoUsuarioInformado(nodo, user_id, server_id)
                modulo_logger.log(logging.DEBUG,
                    "Respuesta obtenida: %s" % respuesta)
        else:
            modulo_logger.log(logging.DEBUG,
                "No hay nuevos usuarios para informar")

    def reportarBajasDeUsuarios(self):
        conexion = MySQLdb.connect(host=self.config.db_host,
                                    user=self.config.db_user,
                                    passwd=self.config.db_password,
                                    db=self.config.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        try:
            cursor.execute("select nodo, server_id, user_id from "\
            "informar_baja_usuario")
            respuesta = cursor.fetchall()
            conexion.close()
        except MySQLdb.Error, e:
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error en reportarBajasDeUsuarios: ERROR %d: %s" % \
                (e.args[0], e.args[1]))
            respuesta = None

        if respuesta:
            manejadorCluster = cluster.Cluster()
            for fila in respuesta:
                nodo, server_id, user_id = fila
                modulo_logger.log(logging.INFO,
                    "Informando nueva baja de usuario a %s" % (nodo))
                ip, puerto = manejadorCluster.obtenerDatosNodo(nodo)
                server = "http://%s:%s" % (ip, puerto)
                logging.log(logging.DEBUG, "Conectando a %s" % server)
                headers = {
                            "Peticion": "bajaUsuario",
                            "UserID": int(user_id),
                            "ServerID": int(server_id),
                            }
                respuesta = self.obtenerRespuesta(headers, server)
                if respuesta == 'OK':
                    self.bajaUsuarioInformada(nodo, user_id, server_id)
                logging.log(logging.DEBUG, "Respuesta obtenida: %s" % respuesta)
        else:
            logging.log(logging.DEBUG, "No hay bajas de usuario para informar")

    def acentarCambioDePassword(self, user_id, server_id, password):
        conexion = MySQLdb.connect(host=self.config.db_host,
                                    user=self.config.db_user,
                                    passwd=self.config.db_password,
                                    db=self.config.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        password = unicode(urllib2.unquote(password), 'utf-8')
        try:
            cursor.execute("update usuarios set password=%s where id=%s and "\
            "server_id=%s", (password, user_id, server_id))
            conexion.commit()
            conexion.close()
        except MySQLdb.Error, e:
            conexion.rollback()
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error en acentarCambioDePassword: ERROR %d: %s" % \
                (e.args[0], e.args[1]))
            return "Fallo"
        return "OK"

    def acentarNuevoUsuario(self, user_id, server_id, ip, nombre, email,
                            password, version, idioma):
        conexion = MySQLdb.connect(host=self.config.db_host,
                                    user=self.config.db_user,
                                    passwd=self.config.db_password,
                                    db=self.config.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()

        nombre = unicode(urllib2.unquote(nombre), 'utf-8')
        email = unicode(urllib2.unquote(email), 'utf-8')
        password = unicode(urllib2.unquote(password), 'utf-8')
        try:
            cursor.execute("insert into usuarios(id, server_id, email, "\
            "ultima_ip, password, nombre, version, idioma) values "\
            "(%s, %s, %s, %s, %s, %s , %s, %s)", (user_id, server_id, email,
            ip, password, nombre, version, idioma)
            )
            conexion.commit()
            conexion.close()
        except MySQLdb.Error, e:
            conexion.rollback()
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error en acentarNuevoUsuario: ERROR %d: %s" % \
                (e.args[0], e.args[1]))
            return "Fallo"
        return "OK"

    def acentarBajaUsuario(self, user_id, server_id):
        conexion = MySQLdb.connect(host=self.config.db_host,
                                    user=self.config.db_user,
                                    passwd=self.config.db_password,
                                    db=self.config.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        try:
            cursor.execute("delete from usuarios where id = %s and "\
            "server_id = %s", (user_id, server_id))
            conexion.commit()
            conexion.close()
        except MySQLdb.Error, e:
            conexion.rollback()
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error en acentarBajaUsuario: ERROR %d: %s" % \
                (e.args[0], e.args[1]))
            return "Fallo"
        return "OK"
