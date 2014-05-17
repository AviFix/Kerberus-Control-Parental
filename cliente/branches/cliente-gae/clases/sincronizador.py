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
import logging

modulo_logger = logging.getLogger('kerberus.' + __name__)

sys.path.append('../conf')
sys.path.append('../password')

# Modulos propios
import config
import registrar
import registrarUsuario
import peticion


class Sincronizador:

    def __init__(self, peticionRemota=None):
        if peticionRemota is None:
            peticionRemota = peticion.Peticion()
        self.peticionRemota = peticionRemota
        self.recienRegistrado = False
        self.recargar_todos_los_dominios = False

    def checkRegistro(self):
        registrador = registrar.Registradores(self.peticionRemota)
        registradoLocalmente = registrador.checkRegistradoLocalmente()
        if not registradoLocalmente:
            modulo_logger.info("Iniciando proceso de solicitud de datos")
            registrarUsuario.RegistrarUsuario()
            if config.PLATAFORMA == 'Windows':
                self.recienRegistrado = True
        else:
            self.id, self.nombre, self.email, self.version, self.password = \
                    registrador.obtenerDatosRegistrados()
            modulo_logger.info("Esta registrado localmente")

        registradoRemotamente = registrador.checkRegistradoRemotamente()
        if not registradoRemotamente:
            modulo_logger.info("Iniciando proceso de registro remoto")
            registrador.registrarRemotamente()
        else:
            modulo_logger.info("Esta registrado remotamente")

        self.id, self.nombre, self.email, self.version, self.password = \
                registrador.obtenerDatosRegistrados()

    def checkPasswordNotificada(self):
        # Verifico si se informo una nueva password
        if not self.passwordNotificada():
            self.notificarPassword()

    def obtenerDatosDeActualizacion(self):
        try:
            conexion_db = sqlite3.connect(config.PATH_DB)
            cursor = conexion_db.cursor()

            self.ultima_actualizacion = cursor.execute(
                'select ultima_actualizacion from sincronizador'
                ).fetchone()[0]

            self.ultima_recarga_completa = cursor.execute(
                'select ultima_recarga_completa from sincronizador'
                ).fetchone()[0]
            conexion_db.close()
        except:
            modulo_logger.error('Hubo un problema mientras se obtenida desde la'
                'base de datos los datos de sincronizacion')

        self.periodo_expiracion = \
            self.peticionRemota.obtenerPeriodoDeActualizacion()

        self.periodo_recarga_completa = \
            self.peticionRemota.obtenerPeriodoDeRecargaCompleta()

        modulo_logger.debug("Periodo de actualizacion: %s segundos"
            % self.periodo_expiracion)
        modulo_logger.debug("Periodo de recarga completa: %s segundos"
            % self.periodo_recarga_completa)
        modulo_logger.debug("Ultima actualizacion: %s"
            % self.ultima_actualizacion)
        modulo_logger.debug("Ultima recarga completa: %s"
            % self.ultima_recarga_completa)

    def __del__(self):
        modulo_logger.debug("Deteniendo el demonio de sincronizacion")

    def run(self):
        if self.recienRegistrado:
            modulo_logger.info("Se terminaron de obtener los datos del usuario")
        else:
            modulo_logger.info("Iniciando el demonio de sincronización")
            if config.PLATAFORMA == 'Windows':
                actualizacionDisponible, md5sum = \
                    self.peticionRemota.chequearActualizaciones()
                if actualizacionDisponible is not None:
                    self.actualizarVersion(actualizacionDisponible, md5sum)

            while True:
                hora_servidor = self.peticionRemota.obtenerHoraServidor()
                self.tiempo_actual = float(hora_servidor)
                tiempo_transcurrido = self.tiempo_actual - \
                    self.ultima_actualizacion
                tiempo_transcurrido_ultima_recarga = \
                    self.tiempo_actual - self.ultima_recarga_completa

                if (tiempo_transcurrido_ultima_recarga >
                    self.periodo_recarga_completa):
                    self.recargar_todos_los_dominios = True
                    modulo_logger.debug("Se recargaran todos los dominios "
                        "permitidos/dengados con servidor...")

                if (tiempo_transcurrido > self.periodo_expiracion):
                    modulo_logger.debug("Sincronizando dominios "
                        "permitidos/dengados con servidor...")
                    self.sincronizarDominiosConServer()
                else:
                    tiempo_restante = self.ultima_actualizacion + \
                        self.periodo_expiracion - self.tiempo_actual
                    tiempo_proxima_recarga_completa = \
                        self.ultima_recarga_completa + \
                        self.periodo_recarga_completa - \
                        self.tiempo_actual
                    modulo_logger.debug("Faltan %s minutos para que se chequee"
                        " si hay dominios nuevos, y %s minutos para recargar "
                        "todos los dominios" % (tiempo_restante / 60,
                        tiempo_proxima_recarga_completa / 60))
                    # FIXME: pongo esto porque sino a veces queda loco pidiendo
                    # hay que ver porque.
                    if tiempo_restante < 60:
                        tiempo_restante = 60
                    time.sleep(tiempo_restante)
                    modulo_logger.debug("Chequeando nuevamente los dominios")

    def passwordNotificada(self):
        """Verifica si se informo remotamente la password"""
        try:
            conexion_db = sqlite3.connect(config.PATH_DB)
            cursor = conexion_db.cursor()
            password_notificada = cursor.execute(
                'select passwordnotificada from instalacion').fetchone()[0]
            conexion_db.close()

        except sqlite3.OperationalError, msg:
            modulo_logger.error("No se pudo verificar si la password esta "
                "verficada. Tal vez no esta la base de datos instalada.\n"
                "Error: %s" % msg)
            conexion_db.close()
            return True
        return password_notificada

    def notificarPassword(self):
        try:
            conexion_db = sqlite3.connect(config.PATH_DB)
            cursor = conexion_db.cursor()
            password = cursor.execute(
                'select password from instalacion').fetchone()[0]

            respuesta = self.peticionRemota.informarNuevaPassword(password)

            if respuesta == 'Informada':
                md5_password_nueva = \
                    hashlib.md5(password.encode('utf-8')).hexdigest()
                cursor.execute('update instalacion set passwordnotificada=?, '
                'password=?, credencial=?', (1, '', md5_password_nueva,))
                conexion_db.commit()

            conexion_db.close()

        except sqlite3.OperationalError, msg:
            conexion_db.rollback()
            modulo_logger.error("No se pudo obtener la pass para notificarla."
            "\nError: %s" % msg)
            conexion_db.close()

    def sincronizarDominiosPermitidos(self):
            conexion_db = sqlite3.connect(config.PATH_DB)
            cursor = conexion_db.cursor()

            if self.recargar_todos_los_dominios:
                self.ultima_actualizacion = 0

            dominios = self.peticionRemota.obtenerDominiosPermitidos(
                self.ultima_actualizacion)

            if len(dominios):
                if dominios[-1] == "":
                    array_dominios = dominios.rsplit("\n")[0:-1]
                else:
                    array_dominios = dominios.rsplit("\n")
                try:
                    if self.recargar_todos_los_dominios:
                        cursor.execute(
                            'delete from dominios_kerberus')
                    for fila in array_dominios:
                        if fila != "":
                            cursor.execute('insert into '
                            'dominios_kerberus(url, estado) values(?,?)',
                            (fila, 1))
                    conexion_db.commit()

                except sqlite3.OperationalError, msg:
                    conexion_db.rollback()
                    modulo_logger.error("Error al cargar los dominios "
                    "permitidos a la base de datos.\nError: %s" % msg)
            else:
                modulo_logger.debug(
                    "No hay dominios permitidos para actualizar")
            conexion_db.close()

    def sincronizarDominiosDenegados(self):
            conexion_db = sqlite3.connect(config.PATH_DB)
            cursor = conexion_db.cursor()

            if self.recargar_todos_los_dominios:
                self.ultima_actualizacion = 0

            dominios = self.peticionRemota.obtenerDominiosDenegados(
                self.ultima_actualizacion)

            if len(dominios):
                if dominios[-1] == "":
                    array_dominios = dominios.rsplit("\n")[0:-1]
                else:
                    array_dominios = dominios.rsplit("\n")
                try:
                    if self.recargar_todos_los_dominios:
                        cursor.execute(
                            'delete from dominios_kerberus')

                    for fila in array_dominios:
                        if fila != "":
                            cursor.execute(
                            'insert into dominios_kerberus(url, estado)'
                            ' values(?,?)', (fila, 2))

                    conexion_db.commit()

                except sqlite3.OperationalError, msg:
                    conexion_db.rollback()
                    modulo_logger.error("Error al cargar los dominios denegados"
                    " a la base de datos.\nError: %s" % msg)

            else:
                modulo_logger.debug("No hay dominios denegados para actualizar")
            conexion_db.close()

    def sincronizarDominiosUsuario(self):
        dominios = self.peticionRemota.obtenerDominiosUsuario()
        if len(dominios):
            if dominios[-1] == "":
                array_dominios = dominios.rsplit("\n")[0:-1]
            else:
                array_dominios = dominios.rsplit("\n")
            try:
                conexion_db = sqlite3.connect(config.PATH_DB)
                cursor = conexion_db.cursor()
                cursor.execute('delete from dominios_usuario')
                conexion_db.commit()
                for fila in array_dominios:
                    if fila != "":
                        dominio, estado = fila.rsplit(',')
                        if estado == 'Permitido':
                            estado_num = 1
                        else:
                            estado_num = 2
                        # usuario 2 es el usuario default, no admin
                        usuario = 2
                        cursor.execute('insert into '
                        'dominios_usuario(url, usuario, estado) values(?,?,?)',
                        (dominio, usuario, estado_num))
                conexion_db.commit()

            except sqlite3.OperationalError, msg:
                conexion_db.rollback()
                modulo_logger.error("Error al cargar los dominios "
                "permitidos a la base de datos.\nError: %s" % msg)
        else:
            modulo_logger.debug(
                "No hay dominios permitidos para actualizar")
        conexion_db.close()

    def sincronizarDominiosConServer(self):
            self.sincronizarDominiosPermitidos()
            self.sincronizarDominiosDenegados()
            self.tiempo_actual = time.time()
            self.ultima_actualizacion = self.tiempo_actual
            modulo_logger.debug("Se terminaron de sincronizar los dominios")

            conexion_db = sqlite3.connect(config.PATH_DB)
            cursor = conexion_db.cursor()

            try:
                if self.recargar_todos_los_dominios:
                    cursor.execute(
                        'update sincronizador set ultima_actualizacion=?, '
                        'ultima_recarga_completa=?',
                        (self.tiempo_actual, self.tiempo_actual))

                    self.recargar_todos_los_dominios = False
                    self.ultima_recarga_completa = self.tiempo_actual

                else:
                    cursor.execute(
                        'update sincronizador set ultima_actualizacion=?',
                        (self.tiempo_actual,))

                conexion_db.commit()

                modulo_logger.info("Se ha sincronizado la base de datos de "
                    "dominios publicamente aceptados/denegados")

            except sqlite3.OperationalError, msg:
                conexion_db.rollback()
                modulo_logger.error("Error al cargar los datos de "
                    "sincronizacion a la base de datos.\nError: %s" % msg)

            conexion_db.close()

    def actualizarVersion(self, nueva_version, md5sum):
        modulo_logger.debug("Descargando nueva version...")

        #Descargo la version
        if config.USAR_PROXY:
            if self.servidor.estaOnline(config.PROXY_IP, config.PROXY_PORT):
                url_proxy = "http://%s:%s" % (config.PROXY_IP,
                                                config.PROXY_PORT)
                modulo_logger.debug("Conectando a %s, por medio del proxy %s ,"
                    " para actualizar la version" % (nueva_version, url_proxy))

                proxy = {'http': url_proxy, 'https': url_proxy}
            else:
                modulo_logger.error("El proxy no esta escuchando en %s:%s por "
                "lo que no se utilizara"
                % (config.PROXY_IP, config.PROXY_PORT,))

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

                modulo_logger.debug("Actualizando a nueva version...")

                if config.PLATAFORMA == 'Windows':
                    path_actualizador = config.PATH_COMMON + '\update.exe'
                elif config.PLATAFORMA == 'Linux':
                    path_actualizador = config.PATH_COMMON + '\update.sh'

                actualizador = open(path_actualizador, 'wb')
                actualizador.write(respuesta)
                actualizador.close()
                subprocess.call(path_actualizador)

        except urllib2.URLError as error:
            modulo_logger.error("Error al intentar descargar %s . ERROR: %s" %
                (nueva_version, error))

        modulo_logger.info("Fin de la actualizacion")


def main():
    pass

# Importante: los módulos no deberían ejecutar
# código al ser importados
if __name__ == '__main__':
    main()