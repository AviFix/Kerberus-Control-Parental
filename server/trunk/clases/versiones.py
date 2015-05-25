#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Modulo encargado de retornar la url a versiones mas recientes de los
clientes"""

# Modulos externos
import MySQLdb
import sys
import logging

# Modulos propios
sys.path.append('/home/mboscovich/proyectos/control_parental/server/conf')
sys.path.append('clases')

import config

modulo_logger = logging.getLogger('Kerberus')


class Versiones:

    def __init__(self):
        self.serverConfig = config.serverConfig()

    def obtenerVersion(self, version_desde, plataforma):
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name)
        cursor = conexion.cursor()
        try:
            cursor.execute('select URL_actualizador, md5sum_actualizador from \
            versiones_cliente where version_desde=%s and plataforma=%s', \
            (version_desde, plataforma))
            row = cursor.fetchone()
            conexion.close()
        except MySQLdb.Error, e:
            conexion.close()
            modulo_logger.log(logging.ERROR,
                "Error al obtener la version: ERROR %d: %s" % \
                (e.args[0], e.args[1]))
            return "No", "No"
        if row:
            url = row[0]
            md5sum = row[1]
            return url, md5sum
        else:
            return "No", "No"
