# -*- coding: utf-8 -*-

"""Test de unidad para el modulo manejadorUrls.py"""

# Modulos externos
import sys,  unittest,  logging

# Modulos propios
sys.path.append('../clases')
import consultor

class verificadorUrls(unittest.TestCase):
    extensiones_exceptuadas=(".gif",".jpeg",".jpg",".png",".js",".css",".swf",".ico",".json",".mp3",".wav",".rss",".rar",".zip",".pdf",".xml")
    extensiones_no_exceptuadas=(".html",".htm",".txt")
    urls_aceptadas=("http://www.wikipedia.org", "http://www.google.com")
    urls_denegadas=("http://www.cuantosexo.com/", )
    urls_publicamente_permitidas=("http://www.hotmail.com", "http://www.mercadolibre.com.ar", "http://www.google.com")
    urls_publicamente_denegadas=("http://www.tiava.com", )
    verificador=consultor.Consultor()
    verificador.setLogger(logging)
    username='test_user'
    password='test'
    adminuser='test_admin'

    
    def test1VerificarExtensionesExceptuadas(self):
        """Verificar que se exceptuen las extensiones no analizables por dansguardian"""
        for extension in self.extensiones_exceptuadas:
            self.assertTrue(self.verificador.extensionValida(extension))
           
    def test2VerificarExtensionesNoExceptuadas(self):
        """Verificar que NO se exceptuen las extensiones analizables por dansguardian"""
        for extension in self.extensiones_no_exceptuadas:
            self.assertFalse(self.verificador.extensionValida(extension))
        
    def test3ChequearUrlsAceptadas(self):
        """Verifica que se acepten un conjunto de urls que se saben que son aptas"""
        for url in self.urls_aceptadas:
            respuesta, mensaje=self.verificador.validarUrl(self.username, self.password, url)
            self.assertTrue(respuesta)

    def test4ChequearUrlsDenegadas(self):
        """Verifica que se rechacen un conjunto de urls con pornografia"""
        for url in self.urls_denegadas:
            respuesta, mensaje=self.verificador.validarUrl(self.username, self.password, url)
            self.assertFalse(respuesta)            

    def test5ChequearAdmin(self):
        """Verifica que un usuario admin se reconozca como tal a la hora de validar las urls"""
        for url in self.urls_denegadas:
            respuesta, mensaje=self.verificador.validarUrl(self.adminuser, self.password, url)
            self.assertTrue(respuesta)            

    def test6ChequearUrlsPublicamenteDenegadas(self):
        """Verifica que se rechacen y reconozcan como tales los dominios publicamente denegados"""
        for url in self.urls_publicamente_denegadas:
            respuesta, mensaje=self.verificador.validarUrl(self.username, self.password, url)
            self.assertFalse(respuesta)       
            self.assertEqual(mensaje, "URL: %s <br>Motivo: Dominio publicamente denegado en el servidor" % url)

    def test7ChequearUrlsPublicamenteAceptadas(self):
        """Verifica que se acepten y reconozcan como tales los dominios publicamente permitidos"""
        for url in self.urls_publicamente_permitidas:
            respuesta, mensaje=self.verificador.validarUrl(self.username, self.password, url)
            self.assertTrue(respuesta)       
            self.assertEqual(mensaje, "Dominio publicamente permitido: %s" % url)
            
if __name__ == '__main__':
    unittest.main()
