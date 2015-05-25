import urllib2
import hashlib

def obtenerRespuesta(headers, server):
    proxy = {}
    proxy_handler = urllib2.ProxyHandler(proxy)
    auth_handler = urllib2.HTTPBasicAuthHandler()
    auth_handler.add_password('realm', 'Kerberus', 'test', 'test')
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
#    opener2 = urllib2.build_opener(proxy_handler)
#    urllib2.install_opener(opener2)
    headers['Version'] = '1.1'
    headers['Nombre'] = 'Prueba'
#    credencial = hashlib.md5('k3rb3r4sk3rb3r4s').hexdigest()
#    headers['Credencial'] = credencial
    print "Headers enviados:\n"
    print headers

    req = urllib2.Request(server, headers=headers)
    timeout = 10
    respuesta = urllib2.urlopen(req, timeout=timeout).read()
    print ""
    return respuesta


def estaRespondiendoSincronizador(server_id, ip, port):
    """Testea si esta respondiendo el sincronizador. Se le pasa server_id,ip"""\
    """y puerto"""
    server = "http://%s:%s" % (ip, port)
    headers = {"ServerID": server_id, "Peticion": "estaRespondiendo"}

    respuesta = obtenerRespuesta(headers, server)
    print ""
    print "Respuesta recibida: %s" % respuesta

def estaRespondiendoServer(user_id, server_id, ip, port):
    server = "http://%s:%s" % (ip, port)
    headers = {
        "UserID": user_id,
        "ServerID": server_id,
        "Peticion": "estaRespondiendo"
        }
    respuesta = obtenerRespuesta(headers, server)
    print ""
    print "Respuesta recibida: %s" % respuesta


def obtenerHoraServidor(self):
    """Obtiene la hora del servidor. Devuelve en segundos"""
    headers = {
        "Peticion": "getHoraServidor",
        "Version": "1.0",
        "Plataforma": "Windows",
        "UserID": '1',
        "ServerID": '1'}
    respuesta = self.obtenerRespuesta(headers)
    return respuesta


def cambiarPassword(user_id, server_id, password, ip, port):
    server = "http://%s:%s" % (ip, port)
    headers = {
        "X-Forwarded-For": '10.0.0.3',
        "Version": "1.0",
        "Plataforma": "Windows",
        "UserID": user_id,
        "ServerID": server_id,
        "Peticion": "informarNuevaPassword",
        "Password": password}

    respuesta = obtenerRespuesta(headers, server)
    print ""
    print "Respuesta recibida: %s" % respuesta

def autenticar(user_id, server_id, credencial, ip, port):
    server = "http://%s:%s" % (ip, port)
    headers = {
        "X-Forwarded-For": '10.0.0.3',
        "Version": "1.1",
        "Plataforma": "Windows",
        "UserID": user_id,
        "ServerID": server_id,
        "Peticion": "autenticar",
        "Credencial": credencial}

    respuesta = obtenerRespuesta(headers, server)
    print ""
    print "Respuesta recibida: %s" % respuesta
