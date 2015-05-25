#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Modulo encargado de levantar el servidor"""

__version__ = "0.3"

#Modulos externos
import BaseHTTPServer
import SocketServer
#import logging
import sys
import logging.handlers
import time
import urllib2
import hashlib

# Modulos propios
sys.path.append('clases')
sys.path.append('conf')

import config
import urls
#import filtradoPorDNS
import usuarios
import clientes
import versiones
import sincronizadorNodos
import cluster

usuarios_password_recordadas = {}
versiones_nuevas = versiones.Versiones()

class ServidorHTTP (BaseHTTPServer.BaseHTTPRequestHandler):
    server_version = "Kerberus - Server /" + __version__
    # FIXME: estas variables deberian ser definidas dentro de la clase
    # ThreadingHTTPServer y no aca como global

    global usuarios_password_recordadas
    global versiones_nuevas

    def denegar(self, motivo, url="", user_id=""):
        self.send_response(403, motivo)
        self.server.logger.log(logging.INFO,
        "DENEGADO:%s - Motivo:%s - UserID:%s" % (url, motivo, user_id))

    def denegar2(self, motivo, url="", user_id=""):
        self.send_response(205, motivo)
        self.server.logger.log(logging.INFO,
        "DENEGADO:%s - Motivo:%s - UserID:%s" % (url, motivo, user_id))

    def permitir(self, url="", user_id=""):
        self.send_response(204)
        self.server.logger.log(logging.INFO,
        "PERMITIDO:%s - UserID:%s" % (url, user_id))

    def registrarUsuario(self, nombre, email, password, version, ip,
        server_id, idioma):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        users = usuarios.Usuarios()
        idUsuario = False
        # FIXME: Deberia desaparecer cuando todos esten en la version 1.1
        if server_id == -1:
            server_id = 1
            version_vieja = True
        else:
            version_vieja = False

        my_server_ID = int(self.server.validador.serverConfig.serverID)

        if int(server_id) == 0 or int(server_id) == my_server_ID:
            idUsuario = users.registrarUsuario(nombre, email, password,
                version, ip, idioma)
            server_id = my_server_ID

        # FIXME: Deberia desaparecer cuando todos esten en la version 1.1
        if version_vieja:
            if server_id == my_server_ID:
                respuesta = "%s" % idUsuario
            else:
                respuesta = "0"
        else:
            respuesta = "%s,%s" % (idUsuario, my_server_ID)

        self.wfile.write(respuesta)
        # Reporto al cluster el cambio
        if idUsuario:
            self.server.sincronizadorNodos.cluster.registrarNuevoUsuario(
                idUsuario,
                server_id,
                nombre,
                email,
                password,
                version,
                ip,
                idioma
                )
            # FIXME: Comente esta linea porque si un nodo esta caido demora
            # en contestarle al cliente.
#            self.server.sincronizadorNodos.reportarNuevosUsuarios()
        return True

    def registrarNuevaPassword(self, user_id, server_id, password_vieja,
    password_nueva):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        users = usuarios.Usuarios()
        if server_id == -1:
            server_id = 1
        respuesta = users.registrarNuevaPassword(user_id, server_id,
            password_vieja, password_nueva)
        self.wfile.write("%s" % respuesta)

        if respuesta == 'Informada':
            cliente = '%s,%s' % (user_id, server_id)
            credencial = \
                    hashlib.md5(password_nueva.encode('utf-8')).hexdigest()
            self.server.clientes_autenticados[cliente] = credencial
            # Reporto al cluster el cambio
            self.server.sincronizadorNodos.cluster.registrarCambioDePassword(
                user_id,
                server_id,
                password_nueva)
            # FIXME: Comente esta linea porque si un nodo esta caido demora
            # en contestarle al cliente.
#            self.server.sincronizadorNodos.reportarCambiosDePassword()
        return True

    def recordarPassword(self, user_id, server_id):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        users = usuarios.Usuarios()
        tiempo_actual = time.time()
        if server_id == -1:
            server_id = 1
        usuario = '%s,%s' % (user_id, server_id)
        if usuario in usuarios_password_recordadas:
            ultimo_pedido = usuarios_password_recordadas[usuario]
            tiempo_transcurrido = tiempo_actual - ultimo_pedido
            # se puede cada 600 segs (10min)
            if (tiempo_transcurrido > 600):
                usuarios_password_recordadas[usuario] = tiempo_actual
                respuesta = users.recordarPassword(user_id, server_id)
                self.wfile.write("%s" % respuesta)
                return True
            else:
                self.wfile.write("No")
        else:
            usuarios_password_recordadas[usuario] = tiempo_actual
            respuesta = users.recordarPassword(user_id, server_id)
            self.wfile.write("%s" % respuesta)
            return True

    def eliminarUsuario(self, user_id, server_id):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if server_id == -1:
            server_id = 1
        users = usuarios.Usuarios()
        respuesta = users.eliminarUsuario(user_id, server_id)
        self.wfile.write("%s" % respuesta)
        if respuesta:
            # Reporto al cluster el cambio
            self.server.sincronizadorNodos.cluster.registrarBajaUsuario(
                user_id,
                server_id)
            # FIXME: Comente esta linea porque si un nodo esta caido demora
            # en contestarle al cliente.
#            self.server.sincronizadorNodos.reportarBajasDeUsuarios()
        return True

    def usuarioRegistrado(self, user_id, server_id, email):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if server_id == -1:
            server_id = 1
        users = usuarios.Usuarios()
        respuesta = users.usuarioRegistrado(user_id, server_id, email)
        self.wfile.write("%s" % respuesta)
        return True

    def chequearActualizaciones(self, version_cliente, plataforma):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # FIXME: Esto se deberia chequear cada tanto, y no cada vez que el
        # cliente solicita
        url, md5sum = versiones_nuevas.obtenerVersion(version_cliente,
            plataforma)
        respuesta = "%s,%s" % (url, md5sum)
        self.wfile.write(respuesta)
        return True

    def estaRespondiendo(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Online')
        return True

    def devolverRankingServidores(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        ranking = self.server.clusterInfo.obtenerRankingServidores()
        #self.wfile.write('validador1.kerberus.com.ar:443\n'
                            #'validador2.kerberus.com.ar:443')
        self.wfile.write(ranking)
        return True

    def devolverDominiosPermitidos(self, ultima_sync=0):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        modificados_despues_de = time.strftime("%Y-%m-%d %H:%M:%S",
        time.localtime(float(ultima_sync)))
        respuesta = \
        "%s" % self.server.validador.getDominiosPermitidos(
            modificados_despues_de)
        self.wfile.write(respuesta)
        return True

    def devolverDominiosDenegados(self, ultima_sync=0):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        modificados_despues_de = time.strftime("%Y-%m-%d %H:%M:%S",
        time.localtime(float(ultima_sync)))
        respuesta = \
        "%s" % self.server.validador.getDominiosDenegados(
            modificados_despues_de)
        self.wfile.write(respuesta)
        return True

    def devolverHoraServidor(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        hora = time.time()
        self.wfile.write("%s" % hora)
        return True

    def devolverPeriodoDeActualizacion(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(
            "%s" % self.server.validador.getPeriodoDeActualizacion()
            )
        return True

    def devolverPeriodoDeRecargaCompleta(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(
            "%s" % self.server.validador.getPeriodoDeRecargaCompleta()
            )
        return True

    def validarUrl(self, url):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        respuesta, mensaje = self.server.validador.urlHabilitada(url)
        # Mensaje es igual a "" si esta permitido el sitio
        self.wfile.write("%s" % mensaje)
        return True

    def autenticarCliente(self, user_id, server_id, credencial):
        cliente = '%s,%s' % (user_id, server_id)
        if cliente in self.server.clientes_autenticados:
            if self.server.clientes_autenticados[cliente] == credencial:
                return True
        cli = clientes.Cliente()
        autenticado = cli.clienteValido(user_id, server_id, credencial)
        if autenticado:
            self.server.clientes_autenticados[cliente] = credencial
        return autenticado

    def actualizarDatosCliente(self, user_id, server_id, version,
                                ip_client, credencial):
        cli = clientes.Cliente()
        cli.actualizarDatosCliente(user_id, server_id, version, ip_client,
                                    credencial)

    def do_GET(self):
        user_id = self.headers.getheader('UserID')
        # FIXME: deberia desaparecer este try-except cuando todos esten en la
        # version 1.1 o superior
        try:
            server_id = self.headers.getheader('ServerID')
        except:
            server_id = -1
        if server_id == None:
            server_id = -1

        peticion = self.headers.getheader('peticion')
        ip_client = self.headers.getheader('X-Forwarded-For')
        version = self.headers.getheader('Version')
        plataforma = self.headers.getheader('Plataforma')

        # Temporal hasta que se actualicen todos

        peticionesAutenticables = [
            'chequearActualizaciones',
            'eliminarUsuario',
            'recordarPassword',
            'consulta'
            ]
#        peticionesNoAutenticables = [
#            'estaRespondiendo',
#            'usuarioRegistrado',
#            'registrarUsuario',
#            'obtenerServidores',
#            'validarUrl',
            #'getPeriodoDeRecargaCompleta',
            #'obtenerDominiosPermitidos',
            #'obtenerDominiosDenegados',
            #'getPeriodoDeActualizacion',
            #'getHoraServidor',
#            'informarNuevaPassword'
#            ]
        if (peticion in peticionesAutenticables) and (version != '1.0'):
            credencial = self.headers.getheader('Credencial')
            cliente_autenticado = self.autenticarCliente(user_id,
            server_id, credencial)

            if not cliente_autenticado:
                self.denegar(
                    "No autorizado: \n"
                    "- Peticion: %s\n"
                    "- userid: %s\n"
                    "- serverid: %s\n"
                    "- credencial: %s"
                    % (peticion, user_id, server_id, credencial,))
                return False

        if not user_id:
            self.denegar("Se requiere un usuario")
            return False

        self.server.logger.log(logging.DEBUG,
            "Peticion: %s, UserID:%s, ServerID:%s, Version:%s, IP:%s" %
            (peticion, user_id, server_id, version, ip_client))

        if peticion == 'obtenerDominiosPermitidos':
            ultima_sincronizacion_cliente = \
            self.headers.getheader('UltimaSync')
            self.devolverDominiosPermitidos(
                ultima_sincronizacion_cliente)

        elif peticion == 'obtenerDominiosDenegados':
            ultima_sincronizacion_cliente = \
            self.headers.getheader('UltimaSync')
            self.devolverDominiosDenegados(ultima_sincronizacion_cliente)

        elif peticion == 'getPeriodoDeActualizacion':
            self.devolverPeriodoDeActualizacion()

        elif peticion == 'getHoraServidor':
            self.devolverHoraServidor()

        elif peticion == 'chequearActualizaciones':
            self.chequearActualizaciones(version, plataforma)

        elif peticion == 'getPeriodoDeRecargaCompleta':
            self.devolverPeriodoDeRecargaCompleta()

        elif peticion == 'registrarUsuario':
            nombre = self.headers.getheader('Nombre')
            email = self.headers.getheader('Email')
            password = self.headers.getheader('Password')
            version = self.headers.getheader('Version')
            try:
                idioma = self.headers.getheader('Idioma')
            except:
                idioma = "es"
            # quito las quota aplicadas para el dialogo http
            nombre = unicode(urllib2.unquote(nombre), 'utf-8')
            email = unicode(urllib2.unquote(email), 'utf-8')
            password = unicode(urllib2.unquote(password), 'utf-8')
            self.registrarUsuario(nombre, email, password, version,
            ip_client, server_id, idioma)

        elif peticion == 'eliminarUsuario':
            self.eliminarUsuario(user_id, server_id)

        elif peticion == 'usuarioRegistrado':
            email = self.headers.getheader('Email')
            self.usuarioRegistrado(user_id, server_id, email)
            if version != '1.0':
                credencial = self.headers.getheader('Credencial')
                self.actualizarDatosCliente(user_id, server_id, version,
                                            ip_client, credencial)

        elif peticion == 'estaRespondiendo':
            self.estaRespondiendo()

        elif peticion == 'informarNuevaPassword':
            password_nueva = self.headers.getheader('PasswordNueva')
            password_vieja = self.headers.getheader('PasswordVieja')
            password_nueva = unicode(urllib2.unquote(password_nueva), 'utf-8')
            self.registrarNuevaPassword(user_id, server_id, password_vieja,
            password_nueva)

        elif peticion == 'recordarPassword':
            self.recordarPassword(user_id, server_id)

        elif peticion == 'validarUrl':
            url = self.headers.getheader('URL')
            self.validarUrl(url)

        elif peticion == 'obtenerServidores':
            self.devolverRankingServidores()

        elif peticion == 'consulta':
            url = self.headers.getheader('URL')
            self.verificarURL(url, user_id)
        else:
            self.denegar("Pedido invalido: %s" % peticion, "", user_id)
            return False

        self.connection.close()
        return True

    # Si viene como head, lo mando a get
    do_HEAD = do_GET

    def verificarURL(self, url, user_id):
            self.server.logger.log(logging.DEBUG, "Url solicitada: %s ", url)
            permitido, motivo = self.server.validador.urlHabilitada(url)
            if permitido:
                self.permitir(url, user_id)
            else:
                self.denegar2(motivo, url, user_id)
            self.connection.close()
            return True

    def log_message(self, format, *args):
        pass
#        self.server.logger.log (
#                                    logging.DEBUG, "%s %s",
#                                    self.address_string(),
#                                    format % args
#                                    )

    def log_error(self, format, *args):
        self.server.logger.log(logging.ERROR, "%s %s", self.address_string(),
                                format % args)


class ThreadingHTTPServer(SocketServer.ThreadingMixIn,
                            BaseHTTPServer.HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, logger=None):
        BaseHTTPServer.HTTPServer.__init__(self, server_address,
                                            RequestHandlerClass)
        self.logger = logger
        self.sincronizadorNodos = sincronizadorNodos.SincronizadorNodos()
        self.validador = urls.Urls()
        self.clientes_autenticados = {}
        self.clusterInfo = cluster.Cluster()


# Funciones

def logSetup(logfile, logsize, cant_rotaciones):
    logger = logging.getLogger("Kerberus")
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


def main(configuracion):
    # setup the log file
    logger = logSetup(configuracion.log_filename, configuracion.log_size,
                        configuracion.log_rotaciones)
    server_address = (configuracion.bind_address, configuracion.bind_port)
    ServidorHTTP.protocol = "HTTP/1.1"
    httpd = ThreadingHTTPServer(server_address, ServidorHTTP, logger)
    sa = httpd.socket.getsockname()
    logger.log(
        logging.INFO, "Server iniciado. Atendiendo en %s:%s" % (sa[0], sa[1])
                )
    httpd.validador.setLogger(logger)
    httpd.validador.inicializarServer(configuracion)
    print "Kerberus - Server, atendiendo en", sa[0], "puerto", sa[1]
    httpd.serve_forever()
    logger.log(logging.INFO, "Server shutdown")
    return 0


def setup_inicial():
    pass


def lanzar_server():
    archivo_config = '/srv/kerberus/server.conf'
    configuracion = config.serverConfig(archivo_config)
    sys.exit(main(configuracion))


def detener_server(arg1, arg2):
    print "Deteniendo el servidor..."


#def reload_server(arg1, arg2):
#    print "Recargando la configuracion del servidor..."
#    archivo_config = '/srv/kerberus/server.conf'
#    configuracion = config.serverConfig(archivo_config)
#    self.server.validador.recargarConfigServer(configuracion)

if __name__ == '__main__':
    lanzar_server()
