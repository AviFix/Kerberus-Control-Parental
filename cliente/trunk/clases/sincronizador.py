# -*- coding: utf-8 -*-

# Modulos externos
import sys
import time
#import os
import sqlite3
#import httplib
#import platform
import urllib2
import hashlib
import subprocess

# Modulos propios
sys.path.append('../conf')
sys.path.append('../password')

import config
import registrar
import registrarUsuario
import peticion
import logging
import loguear

modulo_logger = loguear.logSetup(
    config.SYNC_LOG_FILENAME,
    config.SYNC_LOGLEVEL, config.SYNC_LOG_SIZE_MB,
    config.SYNC_LOG_CANT_ROTACIONES, "kerberus"
    )


class Sincronizador:

    def __init__(self):
        self.registrador = registrar.Registradores()
        self.recienRegistrado = False

        registradoLocalmente = self.registrador.checkRegistradoLocalmente()
        if not registradoLocalmente:
            modulo_logger.log(logging.INFO,
                                "Iniciando proceso de solicitud de datos")
            reg = registrarUsuario.RegistrarUsuario()
            if config.PLATAFORMA == 'Windows':
                self.recienRegistrado = True
        else:
            self.id, self.nombre, self.email, self.version, self.password = \
                    self.registrador.obtenerDatosRegistrados()
            modulo_logger.log(logging.INFO, "Esta registrado localmente")

        registradoRemotamente = self.registrador.checkRegistradoRemotamente()
        if not registradoRemotamente:
            modulo_logger.log(logging.INFO,
                                "Iniciando proceso de registro remoto")
            self.registrador.registrarRemotamente()
        else:
            modulo_logger.log(logging.INFO, "Esta registrado remotamente")

        self.id, self.nombre, self.email, self.version, self.password = \
                self.registrador.obtenerDatosRegistrados()

        # Verifico si se informo una nueva password
        if not self.passwordNotificada():
            self.notificarPassword()

        self.peticionRemota = peticion.Peticion()

        self.conexion_db = sqlite3.connect(config.PATH_DB)
        self.cursor = self.conexion_db.cursor()

        self.ultima_actualizacion = self.cursor.execute(
            'select ultima_actualizacion from sincronizador').fetchone()[0]

        self.ultima_recarga_completa = self.cursor.execute(
            'select ultima_recarga_completa from sincronizador').fetchone()[0]

        self.periodo_expiracion = \
            self.peticionRemota.obtenerPeriodoDeActualizacion()

        self.periodo_recarga_completa = \
            self.peticionRemota.obtenerPeriodoDeRecargaCompleta()

        modulo_logger.log(logging.DEBUG,
            "Periodo de actualizacion: %s segundos" % self.periodo_expiracion)
        modulo_logger.log(logging.DEBUG,
            "Periodo de recarga completa: %s segundos" % \
            self.periodo_recarga_completa)
        modulo_logger.log(logging.DEBUG,
            "Ultima actualizacion: %s" % self.ultima_actualizacion)
        modulo_logger.log(logging.DEBUG,
            "Ultima recarga completa: %s" % self.ultima_recarga_completa)

        self.recargar_todos_los_dominios = False

    def __del__(self):
       #TODO: Tambien deberia informar que se cerror la sesion
        self.conexion_db.close()
        modulo_logger.log(logging.DEBUG,
            "Deteniendo el demonio de sincronizacion")

    def run(self):
        if self.recienRegistrado:
            modulo_logger.log(logging.INFO,
                "Se terminaron de obtener los datos del usuario")
        else:
            modulo_logger.log(logging.INFO,
                "Iniciando el demonio de sincronización")
            if config.PLATAFORMA == 'Windows':
                actualizacionDisponible, md5sum = \
                    self.peticionRemota.chequearActualizaciones()
                if actualizacionDisponible != None:
                    self.actualizarVersion(actualizacionDisponible, md5sum)

            while True:
                hora_servidor = self.peticionRemota.obtenerHoraServidor()
                self.tiempo_actual = float(hora_servidor)
                tiempo_transcurrido = self.tiempo_actual - \
                    self.ultima_actualizacion
                tiempo_transcurrido_ultima_recarga = \
                    self.tiempo_actual - self.ultima_recarga_completa

                if (tiempo_transcurrido_ultima_recarga > \
                    self.periodo_recarga_completa):
                    self.recargar_todos_los_dominios = True
                    modulo_logger.log(logging.DEBUG, "Se recargaran todos los"\
                    " dominios permitidos/dengados con servidor...")

                if (tiempo_transcurrido > self.periodo_expiracion):
                    modulo_logger.log(logging.DEBUG, "Sincronizando dominios"\
                    " permitidos/dengados con servidor...")
                    self.sincronizarDominiosConServer()
                else:
                    tiempo_restante = self.ultima_actualizacion + \
                        self.periodo_expiracion - self.tiempo_actual
                    tiempo_proxima_recarga_completa = \
                        self.ultima_recarga_completa + \
                        self.periodo_recarga_completa - \
                        self.tiempo_actual
                    modulo_logger.log(logging.DEBUG, "Faltan %s minutos para "\
                    "que se chequee si hay dominios nuevos, y %s minutos para"\
                    " recargar todos los dominios" % \
                    (tiempo_restante / 60,
                    tiempo_proxima_recarga_completa / 60))
                    time.sleep(tiempo_restante)
                    modulo_logger.log(logging.DEBUG,
                        "Chequeando nuevamente los dominios")

    def passwordNotificada(self):
        """Verifica si se informo remotamente la password"""
        try:
            conexion_db = sqlite3.connect(config.PATH_DB)
            cursor = conexion_db.cursor()
            password_notificada = cursor.execute(
                'select passwordnotificada from instalacion').fetchone()[0]
        except sqlite3.OperationalError, msg:
            self.modulo_logger.log(logging.ERROR, "No se pudo verificar si la"\
            " password esta verficada. Tal vez no esta la base de datos "\
            "instalada.\nError: %s" % msg)
            return True
        return password_notificada

    def notificarPassword(self):
        try:
            conexion_db = sqlite3.connect(config.PATH_DB)
            cursor = conexion_db.cursor()
            password = cursor.execute(
                'select password from instalacion').fetchone()[0]
            # FIXME: QUEDE ACAAAAAAAAAAAAAA
            # Manda la password vieja como nueva
            peticionRemota=peticion.Peticion()
            respuesta = peticionRemota.informarNuevaPassword(
                password)
            if respuesta == 'Informada':
                cursor.execute('update instalacion set passwordnotificada=1')
            cursor.close()
            conexion_db.commit()
        except sqlite3.OperationalError, msg:
            self.modulo_logger.log(logging.ERROR, "No se pudo obtener la pass"\
            " para notificarla.\nError: %s" % msg)

    def sincronizarDominiosPermitidos(self):
            if self.recargar_todos_los_dominios:
                self.ultima_actualizacion = 0
            dominios = self.peticionRemota.obtenerDominiosPermitidos(
                self.ultima_actualizacion)
            if len(dominios):
                if dominios[-1] == "":
                        array_dominios = dominios.rsplit("\n")[0:-1]
                else:
                    array_dominios = dominios.rsplit("\n")
                if self.recargar_todos_los_dominios:
                    self.cursor.execute(
                        'delete from dominios_publicamente_permitidos')
                for fila in array_dominios:
                    if fila != "":
                        #modulo_logger.log(logging.DEBUG,
                        #    "Se agrego el dominio permitido: %s" % fila)
                        self.cursor.execute(
                           'insert into dominios_publicamente_permitidos(url)'\
                           ' values(?)', (fila, )
                           )
                self.conexion_db.commit()
            else:
                modulo_logger.log(logging.DEBUG,
                    "No hay dominios permitidos para actualizar")

    def sincronizarDominiosDenegados(self):
            if self.recargar_todos_los_dominios:
                self.ultima_actualizacion = 0
            dominios = self.peticionRemota.obtenerDominiosDenegados(
                self.ultima_actualizacion
                )
            if len(dominios):
                if dominios[-1] == "":
                    array_dominios = dominios.rsplit("\n")[0:-1]
                else:
                    array_dominios = dominios.rsplit("\n")
                if self.recargar_todos_los_dominios:
                    self.cursor.execute(
                        'delete from dominios_publicamente_denegados'
                        )
                for fila in array_dominios:
                    if fila != "":
                        #modulo_logger.log(logging.DEBUG,
                        #    "Se agrego el dominio denegado: %s" % fila)
                        self.cursor.execute(
                            'insert into dominios_publicamente_denegados(url)'\
                            ' values(?)', (fila, )
                            )
                self.conexion_db.commit()
            else:
                modulo_logger.log(logging.DEBUG,
                    "No hay dominios denegados para actualizar")

    def sincronizarDominiosConServer(self):
            self.sincronizarDominiosPermitidos()
            self.sincronizarDominiosDenegados()
            modulo_logger.log(logging.DEBUG,
                "Se terminaron de sincronizar los dominios"
                )
            if self.recargar_todos_los_dominios:
                self.cursor.execute(
                    'update sincronizador set ultima_actualizacion=?, '\
                    'ultima_recarga_completa=?',
                    (self.tiempo_actual, self.tiempo_actual)
                    )
                self.recargar_todos_los_dominios = False
                self.ultima_actualizacion = self.tiempo_actual
            else:
                self.cursor.execute(
                    'update sincronizador set ultima_actualizacion=?',
                    (self.tiempo_actual,)
                    )
            self.conexion_db.commit()
            modulo_logger.log(logging.INFO,
                "Se ha sincronizado la base de datos de dominios publicamente"\
                " aceptados/denegados"
                )

    def actualizarVersion(self, nueva_version, md5sum):
        modulo_logger.log(logging.DEBUG, "Descargando nueva version...")
        #Descargo la version
        if config.USAR_PROXY:
            if self.servidor.estaOnline(config.PROXY_IP, config.PROXY_PORT):
                url_proxy = "http://%s:%s" % (config.PROXY_IP,
                                                config.PROXY_PORT)
                modulo_logger.log(logging.DEBUG,
                   "Conectando a %s, por medio del proxy %s , para actualizar"\
                   " la version" % (nueva_version, url_proxy))
                proxy = {'http': url_proxy, 'https': url_proxy}
            else:
                modulo_logger.log(logging.ERROR,
                    "El proxy no esta escuchando en %s:%s por lo que no se "\
                    "utilizara" % (config.PROXY_IP, config.PROXY_PORT,))
                proxy = {}
        else:
            proxy = {}
        proxy_handler = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        try:
            timeout = 10
            respuesta = urllib2.urlopen(nueva_version, timeout=timeout).read()
            md5destino = hashlib.md5(respuesta).hexdigest()
            if md5sum == md5destino:
                modulo_logger.log(logging.DEBUG,
                    "Actualizando a nueva version...")
                if config.PLATAFORMA == 'Windows':
                    path_actualizador = config.PATH_COMMON + '\update.exe'
                elif config.PLATAFORMA == 'Linux':
                    path_actualizador = config.PATH_COMMON + '\update.sh'
                actualizador = open(path_actualizador, 'wb')
                actualizador.write(respuesta)
                actualizador.close()
                subprocess.call(path_actualizador)

        except urllib2.URLError as error:
            modulo_logger.log(logging.ERROR,
                "Error al intentar descargar %s . ERROR: %s" % \
                (nueva_version, error))
        modulo_logger.log(logging.DEBUG, "Fin de la actualizacion")
