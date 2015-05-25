#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Modulo encargado de la comunicacion entre los servidores"""

# Modulos externos
import sys
import MySQLdb

# Modulos propios
sys.path.append(
    '/srv/kerberus/conf')
import config
import logging

modulo_logger = logging.getLogger('Kerberus')


class Cluster:

    def __init__(self):
        self.Configuracion = config.serverConfig()

    def registrarCambioDePassword(self, user_id, server_id, password):
        conexion = MySQLdb.connect(host=self.Configuracion.db_host,
                                    user=self.Configuracion.db_user,
                                    passwd=self.Configuracion.db_password,
                                    db=self.Configuracion.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        for nodo in self.obtenerNodos():
            id_nodo = nodo[0]
            try:
                cursor.execute('insert into informar_cambios_de_password(nodo,'\
                ' user_id, server_id, nuevaPassword) values (%s,%s,%s,%s)',
                (id_nodo, user_id, server_id, password,))
            except:
                modulo_logger.log(logging.ERROR,
                    "ERROR al insertar un registro en la tabla informar_cambios_de_password")
            conexion.commit()
        conexion.close()

    def registrarNuevoUsuario(self, user_id, server_id, nombre, email,
                                password, version, ip, idioma):
        conexion = MySQLdb.connect(host=self.Configuracion.db_host,
                                    user=self.Configuracion.db_user,
                                    passwd=self.Configuracion.db_password,
                                    db=self.Configuracion.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        for nodo in self.obtenerNodos():
            id_nodo = nodo[0]
            try:
                cursor.execute('insert into informar_nuevo_usuario(nodo, '\
                'user_id, server_id, nombre, email, password, version, ip, idioma) '\
                'values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                (id_nodo, user_id, server_id, nombre, email, password,
                version, ip, idioma))
            except:
                modulo_logger.log(logging.ERROR,
                    "ERROR al insertar un registro en la tabla informar_nuevo_usuario")
            conexion.commit()
        conexion.close()

    def registrarBajaUsuario(self, user_id, server_id):
        conexion = MySQLdb.connect(host=self.Configuracion.db_host,
                                    user=self.Configuracion.db_user,
                                    passwd=self.Configuracion.db_password,
                                    db=self.Configuracion.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        for nodo in self.obtenerNodos():
            id_nodo = nodo[0]
            try:
                cursor.execute('insert into informar_baja_usuario(nodo, '\
                'user_id, server_id) values (%s,%s,%s)',
                (id_nodo, user_id, server_id,))
            except:
                modulo_logger.log(logging.ERROR,
                "ERROR al insertar un registro en la tabla informar_baja_usuario")
            conexion.commit()
        conexion.close()

    def obtenerNodos(self):
        conexion = MySQLdb.connect(host=self.Configuracion.db_host,
                                    user=self.Configuracion.db_user,
                                    passwd=self.Configuracion.db_password,
                                    db=self.Configuracion.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        cursor.execute('select id from servidores where id <> %s', \
        (self.Configuracion.serverID,))
        respuesta = cursor.fetchall()
        return respuesta

    def obtenerDatosNodo(self, id_nodo):
        conexion = MySQLdb.connect(host=self.Configuracion.db_host,
                                    user=self.Configuracion.db_user,
                                    passwd=self.Configuracion.db_password,
                                    db=self.Configuracion.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        cursor.execute('select ip, puerto from servidores where id=%s' \
        , (id_nodo,))
        respuesta = cursor.fetchone()
        return respuesta

    def obtenerRankingServidores(self):
        conexion = MySQLdb.connect(host=self.Configuracion.db_host,
                                    user=self.Configuracion.db_user,
                                    passwd=self.Configuracion.db_password,
                                    db=self.Configuracion.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        cursor.execute('select ip, puerto from ranking_servidores order by ranking')
        respuesta = cursor.fetchall()
        ranking = ""
        for servidor in respuesta:
            ip, puerto = servidor
            ranking += "%s:%s\n" % (ip, puerto)
        if ranking[-1] == "\n":
            ranking = ranking[0:-1]
        return ranking