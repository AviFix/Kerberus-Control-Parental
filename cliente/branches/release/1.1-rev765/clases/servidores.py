# -*- coding: utf-8 *-*
"""Modulo encargado de obtener la lista de servidores activos"""

#Modulos externos
import socket
import sys
import urllib2
import time
import sqlite3

#Modulos propios
sys.path.append('../conf')
import config
import logging

modulo_logger = logging.getLogger('kerberus')


#Excepciones
class ServidorError(Exception):

    def __init__(self):
        super(ServidorError, self).__init__()
        pass


# Clase
class Servidor:

    def __init__(self):
        # Los servidores default son aquellos que no son obtenidos desde
        # un server real por medio de una peticion.
        self.listaDeServidoresDefault = []

        # Este es el servidor seteado en el archivo de configuracion
        servidor_config = [config.SERVER_IP, config.SERVER_PORT]
        self.listaDeServidoresDefault.append(servidor_config)

        for i in range(1, 100):
            ip_new = "validador%s.kerberus.com.ar" % i
            port_new = 80
            server = [ip_new, port_new]
            self.listaDeServidoresDefault.append(server)

        # Me conecto para descargar la lista de servidores
        self.obtenerRankingServidores()

    def obtenerDatosUsuario(self):
        try:
            conexion_db = sqlite3.connect(config.PATH_DB)
            cursor = conexion_db.cursor()
            idUsuario, serverId, version, nombretitular, credencial = \
                cursor.execute('select id, serverid, version, nombretitular '
                ', credencial from instalacion').fetchone()
            cursor.close()

            return idUsuario, serverId, version, nombretitular, credencial

        except sqlite3.OperationalError, msg:
            modulo_logger.log(logging.ERROR, "No se pudo obtener el id de "
            "instalacion.\nError: %s" % msg)
            idUsuario = 0
            version = 0
            nombretitular = ''
            serverId = 0
            credencial = ''
            return idUsuario, serverId, version, nombretitular, credencial

    def obtenerRankingServidores(self):
        headers = {}
        headers['Peticion'] = "obtenerServidores"

        if config.USAR_PROXY:
            if self.estaOnline(config.PROXY_IP, config.PROXY_PORT):
                url_proxy = "http://%s:%s" % (config.PROXY_IP,
                    config.PROXY_PORT)
                proxy = {'http': url_proxy, 'https': url_proxy}
            else:
                modulo_logger.log(logging.ERROR, "El proxy no esta escuchando"
                " en %s:%s por lo que no se utilizara" %
                (config.PROXY_IP, config.PROXY_PORT,))
                proxy = {}
        else:
            proxy = {}
        proxy_handler = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)

        # Agrego los datos particulares del cliente
        userid, serverid, version, nombretitular, credencial = \
            self.obtenerDatosUsuario()
        headers['UserID'] = userid
        headers['ServerID'] = serverid
        headers['Version'] = version
        headers['Credencial'] = credencial
        headers['Nombre'] = urllib2.quote(nombretitular.encode('utf-8'))

        # Esto es para que en el caso de que no pueda descargar la lista de
        # servidores, utilice los servidores default (por ejemplo antes de
        # registrarse).
        self.listaDeServidores = self.listaDeServidoresDefault

        for ip, puerto in self.listaDeServidoresDefault:
            if self.estaOnline(ip, puerto):
                servidor = "https://%s:%s" % (ip, puerto)
                try:
                    req = urllib2.Request(servidor, headers=headers)
                    timeout = 40
                    respuesta = urllib2.urlopen(req, timeout=timeout).read()
                    modulo_logger.log(logging.DEBUG,
                                        "Respuesta: %s" % respuesta)
                    if respuesta:
                        # Respuesta es una lista separada por retorno de carro
                        # de la forma IP:PUERTO
                        self.listaDeServidores = []
                        for servidor in respuesta.split('\n'):
                            if ":" in servidor:
                                ip, puerto = servidor.split(":")
                                self.listaDeServidores.append([ip, puerto])
                        modulo_logger.log(logging.DEBUG, "Se obtuvo "
                        "correctamente la lista de servidores disponibles.\n"
                        "Lista de Servidores:\n"
                        "%s" % respuesta)
                        break
                    else:
                        modulo_logger.log(logging.DEBUG, "No se obtuvo "
                        "la lista de servidores disponibles!!!.\n")

                except urllib2.URLError as error:
                    modulo_logger.log(logging.ERROR, "Error al conectarse a %s"
                    ", peticion: %s . ERROR: %s" % (servidor,
                    headers['Peticion'], error))

    def estaRespondiendo(self, ip, port, userid, serverid):
        if not userid and serverid:
            userid, serverid, version, nombretitular, credencial = \
            self.obtenerDatosUsuario()

        server = "https://%s:%s" % (ip, port)
        headers = {"UserID": userid, "ServerID": serverid,
        "Peticion": "estaRespondiendo"}

        if config.USAR_PROXY:
            if self.estaOnline(config.PROXY_IP, config.PROXY_PORT):
                url_proxy = "http://%s:%s" % \
                            (config.PROXY_IP, config.PROXY_PORT)
                modulo_logger.log(logging.DEBUG, "Conectando a %s, por medio "
                "del proxy %s , para realizar la solicitud: %s" %
                (server, url_proxy, headers['Peticion']))
                proxy = {'http': url_proxy, 'https': url_proxy}
            else:
                modulo_logger.log(logging.ERROR, "El proxy no esta escuchando"
                " en %s:%s por lo que no se utilizara" %
                (config.PROXY_IP, config.PROXY_PORT,))
                proxy = {}
        else:
            proxy = {}
        proxy_handler = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        try:
            req = urllib2.Request(server, headers=headers)
            respuesta = urllib2.urlopen(req, timeout=5).read()
            modulo_logger.log(logging.DEBUG, "Respuesta: %s" % respuesta)
            return (respuesta == 'Online')
        except urllib2.URLError as error:
            modulo_logger.log(logging.ERROR, "Error al conectarse a %s, "
            "peticion: %s . ERROR: %s" % (server, headers['Peticion'], error))
            return False

    def estaOnline(self, ip, port):
        """Verifica si el puerto esta abierto. Util para chequear el
        proxy nomas"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        try:
            s.connect((ip, int(port)))
            s.shutdown(2)
            return True
        except:
            modulo_logger.log(logging.ERROR, "No hay conexion a %s:%s" %
            (ip, port,))
            return False

    def obtenerServidor(self, ip=False, port=False, userID=False,
    serverID=False):
        dormir_por = 5
        while True:
            for ip, port in self.listaDeServidores:
                if self.estaRespondiendo(ip, port, userID, serverID):
                    modulo_logger.log(logging.INFO, "Utilizando el servidor "
                    "de validacion %s:%s" % (ip, port,))
                    return ip, port
                else:
                    modulo_logger.log(logging.INFO, "El servidor de "
                    "validacion %s:%s no responde" % (ip, port,))

            modulo_logger.log(logging.CRITICAL, "No se pudo obtener ningun"
            " servidor de validacion!, durmiendo por: %s" % dormir_por)
            time.sleep(dormir_por)
            dormir_por = dormir_por + 5
            if dormir_por > 30:
                dormir_por = 30
        return False, False
