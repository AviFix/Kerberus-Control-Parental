import MySQLdb
import urllib2

servidor = "http://localhost:8080"
#servidor = "http://kerberuscontrolparental.appspot.com"
user = 'mboscovich'
password = 'k3rb3rusCPW'

def cargarDominiosPermitidos(host='localhost', user='root', password='cr1pt0man0', db='kerberus_db'):
    conexion = MySQLdb.connect(host=host,
                                user=user,
                                passwd=password,
                                db=db,
                                charset="utf8", use_unicode=True)
    cursor = conexion.cursor()
    cursor.execute('select distinct url from dominios where estado=1 limit 9850')
    respuesta = cursor.fetchall()
    contador = 0
    ultimo = 7000
    for fila in respuesta:
        contador += 1
        if contador > ultimo:
            dominio = '%s/agregarDominio/%s/Permitido' % (servidor, fila[0])
            req = urllib2.Request(dominio)
            respuesta = urllib2.urlopen(req, timeout=60).read()
            print "%s: %s" % (contador,respuesta)

    conexion.close()
    print "Listo."

def cargarDominiosDenegados(host='localhost', user='root', password='cr1pt0man0', db='kerberus_db'):
    conexion = MySQLdb.connect(host=host,
                                user=user,
                                passwd=password,
                                db=db,
                                charset="utf8", use_unicode=True)
    cursor = conexion.cursor()
    cursor.execute('select distinct url from dominios where estado=2  limit 150')
    respuesta = cursor.fetchall()
    contador = 0
    ultimo = 150
    for fila in respuesta:
        contador += 1
        if contador > ultimo:
            dominio = '%s/agregarDominio/%s/Denegado' % (servidor, fila[0])
            req = urllib2.Request(dominio)
            respuesta = urllib2.urlopen(req, timeout=60).read()
            print "%s: %s" % (contador,respuesta)

    conexion.close()
    print "Listo."

if __name__ == '__main__':
    #peticion = '%s/administrar/cachearTodosLosDominios/%s/%s' % (servidor, user, password)
    #req = urllib2.Request(peticion)
    #respuesta = urllib2.urlopen(req, timeout=6000).read()
    #print "%s: %s" % ('Recargando cache: ',respuesta)
    print "Cargando Dominios Denegados:"
    cargarDominiosDenegados()
    print "Cargando Dominios Permitidos:"
    cargarDominiosPermitidos()
    print "Fin"