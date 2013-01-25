# -*- coding: utf-8 -*-

"""Test de unidad para peticion.py"""
# Este modulo esta muy acoplado con registrar y no esta bueno el tema de los
# tests hasta que no se limpie un poco

# Modulos externos
import sys
import unittest
import sqlite3

# Modulos propios
sys.path.append('../clases')
sys.path.append('../conf')

import sincronizador
import config


# Sobreescribo la variable global de la base para que use la de prueba
config.PATH_DB = 'kerberus-test.db'


class verificadorDeSincronizacion(unittest.TestCase):

        @unittest.skip("Falta implementar")
        def test1VerificarNuevaVersion(self):
            """Verifica si se le informa de una nueva version"""
            pass
        @unittest.skip("Falta implementar")
        def test2ObtenerPeriodoDeActualizacion(self):
            """Verifica si obtiene el periodo de actualizacion"""
            pass

        @unittest.skip("Falta implementar")
        def test3obtenerHoraServidor(self):
            """Verifica si se obtiene la hora del servidor"""
            pass

        @unittest.skip("Falta implementar")
        def test4RegistrarUsuario(self):
            """Prueba de registro un usuario"""
            pass

        @unittest.skip("Falta implementar")
        def test5EliminacionDeusuario(self):
            """Eliminacion correcta de usuario"""
            pass

if __name__ == '__main__':
    unittest.main()
