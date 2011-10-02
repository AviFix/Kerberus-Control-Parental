# -*- coding: utf-8 -*-

import sys, time, os, sqlite3, httplib, platform

from funciones import *

if  platform.uname()[0] == 'Linux':
    PATH_DB='/var/cache/kerberus/kerberus.db'
    LOG_FILENAME='/var/log/kerberus-cliente.log'
else:
    import  _winreg
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
    PATH_DB=_winreg.QueryValueEx(key,'kerberus-common')[0]+'\kerberus.db'
    LOG_FILENAME=_winreg.QueryValueEx(key,'kerberus-common')[0]+'\kerberus-sync.log'

sys.path.append('conf')
import config, urllib2

def sincronizarDominiosPermitidos():
        server_sync="http://%s:%s" % (config.SERVER_IP,config.SERVER_SINC_PORT)
        if config.USAR_PROXY:
            url_proxy="http://%s:%s" % (config.PROXY_IP,config.PROXY_PORT)
            print "Utilizando el proxy %s" % url_proxy
            proxy={'http':url_proxy, 'https': url_proxy}
            proxy_handler=urllib2.ProxyHandler(proxy)
            opener=urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)
        heads = {"UserID": "1","Peticion":"obtenerDominiosPermitidos"}
        req = urllib2.Request(server_sync, headers=heads)
        respuesta = urllib2.urlopen(req)
        dominios=respuesta.read()
        if len(dominios):
            if dominios[-1]=="":
                    array_dominios=dominios.rsplit("\n")[0:-1]
            else:
                array_dominios=dominios.rsplit("\n")
            cursor.execute('delete from dominios_publicamente_permitidos')
            for fila in array_dominios:
                if fila <> "":
                    print "Se agrego el dominio permitido: %s" % fila
                    cursor.execute('insert into dominios_publicamente_permitidos(url) values(?)', (fila, ) )
            conexion_db.commit()

def sincronizarDominiosDenegados():
        server_sync="http://%s:%s" % (config.SERVER_IP,config.SERVER_SINC_PORT)
        if config.USAR_PROXY:
            url_proxy="http://%s:%s" % (config.PROXY_IP,config.PROXY_PORT)
            print "Utilizando el proxy %s" % url_proxy
            proxy={'http':url_proxy, 'https': url_proxy}
            proxy_handler=urllib2.ProxyHandler(proxy)
            opener=urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)
        heads = {"UserID": "1","Peticion":"obtenerDominiosDenegados"}
        req = urllib2.Request(server_sync, headers=heads)
        respuesta = urllib2.urlopen(req)
        dominios=respuesta.read()
        if len(dominios):
            if dominios[-1]=="":
                array_dominios=dominios.rsplit("\n")[0:-1]
            else:
                array_dominios=dominios.rsplit("\n")
            cursor.execute('delete from dominios_publicamente_denegados')
            for fila in array_dominios:
                if fila <> "":
                    print "Se agrego el dominio denegado: %s" % fila
                    cursor.execute('insert into dominios_publicamente_denegados(url) values(?)',(fila, ) )
            conexion_db.commit()
        else:
            print "No hay dominios para actualizar"

def getPeriodoDeActualizacion():
        server_sync="http://%s:%s" % (config.SERVER_IP,config.SERVER_SINC_PORT)
        if config.USAR_PROXY:
            url_proxy="http://%s:%s" % (config.PROXY_IP,config.PROXY_PORT)
            print "Utilizando el proxy %s" % url_proxy
            proxy={'http':url_proxy, 'https': url_proxy}
            proxy_handler=urllib2.ProxyHandler(proxy)
            opener=urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)
        heads = {"UserID": "1","Peticion":"getPeriodoDeActualizacion"}
        req = urllib2.Request(server_sync, headers=heads)
        respuesta = urllib2.urlopen(req)
        return respuesta.read()

def sincronizarDominiosConServer(tiempo_actual):
        timestring=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tiempo_actual))
        sincronizarDominiosPermitidos()
        sincronizarDominiosDenegados()
        cursor.execute('update sincronizador set ultima_actualizacion=?', (tiempo_actual, ))
        conexion_db.commit()
        #print "Se ha sincronizado la base de datos de dominios publicamente aceptados/denegados"

#def borrarUrlsViejasCache(hora_actual, edad_max):
#    tiempo_expiracion=hora_actual-edad_max
#    timestring=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tiempo_expiracion))
#    respuesta=cursor.execute('delete from cache_urls_aceptadas where hora < ? ', (tiempo_expiracion, ))
#    conexion_db.commit()
#    respuesta=cursor.execute('delete from cache_urls_denegadas where hora < ? ', (tiempo_expiracion, ))
#    conexion_db.commit()
#    print "Se han borrado las urls viejas de cache"


while True:
    #obtiene el tiempo en minutos
    periodo_expiracion=getPeriodoDeActualizacion()
    if not periodo_expiracion:
        periodo_expiracion=1
#    print "Periodo de actualizacion %s minuto/s" % periodo_expiracion
    # paso de minutos a segundos el periodo de expiracion
    periodo_expiracion=int(periodo_expiracion)*60
    conexion_db = sqlite3.connect(PATH_DB)
    cursor=conexion_db.cursor()
    ultima_actualizacion=cursor.execute('select ultima_actualizacion from sincronizador').fetchone()[0]
    tiempo_actual=time.time()
    tiempo_transcurrido=tiempo_actual - ultima_actualizacion
    if (tiempo_transcurrido > periodo_expiracion)  :
        #print "Sincronizando dominios permitidos/dengados con servidor..."
        sincronizarDominiosConServer(tiempo_actual)
        #borrarUrlsViejasCache(tiempo_actual, periodo_expiracion)
    else:
        tiempo_restante=ultima_actualizacion + periodo_expiracion - tiempo_actual
#        print "Faltan %s minutos para que se vuelva a sincronizar" % (tiempo_restante/60)
        time.sleep(tiempo_restante)
    conexion_db.close()
