from google.appengine.ext import ndb
from google.appengine.api import memcache, urlfetch

import webapp2
import time
import urllib2
import hashlib

from modelo import Dominio
from modelo import Parametro
from modelo import Usuario
from correo import Correo
import configuracion


def md5sum(t):
    try:
        return hashlib.md5(t.encode('utf-8')).hexdigest()
    except:
        print "No se pudo obtener el hash md5 de %s" % t


def agregarDominio(dominio, estado):
    cant_dominios = memcache.get('cantidadDeDominios')
    if cant_dominios is None:
        cant_dominios = Dominio.query().count()
        memcache.set(key='cantidadDeDominios', value=int(cant_dominios))

    if cant_dominios >= configuracion.CANTIDAD_MAXIMA_DOMINIOS:
        dominio_mas_viejo = Dominio.query().order(Dominio.ultima_revision).get()
        dominio_mas_viejo.key.delete()
        memcache.decr('cantidadDeDominios')

    nuevo_dominio = Dominio()
    nuevo_dominio.url = dominio
    nuevo_dominio.estado = estado
    nuevo_dominio.verificador = 'Filtrado por DNS'
    nuevo_dominio.put()
    memcache.incr('cantidadDeDominios')


class Peticion(webapp2.RequestHandler):

    def getParametro(self, parametro=None):
        try:
            param = self.request.headers[parametro]
            unquoteables = ('Nombre', 'Email', 'Password')
            if parametro in unquoteables:
                param = unicode(urllib2.unquote(param), 'utf-8')
        except:
            param = None
        return param

    def obtenerRespuesta(self, headers, timeout=20):
        # Agrego los datos particulares del cliente
        headers['UserID'] = 1
        headers['ServerID'] = 5
        headers['Version'] = '1.1'
        headers['Credencial'] = md5sum(u'k3rb3rusCPW')
        url = 'https://validador2.kerberus.com.ar'
        respuesta = urlfetch.fetch(
            url,
            headers=headers,
            validate_certificate=False,
             deadline=60)
        del headers
        return respuesta

    def validarRemotamente(self, url):
        headers = {}
        headers['URL'] = url
        headers['Peticion'] = 'validarUrl'
        respuesta = self.obtenerRespuesta(headers)
        if respuesta.status_code == 200:
            if respuesta.content == '':
                return True
        return False

    def get(self):

        userId = self.getParametro('UserID')
        serverId = self.getParametro('ServerID')
        peticion = self.getParametro('Peticion')
        version = self.getParametro('Version')

        #print "UserID: %s\nServerID:%s\nPeticion: %s\nVersion: %s\n" \
        #    % (userId, serverId, peticion, version)

        if peticion and peticion.startswith("obtenerDominios"):
            ultima_sync = self.getParametro('UltimaSync')
            adminDominios = Dominio()
            if peticion.endswith("Denegados"):
                resultado = adminDominios.obtenerDominios(
                    estado='Denegado',
                    ultima_sync=ultima_sync
                    )
            else:
                resultado = adminDominios.obtenerDominios(
                    estado='Permitido',
                    ultima_sync=ultima_sync
                    )

            dominios = ''
            for dominio in resultado:
                dominios += '%s\n' % dominio.url

            del resultado
            del adminDominios

            respuesta = dominios

        elif peticion == "chequearActualizaciones":
            plataforma = self.getParametro('plataforma')
            if plataforma == 'Windows':
                respuesta = 'No,No'
            elif plataforma == 'Linux':
                respuesta = 'No,No'

        elif peticion == "eliminarUsuario":
            credencial = self.getParametro('Credencial')

            nombre = self.getParametro('Nombre')
            email = self.getParametro('Email')

            pais = self.getParametro('X-AppEngine-Country')
            region = self.getParametro('X-AppEngine-Region')
            ciudad = self.getParametro('X-AppEngine-City')
            latitud_longitud = self.getParametro('X-AppEngine-CityLatLong')

            respuesta = Usuario.eliminar(
                user_id=userId,
                server_id=serverId,
                credencial=credencial
                )
            if respuesta:
                email_sender = Correo()
                cant_users_reg = Usuario.cantidadDeUsuarios()
                email_sender.notificarBajaUsuario(
                    cant_users_reg,
                    nombre,
                    email,
                    pais,
                    region,
                    ciudad,
                    latitud_longitud
                    )

        elif peticion == "recordarPassword":
            usuario = Usuario.obtenerUsuario(userId, serverId)
            if usuario:
                email = Correo()
                email.enviarCorreoRecordarPassword(
                    usuario.email,
                    usuario.password,
                    usuario.nombre,
                    usuario.idioma)
                respuesta = 'Recordada'
            else:
                respuesta = 'No recordada'

        elif peticion == "estaRespondiendo":
            respuesta = 'Online'

        elif peticion == "registrarUsuario":
            nombre = self.getParametro('Nombre')
            email = self.getParametro('Email')
            password = self.getParametro('Password')
            idioma = self.getParametro('Idioma')

            pais = self.getParametro('X-AppEngine-Country')
            region = self.getParametro('X-AppEngine-Region')
            ciudad = self.getParametro('X-AppEngine-City')
            latitud_longitud = self.getParametro('X-AppEngine-CityLatLong')

            if idioma is None:
                idioma = 'es'
            server_id = 4
            user_id = Usuario.getNewID(server_id=server_id)
            new_user = Usuario(parent=ndb.Key("Usuario", 'Usuarios'))
            new_user.nombre = nombre
            new_user.email = email
            new_user.password = password
            new_user.version = version
            new_user.idioma = idioma
            new_user.user_id = user_id
            new_user.server_id = server_id
            new_user.ultima_ip = self.request.remote_addr
            new_user.put()
            email = Correo()
            email.enviarCorreoBienvenida(new_user.email, nombre, password,
                idioma)
            cant_users_reg = Usuario.cantidadDeUsuarios()
            email.notificarNuevoUsuario(cant_users_reg, new_user.email,
                nombre,
                password,
                idioma,
                pais,
                region,
                ciudad,
                latitud_longitud,
                new_user.ultima_ip)

            respuesta = "%s,%s" % (user_id, server_id)

        elif peticion == "obtenerServidores":
            # OJO que el cliente hoy usa https!!!
            respuesta = 'kerberuscontrolparental.appspot.com:443\n'\
                            'validador4.kerberus.com.ar:80'

        elif peticion == "getPeriodoDeActualizacion":
            respuesta = Parametro.getParametro('tiempo_actualizacion_clientes')

        elif peticion == "getHoraServidor":
            respuesta = time.time()

        elif peticion == "informarNuevaPassword":
            user_id = self.getParametro('UserID')
            server_id = self.getParametro('ServerID')
            password_nueva = self.getParametro('PasswordNueva')
            password_vieja = self.getParametro('PasswordVieja')
            nombre = self.getParametro('Nombre')
            idioma = self.getParametro('Idioma')

            password_nueva = unicode(urllib2.unquote(password_nueva), 'utf-8')
            respuesta = Usuario.cambiarPassword(
                userId, serverId, password_vieja, password_nueva
                )
            if respuesta:
                email = Usuario.obtenerEmail(userId, serverId)
                email_sender = Correo()
                email_sender.enviarCorreoNuevaPassword(
                    email,
                    password_nueva,
                    nombre,
                    idioma)
                respuesta = 'Informada'
            else:
                respuesta = 'No Informada'

        elif peticion == "getPeriodoDeRecargaCompleta":
            respuesta = Parametro.getParametro(
                'tiempo_de_recarga_completa_clientes'
                )

        elif peticion == "usuarioRegistrado":
            email = self.getParametro('Email')
            respuesta = Usuario.usuarioRegistrado(userId, serverId, email)

        elif peticion == "validarUrl":
            url = self.getParametro('URL')
            dominio = url.split('/')[2]
            memcacheado = memcache.get(dominio)
            if memcacheado is not None:
                if memcacheado == 'Permitido':
                    # OJO que el cliente espera una respuesta vacia si esta
                    # permitido!!!
                    # Devolver '' o devolver 204 es lo mismo, porque
                    # el codigo 204 http significa 'sin respuesta', por eso
                    # devuelvo un 204 pongo respuesta = 'Permitido', para que
                    # se guarde el estado en la base de ese modo.
                    respuesta = 'Permitido'
                    self.response.status_int = 204
                else:
                    respuesta = 'Denegado'
                    self.response.status_int = 200
            else:
                dominio_aprendido = Dominio.dominioAprendido(dominio)
                if dominio_aprendido:
                    if dominio_aprendido.estado == 'Permitido':
                        respuesta = 'Permitido'
                        self.response.status_int = 204
                    else:
                        respuesta = 'Denegado'
                        self.response.status_int = 200
                    memcache.set(
                        key=dominio_aprendido.url,
                        value=dominio_aprendido.estado
                        )
                else:
                    valido = self.validarRemotamente(url)
                    if valido:
                        respuesta = 'Permitido'
                        self.response.status_int = 204
                        # Solo persisto en la base los dominios permitidos
                        # los denegados no son tan recurrentes y por tanto
                        # no importan. Ademas, asi evito falsos positivos
                        agregarDominio(dominio, 'Permitido')
                    else:
                        respuesta = 'Denegado'
                        self.response.status_int = 200

                    memcache.set(key=dominio, value=respuesta)

        elif peticion == "consulta":
            pass
        else:
            respuesta = "Peticion invalida"

        self.response.write(respuesta)
        del respuesta


class Administracion(webapp2.RequestHandler):

    def getParametro(self, parametro=None):
        try:
            param = self.request.headers[parametro]
            unquoteables = ('Nombre', 'Email', 'Password')
            if parametro in unquoteables:
                param = unicode(urllib2.unquote(param), 'utf-8')
        except:
            param = None
        return param

    def get(self, operacion, usuario, password):
        if (usuario != 'mboscovich') and (password != 'k3rb3rusCPW'):
            respuesta = 'Usuario o password incorrecta'
        else:
            if operacion == 'borrarTodosLosDominios':
                Dominio.borrarTodosLosDominios()
                respuesta = "Listo"
            elif operacion == 'agregarUsuario':
                user_id = int(self.getParametro('UserID'))
                server_id = int(self.getParametro('ServerID'))
                email = self.getParametro('Email')

                if Usuario.usuarioRegistrado(user_id, server_id, email):
                    respuesta = "El usuario ya esta cargado. "\
                    "UserID: %s, ServerID: %s, "\
                    "email: %s" % (user_id, server_id, email)
                else:
                    new_user = Usuario(parent=ndb.Key("Usuario", 'Usuarios'))
                    new_user.nombre = self.getParametro('Nombre')
                    new_user.email = email
                    new_user.password = self.getParametro('Password')
                    new_user.version = self.getParametro('Version')
                    new_user.idioma = self.getParametro('Idioma')
                    new_user.user_id = user_id
                    new_user.server_id = server_id
                    new_user.ultima_ip = self.getParametro('UltimaIP')
                    new_user.put()
                    respuesta = "Usuario agregado correctamente. "\
                    "UserID: %s, ServerID: %s, "\
                    "email: %s" % (user_id, server_id, email)

        self.response.write(respuesta)


class CargarDominio(webapp2.RequestHandler):
    """Permite agregar dominios
        Formato: /agregarDominio/URL/(Permitido|Denegado)
    """
    def get(self, url, estado):
        respuesta = "Agregar el dominio: %s<br>Estado: %s" % \
        (url, estado)
        existe = Dominio.yaEstaCargado(url, estado)
        if not existe:
            dominio = Dominio(parent=ndb.Key("Dominio", 'Dominios'))
            dominio.url = url
            dominio.estado = estado
            dominio.verificador = 'Manual'
            dominio.put()
            respuesta = "Se agrego correctamente " + url
        else:
            respuesta = "Ya existe " + url
        self.response.write(respuesta)

# inicializacion de parametros
if not Parametro.yaEstaCargado('tiempo_actualizacion_clientes'):
    param = Parametro(parent=ndb.Key("Parametro", 'Parametros'))
    param.clave = 'tiempo_actualizacion_clientes'
    param.valor = '4320'
    param.put()
if not Parametro.yaEstaCargado('tiempo_de_recarga_completa_clientes'):
    param = Parametro(parent=ndb.Key("Parametro", 'Parametros'))
    param.clave = 'tiempo_de_recarga_completa_clientes'
    param.valor = '86400'
    param.put()
if not Dominio.yaEstaCargado(url='permitido.com', estado='Permitido'):
    dom = Dominio()
    dom.url = 'permitido.com'
    dom.estado = 'Permitido'
    dom.verificador = 'Manual'
    dom.put()
if not Dominio.yaEstaCargado(url='denegado.com', estado='Denegado'):
    dom = Dominio()
    dom.url = 'denegado.com'
    dom.estado = 'Denegado'
    dom.verificador = 'Manual'
    dom.put()

if Usuario.cantidadDeUsuarios() == 0:
    user_id = Usuario.getNewID(server_id=4)
    new_user = Usuario(parent=ndb.Key("Usuario", 'Usuarios'))
    new_user.nombre = 'Usuario Inicial'
    new_user.email = 'maximiliano@kerberus.com.ar'
    new_user.password = 'k3rb3rusCPW'
    new_user.version = '0'
    new_user.idioma = 'es'
    new_user.user_id = user_id
    new_user.server_id = 4
    new_user.ultima_ip = '127.0.0.1'
    new_user.put()

    user_id = Usuario.getNewID(server_id=4)
    new_user = Usuario(parent=ndb.Key("Usuario", 'Usuarios'))
    new_user.nombre = 'Usuario Inicial English'
    new_user.email = 'maximiliano@kerberus.com.ar'
    new_user.password = 'k3rb3rusCPW'
    new_user.version = '0'
    new_user.idioma = 'en'
    new_user.user_id = user_id
    new_user.server_id = 4
    new_user.ultima_ip = '127.0.0.1'
    new_user.put()

    user_id = Usuario(parent=ndb.Key("Usuario", 'Usuarios'))
    new_user.nombre = 'Maximiliano Boscovich'
    new_user.email = 'maximiliano@kerberus.com.ar'
    new_user.password = 'abril22'
    new_user.version = '1.1'
    new_user.idioma = 'es'
    new_user.user_id = 701
    new_user.server_id = 1
    new_user.ultima_ip = '127.0.0.1'
    new_user.put()

application = webapp2.WSGIApplication([
    ('/administrar/(\w.*)/(\w.*)/(\w.*)/.*', Administracion),
    ('/agregarDominio/(\w.*)/(Permitido|Denegado)', CargarDominio),
    ('/.*', Peticion),

], debug=False)
