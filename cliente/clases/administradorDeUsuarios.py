# -*- coding: utf-8 -*-

"""Modulo encargado de verificar si el usuario ingresado por el cliente es valido"""

#Modulos externos
import sqlite3, time,  hashlib,  os, sys, logging

#Modulos propios
sys.path.append('../conf')
import usuario
import config
import funciones

#Excepciones
class AdministradorDeUsuariosError(Exception): pass
class DatabaseError(AdministradorDeUsuariosError): pass
class UsuarioNoValido(AdministradorDeUsuariosError): pass

# Logging
logger = funciones.logSetup (config.LOG_FILENAME, config.LOGLEVEL, config.LOG_SIZE_MB, config.LOG_CANT_ROTACIONES,"Modulo AdministradorDeUsuarios")

# Clase
class AdministradorDeUsuarios:
        def __init__(self):
            if not os.path.exists(config.PATH_DB):
                logger.log(logging.ERROR,"La base de datos no existe, o usted no posee permisos para accederla")
                raise DatabaseError, "La base de datos no existe, o usted no posee permisos para accederla"
            self.usuarios = []
            self.usuarios_ya_validados = []
            self.usuarios_ya_validados_pass = []

        def md5sum(self, t):
            return hashlib.md5(t).hexdigest()

        def passwordSeteada(self,usuario):
            conexion = sqlite3.connect(config.PATH_DB)
            cursor=conexion.cursor()
            cursor.execute('select passwordseteada from usuarios where username = ?',(usuario,))
            password_seteada=cursor.fetchone()[0]
            return password_seteada

        def cambiarPassword(self, usuario, password_vieja, password_nueva):
            password_vieja_md5=self.md5sum(password_vieja)
            password_nueva_md5=self.md5sum(password_nueva)
            conexion = sqlite3.connect(config.PATH_DB)
            cursor=conexion.cursor()
            cursor.execute('update usuarios set password=? ,passwordseteada=1 where username=? and password =?',(password_nueva_md5, usuario, password_vieja_md5, ))
            conexion.commit()
            conexion.close()

        def setPassword(self, usuario, password):
            password_md5=self.md5sum(password)
            conexion = sqlite3.connect(config.PATH_DB)
            cursor=conexion.cursor()
            cursor.execute('update usuarios set password=? ,passwordseteada=1 where username=?',(password_md5, usuario,))
            conexion.commit()
            conexion.close()

        def usuario_valido(self, user, pwd):
            """Verifica si el usuario esta en la base o en cache"""
            if user not in self.usuarios_ya_validados:
                pwd=self.md5sum(pwd)
                if user <> "NoBody":
                    conexion = sqlite3.connect(config.PATH_DB)
                    cursor=conexion.cursor()
                    cursor.execute('select id from usuarios where username=? and password =?',(user, pwd ))
                    salida=len(cursor.fetchall())
                    conexion.close()
                    if (salida < 1):
                       return False
                self.usuarios_ya_validados.append(user)
                self.usuarios_ya_validados_pass.append(pwd)
                return True
            else:
                if (self.md5sum(pwd) == self.usuarios_ya_validados_pass[self.usuarios_ya_validados.index(user)]):
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
            usuario=self.agregarUsuario(nombreusuario)
            return usuario

        def cantidadDeUsuarios(self):
            """Devuelve la cantidad de usuarios creados en la base de datos, sin contar el usuario admin"""
            conexion = sqlite3.connect(config.PATH_DB)
            cursor=conexion.cursor()
            salida=cursor.execute('select count(id) from usuarios where username <> ? ',('admin', )).fetchone()
            conexion.close()
            return salida

        def sePermiteNoLogin(self):
            """Solo se permite el no ingreso de usuario y contrasena si no hay usuarios creados"""
            cant=self.cantidadDeUsuarios()
            return (cant == 0)

