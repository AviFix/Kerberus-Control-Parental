# -*- coding: utf-8 *-*
"""Modulo encargado de obtener la lista de servidores activos"""

#Modulos externos
import socket
import sys
import urllib2
import time


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
        self.listaDeServidores = []
        for i in range(1, 100):
            ip_new = "validador%s.kerberus.com.ar" % i
            port_new = 443
            server = [ip_new, port_new]
            self.listaDeServidores.append(server)

    def estaRespondiendo(self, ip, port, userid, serverid):
        server = "http://%s:%s" % (ip, port)
        headers = {"UserID": userid, "ServerID": serverid,
        "Peticion": "estaRespondiendo"}

        if config.USAR_PROXY:
            if self.estaOnline(config.PROXY_IP, config.PROXY_PORT):
                url_proxy = "http://%s:%s" % \
                            (config.PROXY_IP, config.PROXY_PORT)
                modulo_logger.log(logging.DEBUG, "Conectando a %s, por medio "\
                "del proxy %s , para realizar la solicitud: %s" % \
                (server, url_proxy, headers['Peticion']))
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
        try:
            req = urllib2.Request(server, headers=headers)
            respuesta = urllib2.urlopen(req, timeout=5).read()
            modulo_logger.log(logging.DEBUG, "Respuesta: %s" % respuesta)
            return (respuesta == 'Online')
        except urllib2.URLError as error:
            modulo_logger.log(logging.ERROR, "Error al conectarse a %s, "\
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
            modulo_logger.log(logging.ERROR, "No hay conexion a %s:%s" % \
            (ip, port,))
            return False

    def obtenerServidor(self, ip=False, port=False, userID=1, serverID=-1):
        servers = [[ip, port]] + self.listaDeServidores
        dormir_por = 5
        while True:
            for ip, port in servers:
                if self.estaRespondiendo(ip, port, userID, serverID):
                    modulo_logger.log(logging.INFO, "Utilizando el servidor "\
                    "de validacion %s:%s" % (ip, port,))
                    return ip, port
                else:
                    modulo_logger.log(logging.INFO, "El servidor de "\
                    "validacion %s:%s no responde" % (ip, port,))

            modulo_logger.log(logging.CRITICAL, "No se pudo obtener ningun"\
            " servidor de validacion!, durmiendo por: %s" % dormir_por)
            time.sleep(dormir_por)
            dormir_por = dormir_por + 5
            if dormir_por > 30:
                dormir_por = 30
        return False, False
