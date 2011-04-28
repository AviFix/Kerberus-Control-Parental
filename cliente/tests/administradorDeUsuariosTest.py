# -*- coding: utf-8 -*-

"""Test de unidad para administradorDeUsuarios.py"""

# Modulos externos
import sys,  unittest

# Modulos propios
sys.path.append('../clases')
sys.path.append('../conf')

import administradorDeUsuarios,  config

# Sobreescribo la variable global de la base para que use la de prueba 
config.PATH_DB='kerberus-test.db'

class loginDeUsuarios(unittest.TestCase):   
        admDeUsuarios=administradorDeUsuarios.AdministradorDeUsuarios()
        
        def   test1LoginDeUsuario(self):
            """El usuario test_user debe existir en la base de datos"""
            self.assertTrue(self.admDeUsuarios.usuario_valido('test_user', 'test'))
            
        def   test2LoginDeUsuarioAdmin(self):
            """El usuario test_admin debe existir en la base de datos"""
            self.assertTrue(self.admDeUsuarios.usuario_valido('test_admin', 'test'))
            
        def   test3LoginDeNoUser(self):
            """No debe permitir usuarios que no esten registrados"""
            self.assertFalse(self.admDeUsuarios.usuario_valido('NoUser', ''))

        def   test4LoginSinUsuarioNiPassword(self):
            """El login sin password debe permitirse"""
            admDeUsuarios=administradorDeUsuarios.AdministradorDeUsuarios()
            # Sobreescribo la variable global de la base para que use la de prueba sin usuarios 
            config.PATH_DB='kerberus-test-sin-usuarios.db'
            self.assertTrue(admDeUsuarios.usuario_valido('', ''))
            config.PATH_DB='kerberus-test.db'
            
        def test5CantidadDeUsuarios(self):
            """La cantidad de usuarios tiene que ser mayor o igual a cero"""
            self.assertTrue(self.admDeUsuarios.cantidadDeUsuarios() >= 0)
            
        def test6ExisteAdmin(self):
            """El usuario admin debe existir en la base de datos"""
            self.assertTrue(self.admDeUsuarios.usuario_valido('admin', 'perico'))
        
        def test7PermitirNoLogin(self):
            """Solo se debe permitir no ingresar ni usuario y password si no hay creados usuarios en la bd"""
            self.assertTrue(self.admDeUsuarios.usuario_valido('', ''))
            
if __name__ == '__main__':
    unittest.main()
