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
