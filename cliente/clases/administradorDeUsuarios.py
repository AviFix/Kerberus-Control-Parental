import sqlite3, time,  hashlib, platform, os

from funciones import *
from usuario import *

MAX_CACHE_URLS_ACEPTADAS=1000
MAX_CACHE_URLS_DENEGADAS=30
DEBUG_TIEMPOS=True
SECUREDFAMILYSERVER="securedfamily.no-ip.org:8081"
#SECUREDFAMILYSERVER="127.0.0.1:8081"
if  platform.uname()[0] == 'Linux':
    PATH_DB='/var/cache/securedfamily/securedfamily.db'
else:
    PATH_DB='C:\securedfamily.db'

if not os.path.exists(PATH_DB):
    crearDBCliente(PATH_DB)

def obtenerTiempoParcial(inicio):
    fin=LOG_FILENAME, LOG_SIZE_MB, LOG_CANT_ROTACIONES, time.time()
    return fin-inicio    


class AdministradorDeUsuarios:
        def __init__(self):
            self.usuarios = []
            self.usuarios_ya_validados = []
            self.usuarios_ya_validados_pass = []
            
        def md5sum(self, t):
            return hashlib.md5(t).hexdigest()
    
        def usuario_valido(self, user, pwd):
            if user not in self.usuarios_ya_validados:
                conexion = sqlite3.connect(PATH_DB)
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
            usuario = Usuario(nombre)
            self.usuarios.append(usuario)
            return usuario
        
        def obtenerUsuario(self, nombreusuario):
            for usuario in self.usuarios:
                if usuario.nombre == nombreusuario:
                    return usuario
            # Si no devolvio nada, entonces lo agrego
            usuario=self.agregarUsuario(nombreusuario)
            return usuario
