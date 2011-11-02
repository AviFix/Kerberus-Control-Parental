# -*- coding: utf-8 -*-

"""Modulo que carga la configuracion particular del usuario ingresado"""

# Modulos externos
import re, sqlite3, time, sys, urllib2, httplib, logging

# Modulos propios
sys.path.append('../conf')
import config
import funciones
import servidores

logger = funciones.logSetup (config.LOG_FILENAME, config.LOGLEVEL, config.LOG_SIZE_MB, config.LOG_CANT_ROTACIONES,"usuario")

# Clase
class Usuario:
    def __init__(self, usuario):
        logger.log(logging.INFO,"Conectado como usuario: %s" % usuario)
        self.nombre=usuario
        self.servidor=servidores.Servidor()
        conexion = sqlite3.connect(config.PATH_DB)
        self.cursor=conexion.cursor()
        self.id, self.es_admin=self.getUserIdAndAdmin(usuario)
        self.recargarDominiosDenegados()
        self.recargarDominiosPermitidos()
        self.recargarDominiosPublicamentePermitidos()
        self.recargarDominiosPublicamenteDenegados()
        self.recargarCacheAceptadas()
        self.recargarCacheDenegadas()
        self.ultimaRecargaDeDominios=0
        self.recargarPeriodoDeActualizacion()
        #conexion.close()
        #del(self.cursor)
        self.buffer_denegadas=[]
        self.buffer_aceptadas=[]

    def __str__(self):
        return self.nombre

    def __eq__(self, nombre):
        if self.nombre == nombre:
            return True
        return False

    def __getattribute__(self, attr):
        return object.__getattribute__(self, attr)

#    def __del__(self):
#        self.conexion.commit()
#        self.conexion.close()

    def getUserIdAndAdmin(self, usuario):
        """Devuelve el id del usuario, y si este es admin"""
        if usuario == "NoBody":
            id_usuario=1
            es_admin=0
            return id_usuario,  es_admin
        respuesta=self.cursor.execute('select id,admin from usuarios where username=? ', (usuario, ))
        return respuesta.fetchone()

    def recargarCacheDenegadas(self):
        """Recarga la cache de urls denegadas, con lo que esta en la base de datos"""
        logger.log(logging.INFO,"Recargando cache de URLs denegadas")
        self.cache_urls_denegadas=[]
        respuesta=self.cursor.execute('select url from cache_urls_denegadas').fetchall()
        for fila in respuesta:
            self.cache_urls_denegadas.append(fila[0])

    def recargarCacheAceptadas(self):
        """Recarga la cache de urls aceptadas, con lo que esta en la base de datos"""
        logger.log(logging.INFO,"Recargando cache de URLs aceptadas")
        self.cache_urls_aceptadas=[]
        respuesta=self.cursor.execute('select url from cache_urls_aceptadas').fetchall()
        for fila in respuesta:
            self.cache_urls_aceptadas.append(fila[0])

    def recargarDominiosDenegados(self):
        """Carga desde la base de datos a memoria los dominios denegados"""
        logger.log(logging.INFO,"Recargando dominios denegados")
        self.dominios_denegados=[]
        respuesta=self.cursor.execute('select url from dominios_denegados where usuario=?', (self.id, )).fetchall()
        for fila in respuesta:
            self.dominios_denegados.append(fila[0])

    def recargarDominiosPermitidos(self):
        """Carga desde la base de datos a memoria los dominios permitidos"""
        logger.log(logging.INFO,"Recargando dominios permitidos")
        self.dominios_permitidos=[]
        respuesta=self.cursor.execute('select url from dominios_permitidos where usuario=?',(self.id, )).fetchall()
        for fila in respuesta:
            self.dominios_permitidos.append(fila[0])

    def recargarDominiosPublicamentePermitidos(self):
        """Carga desde la base de datos a memoria los dominios Publicamente permitidos"""
        logger.log(logging.INFO,"Recargando dominios publicamente permitidos")
        conexion = sqlite3.connect(config.PATH_DB)
        cursor=conexion.cursor()
        self.dominios_publicamente_permitidos=[]
        respuesta=cursor.execute('select url from dominios_publicamente_permitidos').fetchall()
        for fila in respuesta:
            self.dominios_publicamente_permitidos.append(fila[0])
        conexion.close()

    def recargarDominiosPublicamenteDenegados(self):
        """Carga desde la base de datos a memoria los dominios Publicamente denegados"""
        logger.log(logging.INFO,"Recargando dominios publicamente denegados")
        conexion = sqlite3.connect(config.PATH_DB)
        cursor=conexion.cursor()
        self.dominios_publicamente_denegados=[]
        respuesta=cursor.execute('select url from dominios_publicamente_denegados').fetchall()
        for fila in respuesta:
            self.dominios_publicamente_denegados.append(fila[0])
        conexion.close()

    def dominioPermitido(self, url):
        """Verifica si el dominio esta en la lista de dominios permitidos"""
        for dominio in self.dominios_permitidos:
            if re.search(dominio,url):
                return True
        return False

    def dominioDenegado(self, url):
        """Verifica si el dominio esta en la lista de dominios denegados"""
        for dominio in self.dominios_denegados:
            if re.search(str(dominio),url):
                return True
        return False

    def dominioPublicamentePermitido(self, url):
        """Verifica si el dominio esta en la lista de dominios Publicamente permitidos"""
        dominio=url.split('/')[2]
        return dominio in self.dominios_publicamente_permitidos

    def dominioPublicamenteDenegado(self, url):
        """Verifica si el dominio esta en la lista de dominios Publicamente denegados"""
        dominio=url.split('/')[2]
        return dominio in self.dominios_publicamente_denegados

    def cacheAceptadas(self, url):
        """Verifica si la url esta en la cache de aceptadas"""
        return url in self.cache_urls_aceptadas

    def cacheDenegadas(self, url):
        """Verifica si la url esta en la cache de denegadas"""
        return url in self.cache_urls_denegadas

    def persistirACacheAceptadas(self, url):
        """Baja de la cache en memoria, a la base de datos las urls aceptadas"""
        hora_url=time.time()
        self.buffer_aceptadas.append([url, hora_url])
        if len(self.buffer_aceptadas) > (config.MAX_CACHE_URLS_ACEPTADAS):
            conexion = sqlite3.connect(config.PATH_DB)
            cursor=conexion.cursor()
            for item in self.buffer_aceptadas:
                cursor.execute('insert into cache_urls_aceptadas values (?,?)',(item[0],item[1], ))
                logger.log(logging.INFO,"Agregando en la cache de urls aceptadas a: %s" % item[0])
            conexion.commit()
            conexion.close()
            self.buffer_aceptadas=[]

    def persistirACacheDenegadas(self, url):
        """Baja de la cache en memoria, a la base de datos las urls denegadas"""
        hora_url=time.time()
        self.buffer_denegadas.append([url, hora_url])
        if len(self.buffer_denegadas) > (config.MAX_CACHE_URLS_DENEGADAS):
            conexion = sqlite3.connect(config.PATH_DB)
            cursor=conexion.cursor()
            for item in self.buffer_denegadas:
                cursor.execute('insert into cache_urls_denegadas values (?,?)',(item[0],item[1], ))
                logger.log(logging.INFO,"Agregando en la cache de urls denegadas a: %s" % item[0])
            conexion.commit()
            conexion.close()
            self.buffer_denegadas=[]

    def recargarPeriodoDeActualizacion(self):
        # prueba con el servidor seteado en la conifg, y sino devuelve
        # uno valido y lo setea para seguir usandolo
        config.SYNC_SERVER_IP,config.SERVER_PORT=self.servidor.obtenerServidor(config.SYNC_SERVER_IP,config.SERVER_PORT)
        conexion=httplib.HTTPConnection("%s:%s" % (config.SYNC_SERVER_IP,config.SERVER_PORT,))
        headers = {"UserID": "1","Peticion":"getPeriodoDeActualizacion"}
        conexion.request("GET", "/", "", headers)
        respuesta=conexion.getresponse()
        respuesta=respuesta.read()
        if not respuesta or not respuesta.isdigit():
            respuesta=10
            logger.log(logging.INFO,"No se obtuvo un Periodo de actualizacion. Seteando por defecto a:" % respuesta)
        self.periodoDeActualizacionDB=int(respuesta)*60
        logger.log(logging.INFO,"Periodo de actualizacion de la DB obtenido: %s" % self.periodoDeActualizacionDB )

    def chequearEdadCaches(self):
        tiempo_actual=time.time()
        tiempo_transcurrido=tiempo_actual - self.ultimaRecargaDeDominios
        if (tiempo_transcurrido > self.periodoDeActualizacionDB):
            self.recargarDominiosPublicamentePermitidos()
            self.recargarDominiosPublicamenteDenegados()
            self.recargarPeriodoDeActualizacion()
            self.ultimaRecargaDeDominios=tiempo_actual
            logger.log(logging.INFO,"Dominios recargados, se volveran a sincronizar en %s" % self.periodoDeActualizacionDB)

    def validarRemotamente(self, url):
        """Consulta al servidor por la url, porque no pudo determinar su aptitud"""
        self.chequearEdadCaches()
        logger.log(logging.INFO,"Validando remotamente: %s" % url)
        if config.USAR_PROXY:
            if self.servidor.estaOnline(config.PROXY_IP,config.PROXY_PORT):
                server="http://%s:%s" % (config.PROXY_IP,config.PROXY_PORT)
                proxy={'http':server, 'https': server}
                proxy_handler=urllib2.ProxyHandler(proxy)
                opener=urllib2.build_opener(proxy_handler)
                urllib2.install_opener(opener)
            else:
                logger.log(logging.ERROR,"El proxy no esta escuchando en %s:%s por lo que no se \
                utilizara" % (config.PROXY_IP,config.PROXY_PORT,))

        heads = {"UserID": "1","URL":url,"Peticion":"consulta"}
        # prueba con el servidor seteado en la config, y sino devuelve
        # uno valido y lo setea para seguir usandolo
        config.SERVER_IP,config.SERVER_PORT=self.servidor.obtenerServidor(config.SERVER_IP,config.SERVER_PORT)
        req = urllib2.Request("http://%s:%s" %(config.SERVER_IP,config.SERVER_PORT, ),headers=heads)
        try:
            respuesta = urllib2.urlopen(req)
            if respuesta.getcode() == 204:
                logger.log(logging.INFO,"URL validada remotamente: %s" % url)
                return True, ""
            else:
                logger.log(logging.INFO,"URL denegada remotamente: %s" % url)
                logger.log(logging.INFO,"Motivo: %s" % respuesta.msg)
                return False, respuesta.msg
        except urllib2.HTTPError, e:
            logger.log(logging.ERROR,"Error verificando la URL: %s , ERROR: %s" % (url, e.code))
