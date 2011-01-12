import SOAPpy, sys, time,  os,  sqlite3

from funciones import *

PATH_DB='/var/cache/securedfamily/securedfamily.db'

def sincronizarDominiosConServer(tiempo_actual):  
        cursor.execute('delete from dominios_publicamente_denegados')
        cursor.execute('delete from dominios_publicamente_permitidos')
        
        registro=server.getDominiosPermitidos()
        i=0
        while i <len(registro):
            cursor.execute('insert into dominios_publicamente_permitidos(tipo,url) values(?,?)',(registro[i],registro[i+1]), ) 
            i=i+2
            
        registro=server.getDominiosDenegados()
        i=0
        while i <len(registro):
            cursor.execute('insert into dominios_publicamente_denegados(tipo,url) values(?,?)',(registro[i],registro[i+1]), ) 
            i=i+2

        conexion.commit()                      
        cursor.execute('update sincronizador set ultima_actualizacion=?', (tiempo_actual, ))
        conexion.commit()          
        print "Se ha sincronizado la base de datos de dominios publicamente aceptados/denegados"

def borrarUrlsViejasCache(hora_actual, edad_max):
    tiempo_expiracion=hora_actual-edad_max
    respuesta=cursor.execute('delete from cache_urls_aceptadas where hora < ? ', (tiempo_expiracion, ))
    conexion.commit()    
    respuesta=cursor.execute('delete from cache_urls_denegadas where hora < ? ', (tiempo_expiracion, ))
    conexion.commit()
    print "Se han borrado las urls viejas de cache"    


while True:
    server = SOAPpy.SOAPProxy("http://securedfamily.no-ip.org:8081/")
    periodo_expiracion=server.getPeriodoDeActualizacion()
    conexion = sqlite3.connect(PATH_DB)
    cursor=conexion.cursor()
    ultima_actualizacion=cursor.execute('select ultima_actualizacion from sincronizador').fetchone()[0]
    tiempo_actual=time.time()
    tiempo_transcurrido=tiempo_actual - ultima_actualizacion
    if (tiempo_transcurrido > periodo_expiracion)  :
        sincronizarDominiosConServer(tiempo_actual)
        borrarUrlsViejasCache(tiempo_actual, periodo_expiracion)    
    else:
        tiempo_restante=ultima_actualizacion + periodo_expiracion - tiempo_actual
        print "Faltan %s hs para que se vuelva a sincronizar" % (tiempo_restante/60/60)
        time.sleep(tiempo_restante)
    conexion.close()
