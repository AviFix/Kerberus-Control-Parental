# -*- coding: utf-8 *-*

"""Modulo encargado de obtener la lista de servidores activos"""

#Modulos externos
import socket, logging

#Modulos propios
import config
import funciones

#Excepciones
class ServidorError(Exception): pass

# Logging
logger = funciones.logSetup (config.LOG_FILENAME, config.LOGLEVEL, config.LOG_SIZE_MB, config.LOG_CANT_ROTACIONES,"Modulo Servidores")

# Clase
class Servidor:
    def estaOnline(self,ip,port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.6)
        try:
            s.connect((ip, int(port)))
            s.shutdown(2)
            return True
        except:
            logger.log(logging.ERROR,"No hay conexion a %s:%s" %(ip,port,))
            return False

    def obtenerServidor(self,ip=False, port=False):
        if ip and port:
            if self.estaOnline(ip,port):
                logger.log(logging.INFO,"Utilizando el servidor de validacion %s:%s" %(ip,port,))
                return ip, port
            else:
                for i in range(1,100):
                    ip="validador%s.kerberus.com.ar" % i
                    port=80
                    if self.estaOnline(ip,port):
                        logger.log(logging.INFO,"Utilizando el servidor de validacion %s:%s" %(ip,port,))
                        return ip, port
                logger.log(logging.CRITICAL,"No se pudo obtener ningun servidor de validacion!")
                return False
