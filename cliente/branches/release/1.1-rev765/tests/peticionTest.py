# -*- coding: utf-8 -*-

"""Test de unidad para peticion.py"""

# Modulos externos
import sys
import unittest

# Modulos propios
sys.path.append('../clases')

from peticion import Peticion, config

# Seteo el path a la base utilizada para los tests
config.PATH_DB = "kerberus-test.db"

class verificadorDeSincronizacion(unittest.TestCase):

        global pedido
        pedido = Peticion()
        pedido.server_ip = "127.0.0.1"
        pedido.server_port = 443
        pedido.server_sync = "%s:%s" % ("127.0.0.1", 443)

        def test1ObtenerPeriodoDeActualizacion(self):
            """Verifica si obtiene el periodo de actualizacion"""
            respuesta = pedido.obtenerPeriodoDeActualizacion()
            self.assertFalse(respuesta == 1)

        def test2obtenerHoraServidor(self):
            """Verifica si se obtiene la hora del servidor"""
            import time
            hora_actual = time.time()
            respuesta = pedido.obtenerHoraServidor()
            self.assertTrue(hora_actual <= respuesta)

        def test3VerificarNuevaVersionParaWindows(self):
            """Verifica si se le informa de una nueva version si la """
            """plataforma es Windows"""
            config.PLATAFORMA = 'Windows'
            actualizacion, md5 = pedido.chequearActualizaciones()
            self.assertTrue(actualizacion is not None and
                            md5 == '52199ce5ebc8fd6934f033d986d35fd7')
        def test4VerificarNuevaVersionParaLinux(self):
            """Verifica si se le informa de una nueva version si la """
            """plataforma es Linux"""
            config.PLATAFORMA = 'Linux'
            actualizacion, md5 = pedido.chequearActualizaciones()
            self.assertTrue(actualizacion is not None and
                            md5 == '52199ce5ebc8fd6934f033d986d35fd7')

        def test5RegistrarUsuario(self):
            """Prueba de registro de un usuario"""
            nombre = 'prueba'
            email = 'maximiliano@boscovich.com.ar'
            password = 'test'
            version = '1.1'
            idUsuario, idServer = pedido.registrarUsuario(
                nombre,
                email,
                password,
                version)
            idUsuario = int(idUsuario)
            idServer = int(idServer)
            pedido.userid = idUsuario
            pedido.serverid = idServer
            self.assertTrue(idServer > 0 and idUsuario > 0)

        def test6EliminacionDeusuario(self):
            """Eliminacion correcta de un usuario"""
            pedido.credencial = '098f6bcd4621d373cade4e832627b4f6'
            pedido.eliminarUsuario()



if __name__ == '__main__':
    unittest.main()
