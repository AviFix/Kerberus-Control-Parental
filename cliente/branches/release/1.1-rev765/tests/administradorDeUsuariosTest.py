# -*- coding: utf-8 -*-

"""Test de unidad para administradorDeUsuarios.py"""

# Modulos externos
import sys
import unittest

# Modulos propios
sys.path.append('../clases')

from administradorDeUsuarios import AdministradorDeUsuarios, config

# Seteo el path a la base utilizada para los tests
config.PATH_DB = "kerberus-test.db"

class loginDeUsuarios(unittest.TestCase):
        admDeUsuarios = AdministradorDeUsuarios()

        def   test1LoginDeUsuario(self):
            """El usuario test_user debe existir en la base de datos"""
            self.assertTrue(
                self.admDeUsuarios.usuario_valido('test_user', 'test')
                )

        def   test2LoginDeUsuarioAdmin(self):
            """El usuario test_admin debe existir en la base de datos"""
            self.assertTrue(
                self.admDeUsuarios.usuario_valido('test_admin', 'test')
                )

        def   test3LoginDeNoUser(self):
            """No debe permitir usuarios que no esten registrados"""
            self.assertFalse(self.admDeUsuarios.usuario_valido('NoUser', ''))

        def test5CantidadDeUsuarios(self):
            """La cantidad de usuarios tiene que ser mayor o igual a cero"""
            self.assertTrue(self.admDeUsuarios.cantidadDeUsuarios() >= 0)

        def test6ExisteAdmin(self):
            """El usuario admin debe existir en la base de datos"""
            self.assertTrue(
                self.admDeUsuarios.usuario_valido('admin', 'test')
                )

        def test7PermitirNoLogin(self):
            """Solo se debe permitir no ingresar ni usuario y password si no
            hay creados usuarios en la bd"""
            self.assertTrue(self.admDeUsuarios.usuario_valido('', ''))

if __name__ == '__main__':
    unittest.main()
