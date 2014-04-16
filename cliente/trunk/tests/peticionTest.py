# -*- coding: utf-8 -*-

"""Test de unidad para peticion.py"""

# Modulos externos
import sys
import unittest

# Modulos propios
sys.path.append('../clases')

from peticion import Peticion, config


class verificadorDeSincronizacion(unittest.TestCase):

        global pedido
        pedido = Peticion()

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
                            md5 == 'c5be3da770e081536a3f68f087a6cff0')
        def test4VerificarNuevaVersionParaLinux(self):
            """Verifica si se le informa de una nueva version si la """
            """plataforma es Linux"""
            config.PLATAFORMA = 'Linux'
            actualizacion, md5 = pedido.chequearActualizaciones()
            self.assertTrue(actualizacion is not None and
            md5 == 'c5be3da770e081536a3f68f087a6cff0')

        def test5UsuarioRegistrado(self):
            """Verifica que el usuario este registrado en el server"""
            id = 1
            email = 'maximiliano@boscovich.com.ar'
            respuesta = pedido.usuarioRegistrado(id, email)

        def test6RecordarPassword(self):
            """Test de recordar password"""
            respuesta = pedido.recordarPassword()
            self.assertTrue(respuesta == 'Recordada')

        def test7RegistrarUsuario(self):
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

        def test8InformarNuevaPassword(self):
            """Test de cambio de password"""
            respuesta = pedido.informarNuevaPassword('test')
            self.assertTrue(respuesta == 'Informada')

        #@unittest.skip("Falta implementar")
        def test9EliminacionDeusuario(self):
            """Eliminacion correcta de un usuario"""
            pedido.credencial = '098f6bcd4621d373cade4e832627b4f6'
            pedido.eliminarUsuario()

        def test10ObtenerDatos(self):
            """Obtencion correcta de los datos de usuario"""
            idUsuario, serverId, version, nombretitular, credencial = \
            pedido.obtenerDatos()
            self.assertTrue(idUsuario == 1)
            self.assertTrue(serverId == 3)
            self.assertTrue(version == "1.1")
            self.assertTrue(nombretitular == "Usuario de Desarrollo")
            self.assertTrue(credencial == "098f6bcd4621d373cade4e832627b4f6")

        def test11ObtenerPeriodoDeRecargaCompleta(self):
            """Verifica si obtiene el periodo de recarga completa"""
            respuesta = pedido.obtenerPeriodoDeRecargaCompleta()
            self.assertFalse(respuesta == 60)

if __name__ == '__main__':
    unittest.main()
