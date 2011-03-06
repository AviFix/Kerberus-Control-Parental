"""Test de unidad para administradorDeUsuarios.py"""

# Modulos externos
import sys,  unittest

# Modulos propios
sys.path.append('../clases')
import administradorDeUsuarios

class loginDeUsuarios(unittest.TestCase):   
        admDeUsuarios=administradorDeUsuarios.AdministradorDeUsuarios()
        
        def   testLoginDeUsuario(self):
            """El usuario test_user debe existir en la base de datos"""
            self.assertTrue(self.admDeUsuarios.usuario_valido('test_user', 'test'))
            
        def   testLoginDeUsuarioAdmin(self):
            """El usuario test_admin debe existir en la base de datos"""
            self.assertTrue(self.admDeUsuarios.usuario_valido('test_admin', 'test'))
            
        def   testLoginDeNoUser(self):
            """No debe permitir usuarios que no esten registrados"""
            self.assertFalse(self.admDeUsuarios.usuario_valido('NoUser', ''))

        def   testLoginSinPassword(self):
            """El login sin password debe permitirse"""
            self.assertTrue(self.admDeUsuarios.usuario_valido('usuario', ''))
            
if __name__ == '__main__':
    unittest.main()
