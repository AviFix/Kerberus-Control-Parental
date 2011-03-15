# -*- coding: utf-8 -*-

import SOAPpy, sys, time,  os,  sqlite3, httplib
 
from funciones import *

PATH_DB='/var/cache/securedfamily/securedfamily.db'
SERVER="securedfamily.no-ip.org:8081"


def sincronizarDominiosPermitidos():
        cursor.execute('delete from dominios_publicamente_permitidos')
        conexion=httplib.HTTPConnection(SERVER)
        headers = {"UserID": "1","Peticion":"obtenerDominiosPermitidos"}
        conexion.request("GET", "/", "", headers)
        respuesta=conexion.getresponse()
        dominios=respuesta.read()
        array_dominios=dominios.rsplit("\n")          
        for fila in array_dominios:
            registro=fila.split(',')
            if len(registro)>1:
                cursor.execute('insert into dominios_publicamente_permitidos(tipo,url) values(?,?)',(registro[0],registro[1]), ) 
        conexion_db.commit()        

def sincronizarDominiosDenegados():
        cursor.execute('delete from dominios_publicamente_denegados')
        conexion=httplib.HTTPConnection(SERVER)
        headers = {"UserID": "1","Peticion":"obtenerDominiosDenegados"}
        conexion.request("GET", "/", "", headers)
        respuesta=conexion.getresponse()
        dominios=respuesta.read()
        if dominios[-1]=="":
            array_dominios=dominios.rsplit("\n")[0:-1]
        else:
            array_dominios=dominios.rsplit("\n")
        for fila in array_dominios:
            registro=fila.split(',')
            if len(registro)>1:
                cursor.execute('insert into dominios_publicamente_denegados(tipo,url) values(?,?)',(registro[0],registro[1]), ) 
        conexion_db.commit()        

def getPeriodoDeActualizacion():
        conexion=httplib.HTTPConnection(SERVER)
        headers = {"UserID": "1","Peticion":"getPeriodoDeActualizacion"}
        conexion.request("GET", "/", "", headers)
        respuesta=conexion.getresponse()
        return respuesta.read()
        
def sincronizarDominiosConServer(tiempo_actual):  
        timestring=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tiempo_actual))
        sincronizarDominiosPermitidos()
        sincronizarDominiosDenegados()
        cursor.execute('update sincronizador set ultima_actualizacion=?', (tiempo_actual, ))
        conexion_db.commit()          
        print "Se ha sincronizado la base de datos de dominios publicamente aceptados/denegados"

def borrarUrlsViejasCache(hora_actual, edad_max):
    tiempo_expiracion=hora_actual-edad_max
    timestring=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tiempo_expiracion))
    respuesta=cursor.execute('delete from cache_urls_aceptadas where hora < ? ', (tiempo_expiracion, ))
    conexion_db.commit()    
    respuesta=cursor.execute('delete from cache_urls_denegadas where hora < ? ', (tiempo_expiracion, ))
    conexion_db.commit()
    print "Se han borrado las urls viejas de cache"    


while True:
    #obtiene el tiempo en minutos
    periodo_expiracion=getPeriodoDeActualizacion()
    # paso de minutos a segundos el periodo de expiracion
    periodo_expiracion=int(periodo_expiracion)*60
    conexion_db = sqlite3.connect(PATH_DB)
    cursor=conexion_db.cursor()
    ultima_actualizacion=cursor.execute('select ultima_actualizacion from sincronizador').fetchone()[0]
    tiempo_actual=time.time()
    tiempo_transcurrido=tiempo_actual - ultima_actualizacion
    if (tiempo_transcurrido > periodo_expiracion)  :
        print "Sincronizando dominios permitidos/dengados con servidor..."
        sincronizarDominiosConServer(tiempo_actual)
        borrarUrlsViejasCache(tiempo_actual, periodo_expiracion)    
    else:
        tiempo_restante=ultima_actualizacion + periodo_expiracion - tiempo_actual
        print "Faltan %s minutos para que se vuelva a sincronizar" % (tiempo_restante/60)
        time.sleep(tiempo_restante)
    conexion_db.close()
