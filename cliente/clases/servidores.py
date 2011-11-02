# -*- coding: utf-8 *-*

"""Modulo encargado de obtener la lista de servidores activos"""

#Modulos externos
import socket

#Modulos propios

#Excepciones
class ServidorError(Exception): pass


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
            return False

    def obtenerServidor(self,ip=False, port=False):
        if ip and port:
            if self.estaOnline(ip,port):
                return ip, port
            else:
                for i in range(1,100):
                    ip="validador%s.kerberus.com.ar" % i
                    port=80
                    if self.estaOnline(ip,port):
                        return ip, port
                return False
