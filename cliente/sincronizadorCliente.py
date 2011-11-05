# -*- coding: utf-8 -*-

# Modulos externos
import sys, time, os, sqlite3, httplib, platform, logging, urllib2
#import logging.handlers

# Modulos propios
sys.path.append('conf')
sys.path.append('clases')

import config
import funciones
import servidores

# Logging
logger = funciones.logSetup (config.SYNC_LOG_FILENAME, config.SYNC_LOGLEVEL, config.SYNC_LOG_SIZE_MB, config.SYNC_LOG_CANT_ROTACIONES,"Sincronizador")

def obtenerRespuesta(headers):
        servidor=servidores.Servidor()
        config.SYNC_SERVER_IP,config.SYNC_SERVER_PORT = servidor.obtenerServidor(config.SYNC_SERVER_IP,config.SYNC_SERVER_PORT)
        server_sync="%s:%s" % (config.SYNC_SERVER_IP,config.SYNC_SERVER_PORT)
        if config.USAR_PROXY:
            if servidor.estaOnline(config.PROXY_IP,config.PROXY_PORT):
                url_proxy="http://%s:%s" % (config.PROXY_IP,config.PROXY_PORT)
                logger.log(logging.DEBUG,"Conectando a %s, por medio del proxy %s , para realizar la solicitud: %s" %(server_sync,url_proxy,headers['Peticion']))
                proxy={'http':url_proxy, 'https': url_proxy}
                proxy_handler=urllib2.ProxyHandler(proxy)
                opener=urllib2.build_opener(proxy_handler)
                urllib2.install_opener(opener)
                req = urllib2.Request("http://"+server_sync, headers=headers)
                respuesta = urllib2.urlopen(req)
            else:
                logger.log(logging.ERROR,"El proxy no esta escuchando en %s:%s por lo que no se \
                utilizara" % (config.PROXY_IP,config.PROXY_PORT,))
        else:
            logger.log(logging.DEBUG,"Conectando a %s para realizar la solicitud: %s" %(server_sync,headers['Peticion']))
            conexion=httplib.HTTPConnection(server_sync)
            conexion.request("GET", "/", "", headers)
            respuesta=conexion.getresponse()
        return respuesta

def sincronizarDominiosPermitidos():
        headers = {"UserID": "1","Peticion":"obtenerDominiosPermitidos"}
        respuesta = obtenerRespuesta(headers)
        dominios=respuesta.read()
        if len(dominios):
            if dominios[-1]=="":
                    array_dominios=dominios.rsplit("\n")[0:-1]
            else:
                array_dominios=dominios.rsplit("\n")
            cursor.execute('delete from dominios_publicamente_permitidos')
            for fila in array_dominios:
                if fila <> "":
                    logger.log(logging.DEBUG, "Se agrego el dominio permitido: %s" % fila)
                    cursor.execute('insert into dominios_publicamente_permitidos(url) values(?)', (fila, ) )
            conexion_db.commit()

def sincronizarDominiosDenegados():
        headers = {"UserID": "1","Peticion":"obtenerDominiosDenegados"}
        respuesta = obtenerRespuesta(headers)
        dominios=respuesta.read()
        if len(dominios):
            if dominios[-1]=="":
                array_dominios=dominios.rsplit("\n")[0:-1]
            else:
                array_dominios=dominios.rsplit("\n")
            cursor.execute('delete from dominios_publicamente_denegados')
            for fila in array_dominios:
                if fila <> "":
                    logger.log(logging.DEBUG, "Se agrego el dominio denegado: %s" % fila)
                    cursor.execute('insert into dominios_publicamente_denegados(url) values(?)',(fila, ) )
            conexion_db.commit()
        else:
           logger.log(logging.DEBUG,"No hay dominios para actualizar")

def getPeriodoDeActualizacion():
        headers = {"UserID": "1","Peticion":"getPeriodoDeActualizacion"}
        respuesta = obtenerRespuesta(headers)
        return respuesta.read()


def sincronizarDominiosConServer(tiempo_actual):
        timestring=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tiempo_actual))
        sincronizarDominiosPermitidos()
        sincronizarDominiosDenegados()
        cursor.execute('update sincronizador set ultima_actualizacion=?', (tiempo_actual, ))
        conexion_db.commit()
        logger.log(logging.INFO, "Se ha sincronizado la base de datos de dominios publicamente aceptados/denegados")

#def borrarUrlsViejasCache(hora_actual, edad_max):
#    tiempo_expiracion=hora_actual-edad_max
#    timestring=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tiempo_expiracion))
#    respuesta=cursor.execute('delete from cache_urls_aceptadas where hora < ? ', (tiempo_expiracion, ))
#    conexion_db.commit()
#    respuesta=cursor.execute('delete from cache_urls_denegadas where hora < ? ', (tiempo_expiracion, ))
#    conexion_db.commit()
#    print "Se han borrado las urls viejas de cache"

# Inicio

while True:
    #obtiene el tiempo en minutos
    periodo_expiracion=getPeriodoDeActualizacion()
    logger.log(logging.INFO, "Iniciando el demonio de sincronización")
    if not periodo_expiracion:
        periodo_expiracion=1
    logger.log(logging.DEBUG, "Periodo de actualizacion: %s minuto/s" % periodo_expiracion)
    # paso de minutos a segundos el periodo de expiracion
    periodo_expiracion=int(periodo_expiracion)*60
    conexion_db = sqlite3.connect(config.PATH_DB)
    cursor=conexion_db.cursor()
    ultima_actualizacion=cursor.execute('select ultima_actualizacion from sincronizador').fetchone()[0]
    tiempo_actual=time.time()
    tiempo_transcurrido=tiempo_actual - ultima_actualizacion
    if (tiempo_transcurrido > periodo_expiracion)  :
        logger.log(logging.DEBUG,"Sincronizando dominios permitidos/dengados con servidor...")
        sincronizarDominiosConServer(tiempo_actual)
        #borrarUrlsViejasCache(tiempo_actual, periodo_expiracion)
    else:
        tiempo_restante=ultima_actualizacion + periodo_expiracion - tiempo_actual
        logger.log(logging.DEBUG, "Faltan %s minutos para que se vuelva a sincronizar" % (tiempo_restante/60))
        time.sleep(tiempo_restante)
    conexion_db.close()

