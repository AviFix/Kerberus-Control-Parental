#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Modulo encargado de manejar las urls"""

# Modulos externos
import urllib2
import httplib
import logging
import time
#import re
import MySQLdb
import sys

# Modulos propios
sys.path.append('/home/mboscovich/proyectos/control_parental/server/conf')
sys.path.append('clases')

import filtradoPorDNS
#FIXME: Falta agregar el manejo de excepciones de mysqldb
modulo_logger = logging.getLogger('Kerberus')


class Urls:
    def __init__(self):
        self.buffer_aceptadas = []
        self.buffer_denegadas = []
        self.buffer_dominios_aceptados = []
        self.buffer_dominios_denegados = []
        self.dnsfilter = filtradoPorDNS.DnsFilter()

    def setLogger(self, logger):
        self.logger = logger

    def inicializarServer(self, config):
        self.serverConfig = config
        hora_actual = time.time()
        self.ultimaVerficiacionCacheAceptadas = hora_actual
        self.ultimaVerficiacionCacheDenegadas = hora_actual
        self.borrarCaches()
        self.cargarDominios()
        self.cargarUrls()
        self.definirDansguaridanServer(self.serverConfig.dansguardian_ip,
                                        self.serverConfig.dansguardian_port)
        self.logger.log(logging.DEBUG,
            "Servidor inicializado, listo para atender solicitudes!"\
            " - ServerID: %s" % self.serverConfig.serverID)

    def recargarConfigServer(self, config):
        self.serverConfig = config

    def definirDansguaridanServer(self, ip, port):
        server = "http://%s:%s" % (ip, port)
        dansguardian = {'http': server, 'https': server}
        proxy_handler = urllib2.ProxyHandler(dansguardian)
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        self.logger.log(logging.DEBUG,
            "Utilizando Dansguardian Server: %s" % server)

    def cargarDominios(self):
        self.cargarDominiosPermitidos()
        self.cargarDominiosDenegados()

    def borrarCaches(self):
        self.borrarCacheDeUrlsAceptadasViejas()
        self.borrarCacheDeUrlsDenegadasViejas()
        self.logger.log(logging.DEBUG,
            "Borrando cache de URLs")

    def cargarUrls(self):
        self.cargarUrlsCacheadasAceptadas()
        self.cargarUrlsCacheadasDenegadas()
        self.logger.log(logging.DEBUG,
            "Cargando cache de URLs")

    def verificarCachesViejas(self, hora_actual):
        tiempo_transcurrido_aceptadas = hora_actual - \
        self.ultimaVerficiacionCacheAceptadas
        tiempo_transcurrido_denegadas = hora_actual - \
        self.ultimaVerficiacionCacheAceptadas
        if tiempo_transcurrido_aceptadas > \
        (self.serverConfig.cache_aceptadas_duracion):
            self.logger.log(logging.INFO,
            "Borrando URLs aceptadas viejas, y recargando")
            self.borrarCacheDeUrlsAceptadasViejas()
            self.cargarUrlsCacheadasAceptadas()
            self.ultimaVerficiacionCacheAceptadas = hora_actual
        if tiempo_transcurrido_denegadas > \
        (self.serverConfig.cache_denegadas_duracion):
            self.logger.log(logging.INFO,
            "Borrando URLs denegadas viejas, y recargando")
            self.borrarCacheDeUrlsDenegadasViejas()
            self.cargarUrlsCacheadasDenegadas()
            self.ultimaVerficiacionCacheDenegadas = hora_actual

    def cargarDominiosPermitidos(self):
        self.dominios_permitidos = []
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        cursor.execute('select distinct url from dominios where estado=1')
        respuesta = cursor.fetchall()
        for fila in respuesta:
            self.dominios_permitidos.append(fila[0])
        conexion.close()

    def cargarDominiosDenegados(self):
        self.dominios_denegados = []
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        cursor.execute('select distinct url from dominios where estado = 2')
        respuesta = cursor.fetchall()
        for fila in respuesta:
            self.dominios_denegados.append(fila[0])
        conexion.close()

    def borrarCacheDeUrlsAceptadasViejas(self):
        tiempo = time.time()
        tiempo_de_expiracion = tiempo - \
        self.serverConfig.cache_aceptadas_duracion * 60
        timestring = time.strftime("%Y-%m-%d %H:%M:%S",
            time.localtime(tiempo_de_expiracion))
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        cursor.executemany('delete from cache_urls_aceptadas where hora < %s ',
            (timestring, ))
        conexion.commit()
        conexion.close()

    def borrarCacheDeUrlsDenegadasViejas(self):
        tiempo = time.time()
        tiempo_de_expiracion = tiempo - \
            self.serverConfig.cache_denegadas_duracion * 60
        timestring = time.strftime("%Y-%m-%d %H:%M:%S",
            time.localtime(tiempo_de_expiracion))
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        cursor.executemany('delete from cache_urls_denegadas where hora < %s ',
            (timestring, ))
        conexion.commit()
        conexion.close()

    def cargarUrlsCacheadasAceptadas(self):
        self.cache_urls_aceptadas = []
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        cursor.execute('select url from cache_urls_aceptadas')
        respuesta = cursor.fetchall()
        for fila in respuesta:
            self.cache_urls_aceptadas.append(fila[0])
        conexion.close()

    def cargarUrlsCacheadasDenegadas(self):
        self.cache_urls_denegadas = []
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        cursor.execute('select url from cache_urls_denegadas')
        respuesta = cursor.fetchall()
        for fila in respuesta:
            self.cache_urls_denegadas.append(fila[0])
        conexion.close()

    def agregarDominioAceptado(self, dominio):
        for registro in self.buffer_dominios_aceptados:
            if dominio in registro:
                return False
        ultima_revision = time.strftime("%Y-%m-%d %H:%M:%S",
            time.localtime(time.time()))
        self.dominios_permitidos.append(dominio)
        self.buffer_dominios_aceptados.append([dominio, ultima_revision])
        self.logger.log(logging.DEBUG,
            "Dominio aceptado buffereado %d de %s" % \
            (len(self.buffer_dominios_aceptados),
            self.serverConfig.cache_max_dominios_aceptados))
        if len(self.buffer_dominios_aceptados) >= \
            int(self.serverConfig.cache_max_dominios_aceptados):
            self.logger.log(logging.INFO,
                "Descargando dominios aceptados a la base de datos")
            conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                        user=self.serverConfig.db_user,
                                        passwd=self.serverConfig.db_password,
                                        db=self.serverConfig.db_name,
                                        charset="utf8", use_unicode=True)
            cursor = conexion.cursor()
            for dominio, ultima_revision in self.buffer_dominios_aceptados:
                self.logger.log(logging.DEBUG,
                    "Persistiendo el dominio %s en la DB" % dominio)
                cursor.execute('insert into dominios(url, ultima_revision, \
                estado, verificador) values (%s, %s, %s, %s)', \
                (dominio, ultima_revision, 1, 1))
            conexion.commit()
            self.buffer_dominios_aceptados = []
            conexion.close()

    def agregarDominioDenegado(self, dominio):
        for registro in self.buffer_dominios_denegados:
            if dominio in registro:
                return False
        ultima_revision = time.strftime("%Y-%m-%d %H:%M:%S",
            time.localtime(time.time()))
        self.dominios_denegados.append(dominio)
        self.buffer_dominios_denegados.append([dominio, ultima_revision])
        self.logger.log(logging.DEBUG,
            "Dominio denegado buffereado %d de %s" % \
            (len(self.buffer_dominios_denegados), \
            self.serverConfig.cache_max_dominios_denegados))
        if len(self.buffer_dominios_denegados) >= \
            int(self.serverConfig.cache_max_dominios_denegados):
            self.logger.log(logging.INFO,
                "Descargando dominios denegados a la base de datos")
            conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                        user=self.serverConfig.db_user,
                                        passwd=self.serverConfig.db_password,
                                        db=self.serverConfig.db_name,
                                        charset="utf8", use_unicode=True)
            cursor = conexion.cursor()
            for dominio, ultima_revision in self.buffer_dominios_denegados:
                self.logger.log(logging.DEBUG,
                    "Persistiendo el dominio %s en la DB" % dominio)
                cursor.execute('insert into dominios(url, ultima_revision, \
                    estado, verificador) values (%s, %s, %s, %s)', \
                    (dominio, ultima_revision, 2, 1))
            conexion.commit()
            self.buffer_dominios_denegados = []
            conexion.close()

    def persistirEnCacheAceptadas(self, url):
        hora_actual = time.time()
        timestring = time.strftime("%Y-%m-%d %H:%M:%S",
            time.localtime(hora_actual))
        self.buffer_aceptadas.append([url, timestring])
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        if len(self.buffer_aceptadas) > \
            (self.serverConfig.cache_max_urls_aceptadas):
            for item in self.buffer_aceptadas:
                cursor.execute('insert into cache_urls_aceptadas(url,hora) \
                values(%s,%s)', (item[0], item[1], ))
            conexion.commit()
            self.buffer_aceptadas = []
            self.verificarCachesViejas(hora_actual)
            conexion.close()

    def persistirEnCacheDenegadas(self, url):
        timestring = time.strftime("%Y-%m-%d %H:%M:%S",
            time.localtime(time.time()))
        self.buffer_denegadas.append([url, timestring])
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        if len(self.buffer_denegadas) > \
            (self.serverConfig.cache_max_urls_denegadas):
            for item in self.buffer_denegadas:
                cursor.execute('insert into cache_urls_denegadas(url,hora) \
                values(%s,%s)', (item[0], item[1], ))
            conexion.commit()
            self.buffer_denegadas = []
        conexion.close()

    def dominioPermitido(self, dominio):
        for entrada in self.buffer_dominios_aceptados:
            if dominio in entrada:
                self.logger.log(logging.DEBUG,
                "Dominio en buffer_dominios_aceptados: %s" % (dominio))
                return True
        return dominio in self.dominios_permitidos

    def dominioDenegado(self, dominio):
        for entrada in self.buffer_dominios_denegados:
            if dominio in entrada:
                self.logger.log(logging.DEBUG,
                "Dominio en buffer_dominios_denegados: %s" % (dominio))
                return True
        return dominio in self.dominios_denegados

    def getDominiosDenegados(self, modificados_despues_de):
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        cursor.execute(
        'select url from dominios where estado = 2 and ultima_revision > %s',
         (modificados_despues_de,))
        salida = cursor.fetchall()
        conexion.close()
        respuesta = ""
        for fila in salida:
            respuesta += str(fila[0]) + "\n"
        if respuesta:
            return respuesta
        else:
            return []

    def getDominiosPermitidos(self, modificados_despues_de):
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        cursor.execute(
        'select url from dominios where estado = 1 and ultima_revision > %s',
        (modificados_despues_de,))
        salida = cursor.fetchall()
        conexion.close()
        respuesta = ""
        for fila in salida:
            respuesta += str(fila[0]) + "\n"
        if respuesta:
            return respuesta
        else:
            return []

    def getPeriodoDeActualizacion(self):
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        cursor.execute('select tiempo_actualizacion_clientes from parametros')
        salida = cursor.fetchall()[0][0]
        conexion.close()
        return salida

    def getPeriodoDeRecargaCompleta(self):
        conexion = MySQLdb.connect(host=self.serverConfig.db_host,
                                    user=self.serverConfig.db_user,
                                    passwd=self.serverConfig.db_password,
                                    db=self.serverConfig.db_name,
                                    charset="utf8", use_unicode=True)
        cursor = conexion.cursor()
        cursor.execute('select tiempo_de_recarga_completa_clientes \
        from parametros')
        salida = cursor.fetchall()[0][0]
        conexion.close()
        return salida

    def preguntarDansguardian(self, url):
        server = "http://127.0.0.1:8082"
        dansguardian = {'http': server, 'https': server}
        proxy_handler = urllib2.ProxyHandler(dansguardian)
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        salida = True
        try:
            respuesta = urllib2.urlopen(url)
            # si devuelve 1, significa que esta denegada la url
            salida = (respuesta.read(1) != "1")
        except urllib2.HTTPError, e:
            self.logger.log(logging.ERROR,
                "Error verificando la URL: %s , ERROR: %s" % (url, e.code))
        except urllib2.URLError, e:
            self.logger.log(logging.ERROR,
                "Error verificando la URL: %s, ERROR: %s, RAZON: %s" % (url,
                e.args, e.reason))
        except httplib.HTTPException, e:
            self.logger.log(logging.ERROR,
                "Error verificando la URL:%s, ERROR: %s" % (url, e, ))
        if salida:
            return True, ""
        else:
            return False, "El sitio no es apto para menores de edad."

    def usuarioValido(self, usuario=""):
        return True

    def urlHabilitada(self, url):
        dominio = url.split('/')[2]

        if self.dominioPermitido(dominio):
            self.logger.log(logging.DEBUG,
            "Dominio Publicamente Permitido: %s, URL: %s " % (dominio, url))
            return True, ""

        if self.dominioDenegado(dominio):
            self.logger.log(logging.DEBUG,
                "Dominio Publicamente Denegado: %s, URL: %s " % (dominio, url))
            return False, "Dominio publicamente denegado en el servidor"
        inicio = time.time()
        valido = self.dnsfilter.testDominio(dominio)
        fin = time.time()
        demoro = fin - inicio
        if valido:
            self.logger.log(logging.DEBUG,
                "Dominio Permitido por DNS: %s , URL: %s, demoro: %f" % \
                (dominio, url, demoro))
            self.agregarDominioAceptado(dominio)
            return True, ""
        else:
            self.logger.log(logging.DEBUG,
            "Dominio Denegado por DNS: %s , URL: %s, demoro: %f" % (dominio,
            url, demoro))
            self.agregarDominioDenegado(dominio)
            return False, "Dominio publicamente denegado por DNS"
        # #################################
        # DE ACA PARA ABAJO NO SE USA  POR AHORA #
        # #################################

        if url in self.cache_urls_aceptadas:
            self.logger.log(logging.DEBUG,
                "Dominio CACHEADO en Mem, aceptado:  %s " % url)
            return True, ""

        if url in self.cache_urls_denegadas:
            self.logger.log(logging.DEBUG,
                "Dominio CACHEADO en Mem, denegado:  %s" % url)
            return False, "Dominio CACHEADO en el servidor"

        # si no esta en la cache, le pregunto a dansguardian

        permitida, mensaje = self.preguntarDansguardian(url)

        if permitida:
            self.logger.log(logging.DEBUG, "URL Permitida: %s" % url)
            self.cache_urls_aceptadas.append(url)
            self.persistirEnCacheAceptadas(url)
        else:
            self.logger.log(logging.DEBUG, "URL Denegada: %s" % url)
            self.cache_urls_denegadas.append(url)
            self.persistirEnCacheDenegadas(url)

        return permitida, mensaje
