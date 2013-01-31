# -*- coding: utf-8 -*-

"""Test de unidad para servidores.py"""

# Modulos externos
import sys
import unittest

# Modulos propios
sys.path.append('../clases')

from peticion import Peticion

class verificadorDeSincronizacion(unittest.TestCase):
        """clase que contiene los tests de servidores.py"""
        global pedido
        pedido = Peticion()

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
            hora_actual = time.time()
            respuesta = pedido.obtenerHoraServidor()
            self.assertTrue(hora_actual <= respuesta)


if __name__ == '__main__':
    unittest.main()
