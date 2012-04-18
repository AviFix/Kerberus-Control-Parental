# -*- coding: utf-8 *-*

"""Modulo encargado de obtener la lista de servidores activos"""

#Modulos externos
import socket, logging, sys, urllib2,time


#Modulos propios
sys.path.append('../conf')
import config
import funciones
import peticion

#Excepciones
class ServidorError(Exception): pass

# Logging
logger = funciones.logSetup (config.LOG_FILENAME, config.LOGLEVEL, config.LOG_SIZE_MB, config.LOG_CANT_ROTACIONES,"Modulo Servidores")

# Clase
class Servidor:

    def __init__(self):
        self.listaDeServidores=[]
        for i in range(1,100):
            ip_new="validador%s.kerberus.com.ar" % i
            port_new=80
            server=[ip_new,port_new]
            self.listaDeServidores.append(server)


    def estaRespondiendo(self, ip, port, userid):
        server="http://%s:%s" % (ip,port)
        headers = {"UserID":userid,"Peticion":"estaRespondiendo"}

        if config.USAR_PROXY:
            if self.estaOnline(config.PROXY_IP,config.PROXY_PORT):
                url_proxy="http://%s:%s" % (config.PROXY_IP,config.PROXY_PORT)
                logger.log(logging.DEBUG,"Conectando a %s, por medio del proxy %s , para realizar la solicitud: %s" %(server,url_proxy,headers['Peticion']))
                proxy={'http':url_proxy, 'https': url_proxy}
            else:
                logger.log(logging.ERROR,"El proxy no esta escuchando en %s:%s por lo que no se \
                utilizara" % (config.PROXY_IP,config.PROXY_PORT,))
                proxy={}
        else:
            proxy={}
        proxy_handler=urllib2.ProxyHandler(proxy)
        opener=urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        try:
            req = urllib2.Request(server, headers=headers)
            timeout=2
            respuesta = urllib2.urlopen(req,timeout).read()
            logger.log(logging.DEBUG,"Respuesta: %s" % respuesta)
            return (respuesta == 'Online')
        except urllib2.URLError as error:
            logger.log(logging.ERROR,"Error al conectarse a %s, peticion: %s . ERROR: %s" %(server,headers['Peticion'],error))
            return False

    def estaOnline(self,ip,port):
        """Verifica si el puerto esta abierto. Util para chequear el proxy nomas"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        try:
            s.connect((ip, int(port)))
            s.shutdown(2)
            return True
        except:
            logger.log(logging.ERROR,"No hay conexion a %s:%s" %(ip,port,))
            return False


    def obtenerServidor(self,ip=False, port=False,userID=1):
        servers=[[ip,port]]+self.listaDeServidores
        for ip, port in servers:
            if self.estaRespondiendo(ip,port,userID):
                logger.log(logging.INFO,"Utilizando el servidor de validacion %s:%s" %(ip,port,))
                return ip, port
            else:
                logger.log(logging.INFO,"El servidor de validacion %s:%s no responde" %(ip,port,))

        logger.log(logging.CRITICAL,"No se pudo obtener ningun servidor de validacion!")
        return False, False
