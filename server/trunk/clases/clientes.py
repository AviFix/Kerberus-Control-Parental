#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Modulo encargado de autenticar a los clientes"""

# Modulos externos
import logging
import MySQLdb
import sys
import urllib2

# Modulos propios
sys.path.append('/home/mboscovich/proyectos/control_parental/server/conf')
import config

modulo_logger = logging.getLogger('Kerberus')


class Cliente:

    def __init__(self):
        self.serverConfig = config.serverConfig()

    def clienteValido(self, user_id, server_id, credencial):
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        try:
            cursor.execute("select md5(password) from usuarios "\
            "where id=%s and server_id=%s", (user_id, server_id))
            if cursor.rowcount > 0:
                credencial_server = cursor.fetchone()[0]
                # Comparo siendo quoteada la pass, no en plano
                respuesta = (credencial_server == credencial)
            else:
                respuesta = False
            conexion.close()
        except MySQLdb.Error, e:
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error al obtener datos: ERROR %d: %s" % \
                (e.args[0], e.args[1]))
            return False
        return respuesta

    def actualizarDatosCliente(self, user_id, server_id, version, ip_client,
                                credencial):
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        try:
            cursor.execute("update usuarios set ultima_ip=%s, version=%s "
                           "where id=%s and server_id=%s and md5(password)=%s",
                           (ip_client, version, user_id, server_id, credencial)
                           )
            conexion.commit()
            conexion.close()
        except MySQLdb.Error, e:
            conexion.rollback()
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error al actualizar los datos de un cliente: ERROR %d: %s" %
                (e.args[0], e.args[1]))
            return False
        return True

