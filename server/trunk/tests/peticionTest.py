# -*- coding: utf-8 -*-

"""Test de unidad para peticion.py"""

# Modulos externos
import sys
import unittest
import urllib2
import time
import hashlib

# Modulos propios

# Variables globales
global servidor, ultimo_id
ultimo_id = 0
servidor = 'http://kerberuscontrolparental.appspot.com/'
servidor = 'http://localhost:8080/'

def md5sum(t):
    try:
        return hashlib.md5(t.encode('utf-8')).hexdigest()
    except:
        print "No se pudo obtener el hash md5 de %s" % t

class testServidor(unittest.TestCase):

        def obtenerRespuesta(self, headers, timeout=120):
            proxy = {}
            proxy_handler = urllib2.ProxyHandler(proxy)
            opener = urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)
            if 'UserID' not in headers:
                headers['UserID'] = 1

            if 'ServerID' not in headers:
                headers['ServerID'] = 4

            if 'Version' not in headers:
                headers['Version'] = '1.1'

            if 'Credencial' not in headers:
                headers['Credencial'] = md5sum(u'Credencial-Test')

            if 'Nombre' not in headers:
                headers['Nombre'] = u'Nombre-Test'

            req = urllib2.Request(servidor, headers=headers)
            respuesta = urllib2.urlopen(req, timeout=timeout).read()
            return respuesta

        def test1_getPeriodoDeActualizacion(self):
            headers = {}
            headers['Peticion'] = 'getPeriodoDeActualizacion'
            respuesta = self.obtenerRespuesta(headers)
            print "\nRespuesta: %s\n" % respuesta
            self.assertTrue(respuesta == '4320')

        def test2_getPeriodoDeRecargaCompleta(self):
            headers = {}
            headers['Peticion'] = 'getPeriodoDeRecargaCompleta'
            respuesta = self.obtenerRespuesta(headers)
            print "\nRespuesta: %s\n" % respuesta
            self.assertTrue(respuesta == '86400')

        def test3_obtenerDominiosPermitidos(self):
            headers = {}
            headers['Peticion'] = 'obtenerDominiosPermitidos'
            headers['UltimaSync'] = 0
            respuesta = self.obtenerRespuesta(headers)
            print "\nRespuesta: %s\n" % respuesta
            self.assertTrue(respuesta != '')

        def test4_obtenerDominiosDenegados(self):
            headers = {}
            headers['Peticion'] = 'obtenerDominiosDenegados'
            headers['UltimaSync'] = 0
            respuesta = self.obtenerRespuesta(headers)
            print "\nRespuesta: %s\n" % respuesta
            self.assertTrue(respuesta != '')

        def test5_chequearActualizacionesWindows(self):
            headers = {}
            headers['Peticion'] = 'chequearActualizaciones'
            headers['Plataforma'] = 'Windows'
            respuesta = self.obtenerRespuesta(headers)
            print "\nRespuesta: %s\n" % respuesta
            self.assertTrue(respuesta == 'No,No')

        def test6_chequearActualizacionesLinux(self):
            headers = {}
            headers['Peticion'] = 'chequearActualizaciones'
            headers['Plataforma'] = 'Linux'
            respuesta = self.obtenerRespuesta(headers)
            print "\nRespuesta: %s\n" % respuesta
            self.assertTrue(respuesta == 'No,No')

        def test7_obtenerDominiosDenegados(self):
            headers = {}
            headers['Peticion'] = 'obtenerDominiosDenegados'
            headers['UltimaSync'] = time.time()
            respuesta = self.obtenerRespuesta(headers)
            print "\nRespuesta: %s\n" % respuesta
            self.assertTrue(respuesta == '')

        def test8_registrarUsuario(self):
            headers = {}
            headers['Peticion'] = 'registrarUsuario'
            headers['Nombre'] = u'test-Nombre'
            headers['Email'] = u'maximiliano@boscovich.com.ar'
            headers['Password'] = u'test-Credencial'
            headers['Version'] = u'1.1'
            headers['Idioma'] = u'es'
            respuesta = self.obtenerRespuesta(headers)
            print "\nRespuesta: %s\n" % respuesta
            user_id, server_id = respuesta.split(',')
            global ultimo_id
            ultimo_id = int(user_id)
            self.assertTrue(int(user_id) and int(server_id))


        def test9_cambiarPassword(self):
            headers = {}
            nueva_pass = u'nuevapass'
            nueva_pass_quoted = urllib2.quote(nueva_pass.encode('utf8'), safe='/')
            pass_vieja_md5 = md5sum(u'test-Credencial')
            headers['Peticion'] = 'informarNuevaPassword'
            headers['UserID'] = ultimo_id
            headers['ServerID'] = 4
            headers['Credencial'] = pass_vieja_md5
            headers['PasswordVieja'] = pass_vieja_md5
            headers['PasswordNueva'] = nueva_pass_quoted
            
            respuesta = self.obtenerRespuesta(headers)
            print "\nRespuesta: %s\n" % respuesta
            self.assertTrue(respuesta=='True')

        def test_10_eliminarUsuario(self):
            headers = {}
            credencial = md5sum(u'nuevapass')
            headers['Peticion'] = 'eliminarUsuario'
            headers['UserID'] = ultimo_id
            headers['ServerID'] = 4
            headers['Credencial'] = credencial
            respuesta = self.obtenerRespuesta(headers)
            print "\nRespuesta: %s\n" % respuesta
            self.assertTrue(respuesta=='True')


        def test_11_eliminarUsuarioInexistente(self):
            headers = {}
            headers['Peticion'] = 'eliminarUsuario'
            headers['UserID'] = ultimo_id
            headers['ServerID'] = '4'
            headers['Credencial'] = 'test-Credencial'
            respuesta = self.obtenerRespuesta(headers)
            print "\nRespuesta: %s\n" % respuesta
            self.assertTrue(respuesta=='False')

        def test_12_recordarPassword(self):
            headers = {}
            headers['Peticion'] = 'recordarPassword'
            headers['UserID'] = 1
            headers['ServerID'] = 4
            respuesta = self.obtenerRespuesta(headers)
            print "\nRespuesta: %s\n" % respuesta
            self.assertTrue(respuesta=='Recordada')

        def test_13_rememberPassword(self):
            headers = {}
            headers['Peticion'] = 'recordarPassword'
            headers['UserID'] = 2
            headers['ServerID'] = 4
            respuesta = self.obtenerRespuesta(headers)
            print "\nRespuesta: %s\n" % respuesta
            self.assertTrue(respuesta=='Recordada')            

        def test_14_dominioDenegado(self):
            headers = {}
            headers['Peticion'] = 'validarUrl'
            headers['URL'] = 'http://www.redtube.com'
            headers['UserID'] = 2
            headers['ServerID'] = 4
            req = urllib2.Request(servidor, headers=headers)
            try:
                respuesta = urllib2.urlopen(req, timeout=20)
                status_code = respuesta.code
            except urllib2.HTTPError, e:
                status_code = e.code      
            self.assertTrue(status_code == 403) 

        def test_15_dominioPermitido(self):
            headers = {}
            headers['Peticion'] = 'validarUrl'
            headers['URL'] = 'http://www.yahoo.com'
            headers['UserID'] = 2
            headers['ServerID'] = 4
            req = urllib2.Request(servidor, headers=headers)
            try:
                respuesta = urllib2.urlopen(req, timeout=20)
                status_code = respuesta.code
            except urllib2.HTTPError, e:
                status_code = e.code      
            self.assertTrue(status_code == 204) 

        def test_16_usuarioRegistrado(self):
            headers = {}
            headers['Peticion'] = 'usuarioRegistrado'
            headers['Email'] = u'maximiliano@boscovich.com.ar'
            headers['UserID'] = 701
            headers['ServerID'] = 1
            respuesta = self.obtenerRespuesta(headers)
            print "\nRespuesta: %s\n" % respuesta
            respuesta = respuesta == 'True'
            self.assertTrue(respuesta)

if __name__ == '__main__':
    unittest.main()
