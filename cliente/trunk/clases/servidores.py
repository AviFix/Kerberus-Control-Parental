# -*- coding: utf-8 *-*
"""Modulo encargado de obtener la lista de servidores activos"""

#Modulos externos
import socket
import sys
import urllib2
import time
import sqlite3
import logging

modulo_logger = logging.getLogger('kerberus.' + __name__)

sys.path.append('../conf')
sys.path.append('../')

#Modulos propios
import config


#Excepciones
class ServidorError(Exception):

    def __init__(self):
        super(ServidorError, self).__init__()
        pass


# Clase
class Servidor:

    def __init__(self):
        self.cargarServidoresFromDB()
        self.listaDeServidores = self.listaDeServidoresDB

    def cargarServidoresDefault(self):
        # Los servidores default son aquellos que no son obtenidos desde
        # un server real por medio de una peticion.
        self.listaDeServidoresDefault = []
        # Este es el servidor seteado en el archivo de configuracion
        self.listaDeServidoresDefault.append(
            [config.SERVER_IP, config.SERVER_PORT]
            )

        for i in range(1, 10):
            ip_new = "validador%s.kerberus.com.ar" % i
            server = [ip_new, 443]
            self.listaDeServidoresDefault.append(server)
            server = [ip_new, 80]
            self.listaDeServidoresDefault.append(server)

    def cargarServidoresFromDB(self):
        try:
            conexion_db = sqlite3.connect(config.PATH_DB)
            cursor = conexion_db.cursor()
            servidores = cursor.execute(
                'select ip, puerto from servidores order by ranking'
                ).fetchall()
            cursor.close()

            self.listaDeServidoresDB = []
            for servidor in servidores:
                ip, puerto = servidor
                self.listaDeServidoresDB.append([ip, puerto])
                modulo_logger.info('Cargando el servidor %s:%s desde la DB'
                % (ip, puerto))

        except sqlite3.OperationalError, msg:
            modulo_logger.error("No se pudo obtener la lista "
            "de servidores desde la base de datos.\nError: %s" % msg)

    def obtenerRankingServidores(self):
        # Obtengo los datos del usuario
        userid, serverid, version, nombretitular, credencial = \
            self.obtenerDatosUsuario()
        headers = {}
        modulo_logger.info('Iniciando solicitud de servidores online')
        headers['Peticion'] = "obtenerServidores"

        if config.USAR_PROXY:
            if self.estaOnline(config.PROXY_IP, config.PROXY_PORT):
                url_proxy = "http://%s:%s" % (config.PROXY_IP,
                    config.PROXY_PORT)
                proxy = {'http': url_proxy, 'https': url_proxy}
            else:
                modulo_logger.log(logging.ERROR,
                "El proxy no esta escuchando en %s:%s por lo que no se "
                "utilizara" % (config.PROXY_IP, config.PROXY_PORT,))
                proxy = {}
        else:
            proxy = {}
        proxy_handler = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)

        # Agrego los datos particulares del cliente
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
                if int(puerto) == 443:
                    protocolo = "https"
                else:
                    protocolo = "http"
                servidor = "%s://%s:%s" % (protocolo, ip, puerto)
                try:
                    req = urllib2.Request(servidor, headers=headers)
                    timeout = 40
                    respuesta = urllib2.urlopen(req, timeout=timeout).read()

                    if respuesta:
                        # Respuesta es una lista separada por retorno de
                        # carro de la forma IP:PUERTO
                        self.listaDeServidores = []
                        for servidor in respuesta.split('\n'):
                            if ":" in servidor:
                                ip, puerto = servidor.split(":")
                                self.listaDeServidores.append([ip, puerto])

                        # lo guardo en la base
                        try:
                            conexion_db = sqlite3.connect(config.PATH_DB)
                            cursor = conexion_db.cursor()
                            ranking = 0

                            cursor.execute('delete from servidores')
                            conexion_db.commit()

                            for servidor in self.listaDeServidores:
                                ranking += 1
                                cursor.execute(
                                    'insert into servidores values (?,?,?)',
                                    (ranking, servidor[0], servidor[1], ))
                                modulo_logger.info('Guardando en la DB el '
                                'servidor %s:%s - Ranking: %s' %
                                (servidor[0], servidor[1], ranking,))

                            conexion_db.commit()
                            conexion_db.close()
                        except sqlite3.OperationalError, msg:
                            modulo_logger.error(
                            "No se pudieron guardar los servidores en la "
                            "base de datos\nError: %s" % msg)

                        modulo_logger.debug(
                            "Se obtuvo correctamente la lista de servidores"
                            " disponibles.\nLista de Servidores:\n"
                            "%s" % respuesta)
                        # Salgo del for sobre dominios default
                        break
                    else:
                        modulo_logger.error(
                            "No se obtuvo se pudo obtener la lista de "
                            "servidores kerberus disponibles.")

                except urllib2.URLError as error:
                    modulo_logger.error(
                    "Error al conectarse a %s, peticion: %s . ERROR: %s"
                    % (servidor, headers['Peticion'], error))
            else:
                # Como no responde lo elimino de la lista de defaults
                self.listaDeServidoresDefault.remove([ip, puerto])

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
            modulo_logger.error("No se pudo obtener el id de "
            "instalacion.\nError: %s" % msg)
            idUsuario = 0
            version = 0
            nombretitular = ''
            serverId = 0
            credencial = ''
            return idUsuario, serverId, version, nombretitular, credencial


    def estaRespondiendo(self, ip, port, userid, serverid):
        if not userid and serverid:
            userid, serverid, version, nombretitular, credencial = \
            self.obtenerDatosUsuario()
        if int(port) == 443:
            protocolo = "https"
        else:
            protocolo = "http"
        server = "%s://%s:%s" % (protocolo, ip, port)
        modulo_logger.debug("Verificando si esta respondiendo %s"
        % (server))
        headers = {"UserID": userid, "ServerID": serverid,
        "Peticion": "estaRespondiendo"}

        if config.USAR_PROXY:
            if self.estaOnline(config.PROXY_IP, config.PROXY_PORT):
                url_proxy = "http://%s:%s" % \
                            (config.PROXY_IP, config.PROXY_PORT)
                modulo_logger.debug("Conectando a %s, por medio "
                "del proxy %s , para realizar la solicitud: %s" %
                (server, url_proxy, headers['Peticion']))
                proxy = {'http': url_proxy, 'https': url_proxy}
            else:
                modulo_logger.error("El proxy no esta escuchando"
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
            respuesta = urllib2.urlopen(req, timeout=15).read()
            modulo_logger.debug("Respuesta: %s" % respuesta)
            return (respuesta == 'Online')
        except urllib2.URLError as error:
            modulo_logger.error("Error al conectarse a %s, "
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
            modulo_logger.error("No hay conexion a %s:%s" %
            (ip, port,))
            return False

    def obtenerServidor(self, ip=False, port=False, userID=False,
    serverID=False):
        dormir_por = 0

        while True:

            servidores_str = ''
            for ip, puerto in self.listaDeServidores:
                servidores_str += '\n - %s:%s ' % (ip, puerto)

            modulo_logger.debug(
                "Lista de servidores a utilizar: %s" % servidores_str)

            for ip, port in self.listaDeServidores:
                if self.estaRespondiendo(ip, port, userID, serverID):
                    modulo_logger.info("Utilizando el servidor "
                    "de validacion %s:%s" % (ip, port,))
                    return ip, port
                else:
                    self.listaDeServidores.remove([ip, port])
                    modulo_logger.info("El servidor de "
                    "validacion %s:%s no responde" % (ip, port,))

            modulo_logger.critical("No se pudo obtener ningun"
            " servidor de validacion!, probando servidores default...")
            self.cargarServidoresDefault()

            # trato de obtener la lista de servidores remotamente
            self.obtenerRankingServidores()

            modulo_logger.critical("No se pudo obtener ningun"
            " servidor de validacion!, durmiendo por: %s" % dormir_por)

            time.sleep(dormir_por)
            dormir_por += 5
            if dormir_por > 30:
                dormir_por = 30
        return False, False
