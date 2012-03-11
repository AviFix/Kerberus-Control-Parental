#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__ = "0.5"

# Modulos externos
import BaseHTTPServer, select, socket, SocketServer, urlparse
import sys
import signal
import threading
from types import FrameType, CodeType
import ftplib
import base64
import platform
import os
import time
import logging
from PyQt4 import QtGui

sys.path.append('clases')
sys.path.append('conf')
sys.path.append('password')

#Modulos propios

import consultor
import manejadorUrls
import config
import funciones
import administradorDeUsuarios
import pedirUsuario
import mensajesHtml

# Logging
logger = funciones.logSetup (config.LOG_FILENAME, config.LOGLEVEL, config.LOG_SIZE_MB, config.LOG_CANT_ROTACIONES,"Modulo cliente")

if not os.path.exists(config.PATH_DB):
    funciones.crearDBCliente(config.PATH_DB)

verificador=consultor.Consultor()
urls=manejadorUrls.ManejadorUrls()
adminUsers=administradorDeUsuarios.AdministradorDeUsuarios()


class ProxyHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    __base = BaseHTTPServer.BaseHTTPRequestHandler
    __base_handle = __base.handle

    server_version = "Kerberus - Cliente /" + __version__
    rbufsize = 0                        # self.rfile Be unbuffered
    global verificador


    def mostrarPublicidad(self, url):
        msg="<html><head><title>Navegador protegido por Kerberus</title>\
        <meta http-equiv=\"REFRESH\" content=\"0;url=http://inicio.kerberus.com.ar\" > \
        </head> <body ></body> </html> "
        self.server.logger.log (logging.DEBUG, "Primer pagina de acceso.")
        self.responderAlCliente(msg)

    def mostrarDeshabilitado(self):
        msg="<html><head><title>Navegador protegido por Kerberus</title>\
        </head> <body >Navegación Deshabilitada</body> </html> "
        self.responderAlCliente(msg)

    def responderAlCliente(self,mensaje):
        tamano=len(mensaje)
        self.wfile.write(self.protocol_version + " 200 Connection established\r\n")
        self.wfile.write("Content-Type: text/html\r\n")
        self.wfile.write(" Content-Length: %s\r\n" % tamano)
        self.wfile.write("\r\n")
        self.wfile.write(mensaje)
        self.connection.close()

    def pedirPassword(self):
        mensaje=mensajesHtml.MensajesHtml(config.PATH_TEMPLATES)
        msg=mensaje.pedirPassword()
        self.responderAlCliente(msg)

    def cambiarPassword(self):
        mensaje=mensajesHtml.MensajesHtml(config.PATH_TEMPLATES)
        msg=mensaje.cambiarPassword()
        self.responderAlCliente(msg)

    def redirigirDesbloqueado(self, url):
        msg="<html><head><meta HTTP-EQUIV=\"REFRESH\" content=\"0; url=%s\"></head></html>" % url
        self.responderAlCliente(msg)

    def passwordErronea(self):
        mensaje=mensajesHtml.MensajesHtml(config.PATH_TEMPLATES)
        msg=mensaje.pedirPassword('Password incorrecta!')
        self.responderAlCliente(msg)

    def cambioPassPasswordErronea(self):
        mensaje=mensajesHtml.MensajesHtml(config.PATH_TEMPLATES)
        msg=mensaje.cambiarPassword('Password incorrecta!')
        self.responderAlCliente(msg)


    def denegar(self, motivo, url):
        mensaje=mensajesHtml.MensajesHtml(config.PATH_TEMPLATES)
        msg=mensaje.denegarSitio(url)
        self.responderAlCliente(msg)

    def handle(self):
        self.__base_handle()

    def _connect_to(self, netloc, soc):
        i = netloc.find(':')
        if i >= 0:
            host_port = netloc[:i], int(netloc[i+1:])
        else:
            host_port = netloc, 80
        self.server.logger.log (logging.DEBUG, "connect to %s:%d", host_port[0], host_port[1])
        try:
             soc.connect(host_port)

        except socket.error, arg:
            try:
                msg = arg[1]
            except:
                msg = arg
                self.send_error(404, msg)
            return False
        return True

    def do_CONNECT(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self._connect_to(self.path, soc):
                self.wfile.write(self.protocol_version +" 200 Connection established\r\n")
                self.wfile.write("Proxy-agent: %s\r\n" % self.version_string())
                self.wfile.write("\r\n")
                self._read_write(soc, 300)
        finally:
            soc.close()
            self.connection.close()


    def validarPassword(self,password):
        return adminUsers.usuario_valido('admin',password)

    def do_GET(self):
        url=self.path
#        if verificador.primerUrl:
#            verificador.primerUrl=False
#            if "kerberus.com.ar" not in url:
#                self.mostrarPublicidad(url)
#                return False
#
        usuario, password="NoBody", "NoBody"
        # es para que muestre que kerberus esta activo, asi no lo muestra cuando se accede
        # a la pagina desde cualquier lugar

        if "!DeshabilitarFiltrado!" in url:
            url=url.replace('!DeshabilitarFiltrado!','')
            if verificador.kerberus_activado:
                if self.command == 'POST':
                    content_len = int(self.headers.getheader('content-length'))
                    post_body = self.rfile.read(content_len)
                    password=post_body.split("=")[1]
                    usuario_admin=self.validarPassword(password)
                    if usuario_admin:
                        verificador.kerberus_activado=False
                        self.redirigirDesbloqueado(url)
                        return True
                    else:
                        self.passwordErronea()
                        return True
                else:
                    self.pedirPassword()
                    return True

        # Cambio de password
#
#        if "!CambiarPassword!" in url:
#            url=url.replace('!CambiarPassword!','')
#            if self.command == 'POST':
#                content_len = int(self.headers.getheader('content-length'))
#                post_body = self.rfile.read(content_len)
#                print post_body
#                password_actual=post_body.split("=")[1]
#                usuario_admin=self.validarPassword(password_actual)
#                if usuario_admin:
#                    password_nueva1=post_body.split("=")[2]
#                    password_nueva2=post_body.split("=")[3]
#                    if password_nueva1 <> password_nueva2:
#                        self.cambioPassPasswordNoCoinciden()
#                    # Cambiar Aca la password!!!!!!!!!!!!!!!
#                    # Quede aca
#                    return True
#                else:
#                    self.cambioPassPasswordErronea()
#                    return True
#            else:
#                self.pedirPassword()
#                return True
#

        #FIXME: Esto deberia ser un header no por url
        if "http://inicio.kerberus.com.ar" in url and verificador.kerberus_activado and "denegado.php" not in url:
           url=url+"?kerberus_activado=1"

        if verificador.kerberus_activado:
            permitido, motivo=verificador.validarUrl(usuario, password,url)
            if not permitido:
                self.denegar(motivo, url)
                return False
            if urls.soportaSafeSearch(url):
                url=urls.agregarSafeSearch(url)
                self.server.logger.log (logging.INFO, "La URL %s  soporta SafeSearch. Forzando su uso", url)

        # Si llego hasta aca es porque esta permitido
        (scm, netloc, path, params, query, fragment) = urlparse.urlparse(url,  'http')
        if scm not in ('http', 'ftp') or fragment or not netloc:
            self.send_error(400, "Url erronea: %s" % url)
            return False
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if scm == 'http':
                if self._connect_to(netloc, soc):
                    self.log_request()
                    try:
                        self.server.logger.log(logging.DEBUG,"Enviando: %s %s %s\r\n" % (self.command, urlparse.urlunparse(('', '', path, params, query,'')),self.request_version))
                        soc.send("%s %s %s\r\n" % (self.command, urlparse.urlunparse(('', '', path, params, query,'')),self.request_version))
                        self.headers['Connection'] = 'close'
                        del self.headers['Proxy-Connection']
                        for key_val in self.headers.items():
                            soc.send("%s: %s\r\n" % key_val)
                        soc.send("\r\n")
                        self._read_write(soc)
                    except:
                        self.server.logger.log (logging.ERROR, "Hubo un error en el metodo do_GET. URL: %s", url)

            elif scm == 'ftp':
                # fish out user and password information
                i = netloc.find ('@')
                if i >= 0:
                    login_info, netloc = netloc[:i], netloc[i+1:]
                    try:
                        user, passwd = login_info.split (':', 1)
                    except ValueError:
                        user, passwd = "anonymous", None
                else:
                    user, passwd ="anonymous", None
                self.log_request ()
                try:
                    ftp = ftplib.FTP (netloc)
                    ftp.login (user, passwd)
                    if self.command == "GET":
                        ftp.retrbinary ("RETR %s"%path, self.connection.send)
                    ftp.quit ()
                except Exception, e:
                    self.server.logger.log (logging.WARNING, "FTP Exception: %s", e)
        finally:
            soc.close()
            self.connection.close()

    def _read_write(self, soc, max_idling=20, local=False):
        #Revisar esta funcion!!!!!! tira el problema 10053 de socket
        iw = [self.connection, soc]
        local_data = ""
        ow = []
        count = 0
        while 1:
            count += 1
            (ins, _, exs) = select.select(iw, ow, iw, 3)
            if exs:
                break
            if ins:
                for i in ins:
                    if i is soc:
                        out = self.connection
                    else:
                        out = soc
                    try:
                        data = i.recv(8192)
                    except:
                        data = ''

                    if data:
                        if local:
                            local_data += data
                        else:
                            out.send(data)
                        count = 0
            if count == max_idling:
                break
        if local:
            return local_data
        return None

    do_HEAD = do_GET
    do_POST = do_GET
    do_PUT  = do_GET
    do_DELETE=do_GET

    def log_message (self, format, *args):
        self.server.logger.log (logging.DEBUG, "%s %s", self.address_string (),
                                format % args)

    def log_error (self, format, *args):
        self.server.logger.log (logging.ERROR, "%s %s", self.address_string (),
                                format % args)

class ThreadingHTTPServer (SocketServer.ThreadingMixIn,
                           BaseHTTPServer.HTTPServer):
    def __init__ (self, server_address, RequestHandlerClass, logger=None):
        BaseHTTPServer.HTTPServer.__init__ (self, server_address,
                                            RequestHandlerClass)
        self.logger = logger


def handler (signo, frame):
    while frame and isinstance (frame, FrameType):
        if frame.f_code and isinstance (frame.f_code, CodeType):
            if "run_event" in frame.f_code.co_varnames:
                frame.f_locals["run_event"].set ()
                return
        frame = frame.f_back

def main ():
    run_event = threading.Event ()
    # setup the log file
    signal.signal (signal.SIGINT, handler)
    server_address = (config.BIND_ADDRESS, config.BIND_PORT)
    ProxyHandler.protocol = "HTTP/1.1"
    if config.USAR_PROXY:
        logger.log(logging.INFO,"Usando kerberus a traves de proxy %s:%s" % (config.PROXY_IP,config.PROXY_PORT))
    httpd = ThreadingHTTPServer (server_address, ProxyHandler, logger)
    sa = httpd.socket.getsockname ()
    logger.log(logging.INFO,'Kerberus - Cliente Activo, atendiendo en %s puerto %s' % (sa[0],sa[1],))
    req_count = 0
    while not run_event.isSet ():
        try:
            httpd.handle_request ()
            req_count += 1
            if req_count == 1000:
                logger.log (logging.INFO, "Number of active threads: %s",
                            threading.activeCount ())
                req_count = 0
        except select.error, e:
            if e[0] == 4 and run_event.isSet (): pass
            else:
                logger.log (logging.CRITICAL, "Errno: %d - %s", e[0], e[1])
    logger.log (logging.INFO, "Se ha detenido el cliente de Kerberus satisfactoriamente")
    return 0

if __name__ == '__main__':
    sys.exit (main ())
