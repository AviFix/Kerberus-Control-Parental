import MySQLdb
import urllib2

#servidor = "http://localhost:80"
servidor = "http://kerberuscontrolparental.appspot.com"

def agregarUsuarios(host='localhost', user='root', password='cr1pt0man0', db='kerberus_db'):
    conexion = MySQLdb.connect(host=host,
                                user=user,
                                passwd=password,
                                db=db,
                                charset="utf8", use_unicode=True)
    cursor = conexion.cursor()
    cursor.execute(
        'select id, server_id, email, ultima_ip, password, nombre, '\
        'version, idioma from usuarios')
    respuesta = cursor.fetchall()
    for usuario in respuesta:
        id, server_id, email, ultima_ip, password, nombre, version, idioma = usuario
        headers = {}
        headers['UserID'] = id
        headers['ServerID'] = server_id
        headers['Email'] = urllib2.quote(email.encode('utf-8'))
        headers['UltimaIP'] = ultima_ip
        headers['Password'] = urllib2.quote(password.encode('utf-8'))
        headers['Nombre'] = urllib2.quote(nombre.encode('utf-8'))
        headers['Version'] = version

        if idioma == 'None' or idioma is None:
            idioma = 'es'
        headers['Idioma'] = idioma

        url = '%s/administrar/agregarUsuario/%s/%s/' % (servidor, 'mboscovich', 'k3rb3rusCPW')
        print url
        req = urllib2.Request(url, headers=headers)
        respuesta = urllib2.urlopen(req, timeout=60).read()
        print "Ejecutando: %s\nRespuesta: %s" % (url, respuesta)

    conexion.close()
    print "Listo."

if __name__ == '__main__':
    print "Agregando usuarios:"
    agregarUsuarios()
    print "Fin"