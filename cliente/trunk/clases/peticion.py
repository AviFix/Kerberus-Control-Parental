# -*- coding: utf-8 -*-
#
"""Modulo encargado del dialogo con el server remoto"""

# Modulos externos
import sys
import urllib2
import sqlite3

# Modulos propios
sys.path.append('../conf')
sys.path.append('../')
import servidores
import config

#import registrar
import logging

modulo_logger = logging.getLogger('kerberus')


# Clase
class Peticion:
    def __init__(self):
        self.servidor = servidores.Servidor()
        self.userid, self.serverid, self.version, self.nombretitular = \
            self.obtenerDatos()
        self.server_ip, self.server_port = self.servidor.obtenerServidor(\
            config.SYNC_SERVER_IP, config.SYNC_SERVER_PORT, self.userid)
        self.server_sync = "%s:%s" % (self.server_ip, self.server_port)

    def obtenerDatos(self):
        try:
            conexion_db = sqlite3.connect(config.PATH_DB)
            cursor = conexion_db.cursor()
            idUsuario, serverId, version, nombretitular = \
                cursor.execute('select id, serverid, version, nombretitular '\
                'from instalacion').fetchone()
            cursor.close()
            return idUsuario, serverId, version, nombretitular
        except sqlite3.OperationalError, msg:
            modulo_logger.log(logging.ERROR, "No se pudo obtener el id de "\
            "instalacion.\nError: %s" % msg)
            idUsuario = 0
            version = 0
            nombretitular = ''
            serverId = 0
            return idUsuario, serverId, version, nombretitular

    def obtenerRespuesta(self, headers):
        #FIXME: Si no obtiene respuesta, deberia buscar otro server
        if config.USAR_PROXY:
            if self.servidor.estaOnline(config.PROXY_IP, config.PROXY_PORT):
                url_proxy = "http://%s:%s" % (config.PROXY_IP,
                            config.PROXY_PORT)
                modulo_logger.log(logging.DEBUG, "Conectando a %s, por medio "\
                "del proxy %s , para realizar la solicitud: %s" % \
                (self.server_sync, url_proxy, headers['Peticion']))
                proxy = {'http': url_proxy, 'https': url_proxy}
            else:
                modulo_logger.log(logging.ERROR, "El proxy no esta escuchando"\
                " en %s:%s por lo que no se utilizara" % \
                (config.PROXY_IP, config.PROXY_PORT,))
                proxy = {}
        else:
            proxy = {}
        proxy_handler = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        modulo_logger.log(logging.DEBUG, "Conectando a %s para realizar la "\
        "solicitud: %s" % (self.server_sync, headers['Peticion']))
#        dormir_por = 1

        # Agrego los datos particulares del cliente
        headers['UserID'] = self.userid
        headers['ServerID'] = self.serverid
        headers['Version'] = self.version
        headers['Nombre'] = urllib2.quote(self.nombretitular.encode('utf-8'))
        while True:
            try:
                if self.servidor.estaOnline(self.server_ip, self.server_port):
                    req = urllib2.Request("http://" + self.server_sync, \
                    headers=headers)
                    timeout = 120
                    respuesta = urllib2.urlopen(req, timeout=timeout).read()
                    modulo_logger.log(logging.DEBUG,
                                        "Respuesta: %s" % respuesta)
                    return respuesta
            except urllib2.URLError as error:
                modulo_logger.log(logging.ERROR, "Error al conectarse a %s, "\
                "peticion: %s . ERROR: %s" % (self.server_sync, \
                headers['Peticion'], error))
                self.server_ip, self.server_port = \
                    self.servidor.obtenerServidor(self.server_ip, \
                    self.server_ip, self.userid)
                self.server_sync = "%s:%s" % (self.server_ip, self.server_port)
                modulo_logger.log(logging.INFO, "Se cambia al servidor "\
                "%(server)s " % self.server_sync)

    def chequearActualizaciones(self):
        headers = {"Peticion": "chequearActualizaciones", "Plataforma": \
        config.PLATAFORMA}
        respuesta = self.obtenerRespuesta(headers)
        actualizacion, md5sum = respuesta.split(',')
        if actualizacion == 'No':
            return None, None
        else:
            return actualizacion, md5sum

    def obtenerDominiosPermitidos(self, ultima_actualizacion):
        headers = {"Peticion": "obtenerDominiosPermitidos", "UltimaSync": \
        str(ultima_actualizacion)}
        dominios = self.obtenerRespuesta(headers)
        return dominios

    def informarNuevaPassword(self, password):
        # FIXME: Deberia enviar la password vieja y nueva para verificar que
        # sea el usuario quien solicito el cambio
        password = urllib2.quote(password.encode('utf8'), safe='/')
        headers = {"UserID": self.userid,
                    "Peticion": "informarNuevaPassword",
                    "Password": password}
        respuesta = self.obtenerRespuesta(headers)
        return respuesta

    def recordarPassword(self):
        headers = {"Peticion": "recordarPassword"}
        respuesta = self.obtenerRespuesta(headers)
        return respuesta

    def obtenerDominiosDenegados(self, ultima_actualizacion):
        headers = {"Peticion": "obtenerDominiosDenegados",
                    "UltimaSync": str(ultima_actualizacion)}
        dominios = self.obtenerRespuesta(headers)
        return dominios

    def obtenerPeriodoDeActualizacion(self):
        """Obtiene el periodo de actualizacion. Devuelve en segundos"""
        headers = {"Peticion": "getPeriodoDeActualizacion"}
        respuesta = self.obtenerRespuesta(headers)
        if not respuesta:
            respuesta = 1
        respuesta_en_segs = int(respuesta) * 60
        return respuesta_en_segs

    def obtenerPeriodoDeRecargaCompleta(self):
        """Obtiene el periodo de recarga completa. Devuelve en segundos"""
        headers = {"Peticion": "getPeriodoDeRecargaCompleta"}
        respuesta = self.obtenerRespuesta(headers)
        if not respuesta:
            respuesta = 1
        respuesta_en_segs = int(respuesta) * 60
        return respuesta_en_segs

    def obtenerHoraServidor(self):
        """Obtiene la hora del servidor. Devuelve en segundos"""
        headers = {"Peticion": "getHoraServidor"}
        respuesta = self.obtenerRespuesta(headers)
        return respuesta

    def registrarUsuario(self, nombre, email, password, version):
        """Devuelve el id si registra, sino devuelve 0"""
        nombre = urllib2.quote(nombre.encode('utf8'), safe='/')
        email = urllib2.quote(email.encode('utf8'), safe='/')
        password = urllib2.quote(password.encode('utf8'), safe='/')
        version = urllib2.quote(version.encode('utf8'), safe='/')
        headers = {"Peticion": "registrarUsuario", "Email": email,
                    "Password": password, "ServerID": '0'}
        respuesta = self.obtenerRespuesta(headers)
        modulo_logger.log(logging.DEBUG, "Id de usuario y  Id server: %s" % \
                            respuesta)
        idUsuario, server_id = respuesta.split(',')
        return [idUsuario, server_id]

    def eliminarUsuario(self, id):
        """Solicita la eliminacion"""
        headers = {"Peticion": "eliminarUsuario"}
        respuesta = self.obtenerRespuesta(headers)
        return respuesta

    def usuarioRegistrado(self, id, email):
        #FIXME: Debe enviar id y email para verificar
        """Devuelve true o false"""
        headers = {"Peticion": "usuarioRegistrado", "ID": id, "Email": email}
        respuesta = self.obtenerRespuesta(headers)
        return respuesta

    def validarUrl(self, url):
        """Devuelve true o false, segun la url se permita o no.
        En caso de que no se permita, devuelve a su vez el motivo de porque no
        se permite."""
        headers = {"Peticion": "validarUrl", "URL": url}
        respuesta = self.obtenerRespuesta(headers)
        if respuesta == "":
            modulo_logger.log(logging.INFO,
                                "URL validada remotamente: %s" % url)
            return True, ""
        else:
            modulo_logger.log(logging.INFO,
                                "URL denegada remotamente: %s" % url)
            modulo_logger.log(logging.INFO, "Motivo: %s" % respuesta)
            return False, respuesta
