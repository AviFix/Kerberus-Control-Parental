# -*- coding: utf-8 -*-

"""Modulo encargado de verificar si el usuario ingresado por el cliente es
valido"""

#Modulos externos
import sqlite3
#import time
import hashlib
import os
import sys
#Modulos propios
sys.path.append('../conf')
import usuario
import config
import peticion
import logging

modulo_logger = logging.getLogger('kerberus.' + __name__)


#Excepciones
class AdministradorDeUsuariosError(Exception):

    def __init__(self):
        super(AdministradorDeUsuariosError, self).__init__()
        pass


class DatabaseError(AdministradorDeUsuariosError):

    def __init__(self):
        super(DatabaseError, self).__init__()
        pass


class UsuarioNoValido(AdministradorDeUsuariosError):

    def __init__(self):
        super(UsuarioNoValido, self).__init__()
        pass


# Clase
class AdministradorDeUsuarios:
        def __init__(self):
            if not os.path.exists(config.PATH_DB):
                modulo_logger.log(logging.ERROR, "La base de datos no existe, "\
                "o usted no posee permisos para accederla")
                raise DatabaseError("La base de datos no existe, o usted no "\
                "posee permisos para accederla")
            self.usuarios = []
            self.usuarios_ya_validados = []
            self.usuarios_ya_validados_pass = []

        def md5sum(self, t):
            try:
                return hashlib.md5(t.encode('utf-8')).hexdigest()
            except:
                modulo_logger.log(logging.ERROR, 'No se puedo generar el md5'
                    ' de %s' % t)

        def passwordSeteada(self, usuario):
            conexion = sqlite3.connect(config.PATH_DB)
            cursor = conexion.cursor()
            cursor.execute('select passwordseteada from usuarios where '\
            'username = ?', (usuario,))
            password_seteada = cursor.fetchone()[0]
            return password_seteada

        def cambiarPassword(self, usuario, password_vieja, password_nueva):
            password_vieja_md5 = self.md5sum(password_vieja)
            password_nueva_md5 = self.md5sum(password_nueva)
            conexion = sqlite3.connect(config.PATH_DB)
            cursor = conexion.cursor()
            cursor.execute('update usuarios set password=? where username=? '\
            'and password=? and passwordseteada=1', (password_nueva_md5, \
            usuario, password_vieja_md5, ))
            conexion.commit()
            cursor.execute('update instalacion set password=?, '\
            'passwordnotificada=?', (password_nueva, 0,))
            conexion.commit()
            conexion.commit()
            conexion.close()
            index = self.usuarios_ya_validados.index('admin')
            self.usuarios_ya_validados_pass[index] = password_nueva_md5
            self.notificarPassword()

        # OPTIMIZE: Este metodo esta duplicado con el de la clase
        # sincronizador
        def notificarPassword(self):
            try:
                conexion_db = sqlite3.connect(config.PATH_DB)
                cursor = conexion_db.cursor()
                password = cursor.execute(
                    'select password from instalacion').fetchone()[0]
                peticionRemota = peticion.Peticion()
                respuesta = peticionRemota.informarNuevaPassword(
                    password)
                if respuesta == 'Informada':
                    md5_password_nueva = \
                        hashlib.md5(password.encode('utf-8')).hexdigest()
                    cursor.execute('update instalacion set passwordnotificada=?, '\
                    'password=?, credencial=?', (1, '', md5_password_nueva,))
                cursor.close()
                conexion_db.commit()
            except sqlite3.OperationalError, msg:
                cursor.close()
                conexion_db.rollback()
                self.modulo_logger.log(logging.ERROR, "No se pudo obtener la pass"\
                " para notificarla.\nError: %s" % msg)


        def setPassword(self, usuario, password):
            password_md5 = self.md5sum(password)
            conexion = sqlite3.connect(config.PATH_DB)
            cursor = conexion.cursor()
            cursor.execute('update usuarios set password=? ,passwordseteada=? '\
            'where username=? and passwordseteada=?',
            (password_md5, 1, usuario, 0))
            # esta nofificada, porque le llega el mail del registro con la pass
            cursor.execute('update instalacion set ' \
            'passwordnotificada=?, credencial=?', (1, password_md5,))
            conexion.commit()
            conexion.close()

        def usuario_valido(self, user, pwd):
            """Verifica si el usuario esta en la base o en cache"""
            if user not in self.usuarios_ya_validados:
                pwd = self.md5sum(pwd)
                if user != "NoBody":
                    conexion = sqlite3.connect(config.PATH_DB)
                    cursor = conexion.cursor()
                    cursor.execute('select id from usuarios where username=? '\
                    'and password =?', (user, pwd))
                    salida = len(cursor.fetchall())
                    conexion.close()
                    if (salida < 1):
                        return False
                self.usuarios_ya_validados.append(user)
                self.usuarios_ya_validados_pass.append(pwd)
                return True
            else:
                if (self.md5sum(pwd) == \
                self.usuarios_ya_validados_pass[\
                self.usuarios_ya_validados.index(user)]):
                    return True
                else:
                    return False

        def agregarUsuario(self, nombre):
            """Si es valido el usuario y no esta en cache, lo agrega"""
            user = usuario.Usuario(nombre)
            self.usuarios.append(user)
            return user

        def obtenerUsuario(self, nombreusuario):
            """Busca el usuario en la cache de usuarios"""
            for usuario in self.usuarios:
                if usuario.nombre == nombreusuario:
                    return usuario
            # Si no devolvio nada, entonces lo agrego
            usuario = self.agregarUsuario(nombreusuario)
            return usuario

        def cantidadDeUsuarios(self):
            """Devuelve la cantidad de usuarios creados en la base de datos,
            sin contar el usuario admin"""
            conexion = sqlite3.connect(config.PATH_DB)
            cursor = conexion.cursor()
            salida = cursor.execute('select count(id) from usuarios where '\
            'username <> ? ', ('admin', )).fetchone()
            conexion.close()
            return salida

        def sePermiteNoLogin(self):
            """Solo se permite el no ingreso de usuario y contrasena si no hay
             usuarios creados"""
            cant = self.cantidadDeUsuarios()
            return (cant == 0)

def main():
    pass

# Importante: los módulos no deberían ejecutar
# código al ser importados
if __name__ == '__main__':
    main()