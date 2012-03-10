# -*- coding: utf-8 -*-
#
"""Modulo encargado del dialogo con el server remoto"""

# Modulos externos
import sys
import urllib2
import logging
import sqlite3

# Modulos propios
sys.path.append('../conf')
sys.path.append('../')
import servidores
import config
import funciones
import time
import registrar

# Logging
logger = funciones.logSetup (config.SYNC_LOG_FILENAME, config.SYNC_LOGLEVEL, config.SYNC_LOG_SIZE_MB, config.SYNC_LOG_CANT_ROTACIONES,"Peticion")

# Clase
class Peticion:
    def __init__(self):
        self.servidor=servidores.Servidor()
        self.userid=self.obtenerUserID()
        self.server_ip,self.server_port = self.servidor.obtenerServidor(config.SYNC_SERVER_IP,config.SYNC_SERVER_PORT,self.userid)
        self.server_sync="%s:%s" % (self.server_ip,self.server_port)

    def obtenerUserID(self):
        try:
            conexion_db = sqlite3.connect(config.PATH_DB)
            cursor=conexion_db.cursor()
            id = cursor.execute('select id from instalacion').fetchone()[0]
            cursor.close()
            return id
        except sqlite3.OperationalError, msg:
            self.logger.log(logging.ERROR,"No se pudo obtener el id de instalacion.\nError: %s" % msg)
            id=0
            return id

    def obtenerRespuesta(self,headers):
        #FIXME: Si no obtiene respuesta, deberia buscar otro server
        if config.USAR_PROXY:
            if self.servidor.estaOnline(config.PROXY_IP,config.PROXY_PORT):
                url_proxy="http://%s:%s" % (config.PROXY_IP,config.PROXY_PORT)
                logger.log(logging.DEBUG,"Conectando a %s, por medio del proxy %s , para realizar la solicitud: %s" %(self.server_sync,url_proxy,headers['Peticion']))
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
        logger.log(logging.DEBUG,"Conectando a %s para realizar la solicitud: %s" %(self.server_sync,headers['Peticion']))
        dormir_por=1
        while True:
            try:
                if self.servidor.estaOnline(self.server_ip,self.server_port):
                    req = urllib2.Request("http://"+self.server_sync, headers=headers)
                    respuesta = urllib2.urlopen(req).read()
                    logger.log(logging.DEBUG,"Respuesta: %s" % respuesta)
                    return respuesta
            except urllib2.URLError as error:
                logger.log(logging.ERROR,"Error al conectarse a %s, peticion: %s . ERROR: %s" %(self.server_sync,headers['Peticion'],error))
            logger.log(logging.ERROR,"Durmiendo por %s", dormir_por)
            time.sleep(dormir_por)
            #se va incrementando el tiempo de dormir para no  matar el micro
            if dormir_por < 64:
                dormir_por=dormir_por*2


    def obtenerDominiosPermitidos(self,ultima_actualizacion):
        headers = {"UserID":self.userid ,"Peticion":"obtenerDominiosPermitidos","UltimaSync":str(ultima_actualizacion)}
        dominios = self.obtenerRespuesta(headers)
        return dominios

    def informarNuevaPassword(self, password):
        headers = {"UserID":self.userid ,"Peticion":"informarNuevaPassword","Password":str(password)}
        respuesta = self.obtenerRespuesta(headers)
        return respuesta

    def obtenerDominiosDenegados(self,ultima_actualizacion):
        headers = {"UserID":self.userid ,"Peticion":"obtenerDominiosDenegados","UltimaSync":str(ultima_actualizacion)}
        dominios = self.obtenerRespuesta(headers)
        return dominios

    def obtenerPeriodoDeActualizacion(self):
        """Obtiene el periodo de actualizacion. Devuelve en segundos"""
        headers = {"UserID": self.userid,"Peticion":"getPeriodoDeActualizacion"}
        respuesta = self.obtenerRespuesta(headers)
        if not respuesta:
            respuesta=1
        respuesta_en_segs=int(respuesta)*60
        return respuesta_en_segs

    def obtenerPeriodoDeRecargaCompleta(self):
        """Obtiene el periodo de recarga completa. Devuelve en segundos"""
        headers = {"UserID": self.userid,"Peticion":"getPeriodoDeRecargaCompleta"}
        respuesta = self.obtenerRespuesta(headers)
        if not respuesta:
            respuesta=1
        respuesta_en_segs=int(respuesta)*60
        return respuesta_en_segs

    def obtenerHoraServidor(self):
        """Obtiene la hora del servidor. Devuelve en segundos"""
        headers = {"UserID": self.userid,"Peticion":"getHoraServidor"}
        respuesta = self.obtenerRespuesta(headers)
        return respuesta

    def registrarUsuario(self, nombre, email, password, version):
        """Devuelve el id si registra, sino devuelve 0"""
        headers = {"UserID": self.userid,"Peticion":"registrarUsuario","Nombre":nombre,"Email":email,"Password":password,"Version":version}
        respuesta = self.obtenerRespuesta(headers)
        return respuesta

    def eliminarUsuario(self, id):
        """Solicita la eliminacion"""
        headers = {"UserID": self.userid,"Peticion":"eliminarUsuario"}
        respuesta = self.obtenerRespuesta(headers)
        return respuesta

    def usuarioRegistrado(self, id, email):
        #FIXME: Debe enviar id y email para verificar
        """Devuelve true o false"""
        headers = {"UserID": self.userid,"Peticion":"usuarioRegistrado","ID":id,"Email":email}
        respuesta = self.obtenerRespuesta(headers)
        return respuesta

