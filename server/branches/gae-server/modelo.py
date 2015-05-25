from google.appengine.ext import ndb
from google.appengine.api import memcache

import datetime
import hashlib
import logging
import pickle
import time
import configuracion

#funciones
def md5sum(t):
    try:
        return hashlib.md5(t.encode('utf-8')).hexdigest()
    except:
        print "No se pudo obtener el hash md5 de %s" % t


class Dominio(ndb.Model):
    url = ndb.StringProperty(required=True)
    estado = ndb.StringProperty(required=True,
                                choices=['Permitido', 'Denegado', 'Gris'])
    ultima_revision = ndb.DateTimeProperty(auto_now=True)
    verificador = ndb.StringProperty(default='Filtrado por DNS',
                                         choices=['Filtrado por DNS',
                                                'Filtrado de contenidos',
                                                'Manual'])

    @classmethod
    def borrarTodosLosDominios(cls):
        dominios_key = cls.query().fetch(keys_only=True)
        ndb.delete_multi(dominios_key)

    @classmethod
    def obtenerDominios(cls, estado=None, ultima_sync=0):
        tiempo = datetime.datetime.fromtimestamp(float(ultima_sync))
        hora_actual = time.time()

        ultima_recarga_dominios = memcache.get('UltimaRecargaDominios')
        dominios = memcache.get('Dominios')

        if ultima_recarga_dominios is None or dominios is None:
            dominios = cls.query().fetch(configuracion.CANTIDAD_MAXIMA_DOMINIOS)
            memcache.set(key='Dominios', value=dominios)
            memcache.set(key='UltimaRecargaDominios', value=hora_actual)
        else:
            tiempo_transcurrido = hora_actual - float(ultima_recarga_dominios)
            if tiempo_transcurrido > configuracion.TIEMPO_RECARGA_DOMINIOS:
                dominios = cls.query().fetch(configuracion.CANTIDAD_MAXIMA_DOMINIOS)
                memcache.set(key='Dominios', value=dominios)
                memcache.set(key='UltimaRecargaDominios', value=hora_actual)

        respuesta = []
        for dominio in dominios:
            if dominio.estado == estado and dominio.ultima_revision >= tiempo:
                respuesta.append(dominio)

        del dominios

        return respuesta


    @classmethod
    def yaEstaCargado(cls, url, estado):
        clave = "Dominio.%s" % url
        existe = memcache.get(clave)
        if not existe:
            dominio = cls.query().filter(cls.url == url).get()
            if not dominio:
                return False
            else:
                memcache.set(key=clave, value=dominio)
                return True
        else:
            return True

    @classmethod
    def dominioAprendido(cls, url):
        dominio = cls.query().filter(cls.url == url).get()
        if dominio is None:
            return False
        else:
            return dominio

class Parametro(ndb.Model):
    clave = ndb.StringProperty(required=True)
    valor = ndb.StringProperty(required=True)

    @classmethod
    def yaEstaCargado(cls, clave,
                        ancestor_key=ndb.Key("Parametro", 'Parametros')):
        existe = cls.query(ancestor=ancestor_key).filter(
                            cls.clave == clave).get()
        if not existe:
            return False
        else:
            return True

    @classmethod
    def getParametro(cls, parametro,
                        ancestor_key=ndb.Key("Parametro", 'Parametros')):
        respuesta = cls.query(ancestor=ancestor_key).filter(
                                cls.clave == parametro).get()
        return respuesta.valor


class Usuario(ndb.Model):
    user_id = ndb.IntegerProperty(required=True)
    server_id = ndb.IntegerProperty(required=True, default=1)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    idioma = ndb.StringProperty(choices=['es', 'en'])
    nombre = ndb.StringProperty()
    version = ndb.StringProperty()
    ultima_ip = ndb.StringProperty()
    dominios_permitidos = ndb.StringProperty(repeated=True)
    dominios_denegados = ndb.StringProperty(repeated=True)

    @classmethod
    def usuarioRegistrado(cls, user_id=0, server_id=4, email='',
            ancestor_key=ndb.Key("Usuario", 'Usuarios')):
        respuesta = cls.query(ancestor=ancestor_key).filter(
                        cls.user_id == int(user_id),
                        cls.server_id == int(server_id),
                        cls.email == email
                        ).get()
        if respuesta is None:
            return False
        else:
            return True

    @classmethod
    def getNewID(cls, server_id=4, ancestor_key=ndb.Key("Usuario", 'Usuarios')):
        respuesta = cls.query(ancestor=ancestor_key).filter(
                        cls.server_id == int(server_id),
                        ).order(-cls.user_id).get()
        if not respuesta:
            new_id = 1
        else:
            new_id = respuesta.user_id + 1
        return new_id

    @classmethod
    def cantidadDeUsuarios(cls, ancestor_key=ndb.Key("Usuario", 'Usuarios')):
        respuesta = cls.query(ancestor=ancestor_key).count()
        return respuesta

    @classmethod
    def obtenerUsuario(cls, user_id, server_id, ancestor_key=ndb.Key("Usuario", 'Usuarios')):
        resultado = cls.query(ancestor=ancestor_key).filter(
                                cls.user_id == int(user_id),
                                cls.server_id == int(server_id),
                                ).get()
        if resultado is not None:
            respuesta = resultado
        else:
            respuesta = False

        return respuesta

    @classmethod
    def obtenerEmail(cls, user_id, server_id, ancestor_key=ndb.Key("Usuario", 'Usuarios')):
        resultado = cls.query(ancestor=ancestor_key).filter(
                                cls.user_id == int(user_id),
                                cls.server_id == int(server_id),
                                ).get()
        if resultado is not None:
            respuesta = resultado.email
        else:
            respuesta = False

        return respuesta

    @classmethod
    def cambiarPassword(
        cls, user_id, server_id, password_vieja, password_nueva,
        ancestor_key=ndb.Key("Usuario", 'Usuarios')
        ):
        resultado = cls.query(ancestor=ancestor_key).filter(
                                cls.user_id == int(user_id),
                                cls.server_id == int(server_id),
                                ).fetch()
        respuesta = False
        if resultado is not None:
            for user in resultado:
                if md5sum(user.password) == password_vieja:
                    user.password = password_nueva
                    user.put()
                    respuesta = True

        return respuesta

    @classmethod
    def eliminar(cls, user_id=0, server_id=0, credencial='',
                    ancestor_key=ndb.Key("Usuario", 'Usuarios')):
        resultado = cls.query(ancestor=ancestor_key).filter(
                                cls.user_id == int(user_id),
                                cls.server_id == int(server_id)
                                ).fetch()
        respuesta = False
        if resultado is not None:
            for user in resultado:
                if md5sum(user.password) == credencial:
                    user.key.delete()
                    respuesta = True

        return respuesta

class cliente(ndb.Model):
    pass


