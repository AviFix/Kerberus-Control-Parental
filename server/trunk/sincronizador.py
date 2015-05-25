#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Modulo encargado de levantar el servidor"""

__version__ = "0.1"

#Modulos externos
import BaseHTTPServer
import SocketServer
import sys
import logging.handlers
import time
import threading
import select
import signal
import hashlib
from types import FrameType, CodeType


# Modulos propios
sys.path.append('clases')
sys.path.append('conf')

import sincronizadorNodos
import config


class ServidorHTTP(BaseHTTPServer.BaseHTTPRequestHandler):
    server_version = "Kerberus - Sincronizador /" + __version__

    def denegar(self, mensaje):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(mensaje)
        return True

    def estaRespondiendo(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Online')
        return True

    def responder(self, respuesta):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(respuesta)

    def do_GET(self):
        user_id = self.headers.getheader('UserID')
        server_id = self.headers.getheader('ServerID')
        peticion = self.headers.getheader('peticion')
        ip_client = self.headers.getheader('X-Forwarded-For')
        self.server.logger.log(logging.DEBUG, "Peticion: %s ", peticion)
        self.server.logger.log(logging.DEBUG, "ServerID: %s ", server_id)
        self.server.logger.log(logging.DEBUG, "IP: %s ", ip_client)
        # FIXME: Deberia sacarlo de la base de datos
        credencial = hashlib.md5('k3rb3r4sk3rb3r4s').hexdigest()

        if self.headers.getheader('Credencial') != credencial:
            self.denegar('Acceso Denegado')
            return True

        if peticion == 'estaRespondiendo':
            self.estaRespondiendo()
        elif peticion == 'cambioDePassword':
            nueva_password = self.headers.getheader("NuevaPassword")
            respuesta = self.server.sincronizadorNodos.acentarCambioDePassword(
                user_id,
                server_id,
                nueva_password
                )
            self.responder(respuesta)
        elif peticion == 'nuevoUsuario':
            user_id = self.headers.getheader("UserID")
            server_id = self.headers.getheader("ServerID")
            ip = self.headers.getheader("UltimaIp")
            nombre = self.headers.getheader("Nombre")
            email = self.headers.getheader("Email")
            password = self.headers.getheader("Password")
            version = self.headers.getheader("Version")
            idioma = self.headers.getheader("Idioma")
            respuesta = self.server.sincronizadorNodos.acentarNuevoUsuario(
                user_id,
                server_id,
                ip,
                nombre,
                email,
                password,
                version,
                idioma
                )
            self.responder(respuesta)
        elif peticion == 'bajaUsuario':
            user_id = self.headers.getheader("UserID")
            server_id = self.headers.getheader("ServerID")
            respuesta = self.server.sincronizadorNodos.acentarBajaUsuario(
                user_id,
                server_id)
            self.responder(respuesta)
        else:
            self.denegar("Pedido invalido: %s" % peticion)
            return False

        self.connection.close()
        return True

    # Si viene como head, lo mando a get
#    do_HEAD = do_GET
        def do_HEAD(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

    def log_message(self, format, *args):
        pass
#       self.server.logger.log (
#                               logging.DEBUG, "%s %s",
#                               self.address_string (), format % args
#                              )

    def log_error(self, format, *args):
        self.server.logger.log(logging.ERROR, "%s %s", self.address_string(),
                                format % args)


class ThreadingHTTPServer(
                            SocketServer.ThreadingMixIn,
                            BaseHTTPServer.HTTPServer
                            ):
    def __init__(
                    self, server_address, RequestHandlerClass,
                    config, logger=None
                ):
        BaseHTTPServer.HTTPServer.__init__(
                                            self, server_address,
                                            RequestHandlerClass
                                            )
        # Defino las variables del server, estas podran ser accedidas por
        # todos los threads mediante el uso de self.server.variable.
        self.logger = logger
        self.sincronizadorNodos = sincronizadorNodos.SincronizadorNodos(config)


# Funciones
def handler(signo, frame):
    while frame and isinstance(frame, FrameType):
        if frame.f_code and isinstance(frame.f_code, CodeType):
            if "run_event" in frame.f_code.co_varnames:
                frame.f_locals["run_event"].set()
                return
        frame = frame.f_back


def logSetup(logfile, logsize, cant_rotaciones):
    logger = logging.getLogger("Kerberus-cluster")
    #logger.setLevel (logging.INFO)
    logger.setLevel(logging.DEBUG)
    #logger.setLevel (logging.ERROR)
    handler = logging.handlers.RotatingFileHandler(
                                        logfile,
                                        maxBytes=(logsize * (1 << 20)),
                                        backupCount=cant_rotaciones
                                                    )
    fmt = logging.Formatter(
                                "[%(asctime)-12s.%(msecs)03d] "
                                "%(levelname)-4s {%(threadName)s}"
                                " %(message)s",
                                "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger


def chequeosPeriodicos(server, periodo):
    while chequeos_activos:
        server.sincronizadorNodos.informarCambios()
        time.sleep(periodo)


def main(configuracion):
    # setup the log file
    logger = logSetup(
                        configuracion.log_filename, configuracion.log_size,
                        configuracion.log_rotaciones
                        )
    server_address = (configuracion.bind_address, configuracion.bind_port)
    ServidorHTTP.protocol = "HTTP/1.1"
    httpd = ThreadingHTTPServer(server_address, ServidorHTTP, configuracion,
                                logger)
    sa = httpd.socket.getsockname()

    run_event = threading.Event()
    signal.signal(signal.SIGINT, handler)
    req_count = 0

    logger.log(logging.INFO,
                "Sincronizador iniciado. Atendiendo en %s:%s" % (sa[0], sa[1]))
    print "Kerberus - Sincronizador, atendiendo en", sa[0], "puerto", sa[1]
    # FIXME: Esto quedo medio chancho, hay que ver de armar una clase donde
    # Esto permite que cada 'periodo' segundos se chequee en busca de cambios
    # a informar.
    global chequeos_activos
    chequeos_activos = True
    t = threading.Thread(
                        target=chequeosPeriodicos,
                        args=(httpd, configuracion.periodo_chequeo)
                        )
    t.start()
    while not run_event.isSet():
        try:
            httpd.handle_request()
            req_count += 1
            if req_count == 1000:
                logger.log(logging.INFO, "Numero de hilos en ejecucion: %s",
                            threading.activeCount())
                req_count = 0
        except select.error, e:
            if e[0] == 4 and run_event.isSet():
                pass
            else:
                logger.log(logging.CRITICAL, "Error Nro: %d - %s", e[0], e[1])
    chequeos_activos = False
    logger.log(logging.INFO, "Kerberus - Sincronizador, detenido correctamente")
    return 0


def setup_inicial(configuracion):
    pass


def lanzar_server(configuracion):
    print "Iniciando el sincronizador"
    sys.exit(main(configuracion))


def detener_server():
    print "Deteniendo el sincronizador..."
    chequeos_activos = False


def reload_server(arg1, arg2):
    print "Recargando la configuracion del sincronizador..."
#    archivo_config = '/srv/kerberus/sincronizador.conf'
#    configuracion = config.serverConfig(archivo_config)
#    ServerSync.recargarConfigServer(configuracion)

if __name__ == '__main__':
    archivo_config = 'sincronizador.conf'
    configuracion = config.sincronizadorConfig(archivo_config)
    lanzar_server(configuracion)
