# -*- coding: utf-8 -*-

"""Test de unidad para servidores.py"""

# Modulos externos
import sys
import unittest
import sqlite3

# Modulos propios
sys.path.append('../clases')
sys.path.append('../conf')

import peticion
import config


# Sobreescribo la variable global de la base para que use la de prueba
config.PATH_DB = 'kerberus-test.db'


class verificadorDeSincronizacion(unittest.TestCase):

        global pedido
        pedido = peticion.Peticion()

        @unittest.skip("Falta implementar")
        def test1VerificarNuevaVersion(self):
            """Verifica si se le informa de una nueva version"""
            pass

        def test2ObtenerPeriodoDeActualizacion(self):
            """Verifica si obtiene el periodo de actualizacion"""
            respuesta = pedido.obtenerPeriodoDeActualizacion()
            self.assertFalse(respuesta == 1)

        def test3obtenerHoraServidor(self):
            """Verifica si se obtiene la hora del servidor"""
            import time
            hora_actual = hora = time.time()
            respuesta = pedido.obtenerHoraServidor()
            self.assertTrue(hora_actual <= respuesta)

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
