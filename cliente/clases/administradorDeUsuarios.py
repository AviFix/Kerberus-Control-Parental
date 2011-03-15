# -*- coding: utf-8 -*-

"""Modulo encargado de verificar si el usuario ingresado por el cliente es valido"""

#Modulos externos
import sqlite3, time,  hashlib,  os

#Modulos propios
import usuario
import config

#Excepciones
class AdministradorDeUsuariosError(Exception): pass
class DatabaseError(AdministradorDeUsuariosError): pass
class UsuarioNoValido(AdministradorDeUsuariosError): pass

# Clase
class AdministradorDeUsuarios:
        def __init__(self):
            if not os.path.exists(config.PATH_DB):
                raise DatabaseError, "La base de datos no existe, o usted no posee permisos para accederla"
            self.usuarios = []
            self.usuarios_ya_validados = []
            self.usuarios_ya_validados_pass = []
            
        def md5sum(self, t):
            return hashlib.md5(t).hexdigest()
    
        def usuario_valido(self, user, pwd):
            """Verifica si el usuario esta en la base o en cache"""
            if user not in self.usuarios_ya_validados:
                if user == "":
                    if self.sePermiteNoLogin():
                        return False
                    else:
                        return True
                
                conexion = sqlite3.connect(config.PATH_DB)
                cursor=conexion.cursor()
                password=self.md5sum(pwd)
                cursor.execute('select id from usuarios where username=? and password =?',(user, password ))
                salida=len(cursor.fetchall())
                conexion.close()
                if (salida < 1):
                   return False
                self.usuarios_ya_validados.append(user)
                self.usuarios_ya_validados_pass.append(password)
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
                
