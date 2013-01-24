# -*- coding: utf-8 -*-

"""Test de unidad para el modulo usuario.py"""

# Modulos externos
import sys,  unittest, sqlite3, time

# Modulos propios
sys.path.append('../clases')

import usuario
import config


class verificadorUsuarios(unittest.TestCase):
    username = 'NoBody'
    password = 'abril22'
    adminuser = 'admin'

    def testUserAdmin(self):
        """Prueba que si se le pasa el usuario test_admin,
        devuelva que es admin"""
        usuarioAdmin = usuario.Usuario(self.adminuser)
        self.assertTrue(usuarioAdmin.es_admin)

    def testUserNoAdmin(self):
        """Prueba que si se le pasa el usuario test_user,
        devuelva que NO es admin"""
        usuarioNoAdmin = usuario.Usuario(self.username)
        self.assertFalse(usuarioNoAdmin.es_admin)

    def testRecargaCacheDenegadas(self):
        """Prueba la recarga de la cache de denegadas"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor = conexion.cursor()
        hora_url = time.time()
        url = "http://urldeprueba.com/prueba"
        cursor.execute(
            'insert into cache_urls_denegadas(url,hora) values (?,?)',
            (url, hora_url, )
            )
        conexion.commit()
        usuarioPrueba = usuario.Usuario(self.username)
        usuarioPrueba.recargarCacheDenegadas()
        cursor.execute(
            'delete from cache_urls_denegadas where url=? and hora=?',
            (url, hora_url, )
            )
        conexion.commit()
        conexion.close()
        self.assertTrue(url in usuarioPrueba.cache_urls_denegadas)

    def testRecargaCacheAceptadas(self):
        """Prueba la recarga de la cache de aceptadas"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor = conexion.cursor()
        hora_url = time.time()
        url = "http://urldeprueba.com/prueba"
        cursor.execute(
            'insert into cache_urls_aceptadas(url,hora) values (?,?)',
            (url, hora_url, )
            )
        conexion.commit()
        usuarioPrueba = usuario.Usuario(self.username)
        usuarioPrueba.recargarCacheAceptadas()
        cursor.execute(
            'delete from cache_urls_aceptadas where url=? and hora=?',
            (url, hora_url, )
            )
        conexion.commit()
        conexion.close()
        self.assertTrue(url in usuarioPrueba.cache_urls_aceptadas)

    def testRecargaDominiosPermitidos(self):
        """Prueba la recarga de los dominios permitidos"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor = conexion.cursor()
        usuarioPrueba = usuario.Usuario(self.username)
        url = "http://urldeprueba.com/prueba"
        cursor.execute(
            'insert into dominios_permitidos(url,usuario) values (?,?)',
            (url, usuarioPrueba.id, )
            )
        conexion.commit()
        usuarioPrueba.recargarDominiosPermitidos()
        cursor.execute(
            'delete from dominios_permitidos where url=? and usuario=?',
            (url, usuarioPrueba.id, )
            )
        conexion.commit()
        conexion.close()
        self.assertTrue(url in usuarioPrueba.dominios_permitidos)

    def testRecargaDominiosDenegados(self):
        """Prueba la recarga de los dominios denegados"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor = conexion.cursor()
        usuarioPrueba=usuario.Usuario(self.username)
        url="http://urldeprueba.com/prueba"
        cursor.execute('insert into dominios_denegados(url,usuario) values (?,?)',(url,usuarioPrueba.id, ))
        conexion.commit()
        usuarioPrueba.recargarDominiosDenegados()
        cursor.execute('delete from dominios_denegados where url=? and usuario=?',(url,usuarioPrueba.id, ))
        conexion.commit()
        conexion.close()
        self.assertTrue(url in usuarioPrueba.dominios_denegados)

    def testRecargaDominiosPublicamenteDenegados(self):
        """Prueba la recarga de los dominios publicamente denegados"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor=conexion.cursor()
        hora_url=time.time()
        usuarioPrueba=usuario.Usuario(self.username)
        url="http://urldeprueba.com/prueba"
        cursor.execute('insert into dominios_publicamente_denegados(url) values (?)',(url, ))
        conexion.commit()
        usuarioPrueba.recargarDominiosPublicamenteDenegados()
        cursor.execute('delete from dominios_publicamente_denegados where url=?',(url, ))
        conexion.commit()
        conexion.close()
        self.assertTrue(url in usuarioPrueba.dominios_publicamente_denegados)

    def testRecargaDominiosPublicamentePermitidos(self):
        """Prueba la recarga de los dominios publicamente permitidos"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor=conexion.cursor()
        hora_url=time.time()
        usuarioPrueba=usuario.Usuario(self.username)
        url="http://urldeprueba.com/prueba"
        cursor.execute('insert into dominios_publicamente_permitidos(url) values (?)',(url,))
        conexion.commit()
        usuarioPrueba.recargarDominiosPublicamentePermitidos()
        cursor.execute('delete from dominios_publicamente_permitidos where url=?',(url,))
        conexion.commit()
        conexion.close()
        self.assertTrue(url in usuarioPrueba.dominios_publicamente_permitidos)

    def testVerificarDominioPublicamentePermitido(self):
        """Se reconocen los dominios publicamente permitidos"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor=conexion.cursor()
        hora_url=time.time()
        usuarioPrueba=usuario.Usuario(self.username)
        url="http://urldeprueba.com/prueba"
        dominio="urldeprueba.com"
        cursor.execute('insert into dominios_publicamente_permitidos(url) values (?)',(dominio,))
        conexion.commit()
        usuarioPrueba.recargarDominiosPublicamentePermitidos()
        self.assertTrue(usuarioPrueba.dominioPublicamentePermitido(url))
        cursor.execute('delete from dominios_publicamente_permitidos where url=? ',(dominio, ))
        conexion.commit()
        conexion.close()

    def testVerificarDominioPublicamenteDenegado(self):
        """Se reconocen los dominios publicamente denegados"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor=conexion.cursor()
        hora_url=time.time()
        usuarioPrueba=usuario.Usuario(self.username)
        url="http://urldeprueba.com/prueba"
        dominio="urldeprueba.com"
        cursor.execute('insert into dominios_publicamente_denegados(url) values (?)',(dominio, ))
        conexion.commit()
        usuarioPrueba.recargarDominiosPublicamenteDenegados()
        self.assertTrue(usuarioPrueba.dominioPublicamenteDenegado(url))
        cursor.execute('delete from dominios_publicamente_denegados where url=? ',(dominio, ))
        conexion.commit()
        conexion.close()

    def testVerificarDominioDenegado(self):
        """Se reconocen los dominios denegados locales"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor=conexion.cursor()
        usuarioPrueba=usuario.Usuario(self.username)
        url="http://urldeprueba.com/prueba"
        cursor.execute('insert into dominios_denegados(url,usuario) values (?,?)',(url,usuarioPrueba.id, ))
        conexion.commit()
        usuarioPrueba.recargarDominiosDenegados()
        self.assertTrue(usuarioPrueba.dominioDenegado(url))
        cursor.execute('delete from dominios_denegados where url=? and usuario=?',(url,usuarioPrueba.id, ))
        conexion.commit()
        conexion.close()

    def testVerificarDominioPermitidos(self):
        """Se reconocen los dominios permitidos locales"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor=conexion.cursor()
        usuarioPrueba=usuario.Usuario(self.username)
        url="http://urldeprueba.com/prueba"
        cursor.execute('insert into dominios_permitidos(url,usuario) values (?,?)',(url,usuarioPrueba.id, ))
        conexion.commit()
        usuarioPrueba.recargarDominiosPermitidos()
        self.assertTrue(usuarioPrueba.dominioPermitido(url))
        cursor.execute('delete from dominios_permitidos where url=? and usuario=?',(url,usuarioPrueba.id, ))
        conexion.commit()
        conexion.close()

    def testCacheAceptadas(self):
        """Se reconoce la cache de aceptadas"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor=conexion.cursor()
        hora_url=time.time()
        url="http://urldeprueba.com/prueba"
        cursor.execute('insert into cache_urls_aceptadas(url,hora) values (?,?)',(url,hora_url, ))
        conexion.commit()
        usuarioPrueba=usuario.Usuario(self.username)
        usuarioPrueba.recargarCacheAceptadas()
        cursor.execute('delete from cache_urls_aceptadas where url=? and hora=?',(url,hora_url, ))
        conexion.commit()
        conexion.close()
        self.assertTrue(usuarioPrueba.cacheAceptadas(url))

    def testCacheDenegadas(self):
        """Se reconoce la cache de denegadas"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor=conexion.cursor()
        hora_url=time.time()
        url="http://urldeprueba.com/prueba"
        cursor.execute('insert into cache_urls_denegadas(url,hora) values (?,?)',(url,hora_url, ))
        conexion.commit()
        usuarioPrueba=usuario.Usuario(self.username)
        usuarioPrueba.recargarCacheDenegadas()
        cursor.execute('delete from cache_urls_denegadas where url=? and hora=?',(url,hora_url, ))
        conexion.commit()
        conexion.close()
        self.assertTrue(usuarioPrueba.cacheDenegadas(url))

    def testPersistirCacheAceptadas(self):
        """Se puede persistir en la db la cache de acpetadas"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor=conexion.cursor()
        hora_url=time.time()
        url="http://urldepruebaapersisitir.com/persistir/url"
        usuarioPrueba=usuario.Usuario(self.username)

        for i in range(0, config.MAX_CACHE_URLS_ACEPTADAS+1):
            usuarioPrueba.persistirACacheAceptadas(url+str(i))

        usuarioPrueba.recargarCacheAceptadas()

        for i in range(0, config.MAX_CACHE_URLS_ACEPTADAS+1):
            self.assertTrue(usuarioPrueba.cacheAceptadas(url+str(i)))

        cursor.executemany('delete from cache_urls_aceptadas where url like ?',(url+"%"))
        conexion.commit()
        conexion.close()

    def testPersistirCacheDenegadas(self):
        """Se puede persistir en la db la cache de denegadas"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor=conexion.cursor()
        hora_url=time.time()
        url="http://urldepruebaapersisitir.com/persistir/url"
        usuarioPrueba=usuario.Usuario(self.username)

        for i in range(0, config.MAX_CACHE_URLS_DENEGADAS+1):
            usuarioPrueba.persistirACacheDenegadas(url+str(i))

        usuarioPrueba.recargarCacheDenegadas()

        for i in range(0, config.MAX_CACHE_URLS_DENEGADAS+1):
            self.assertTrue(usuarioPrueba.cacheDenegadas(url+str(i)))

        cursor.executemany('delete from cache_urls_denegadas where url like ?',(url+"%"))
        conexion.commit()
        conexion.close()

    def testValfdacionRemota(self):
        """El servidor valida correctamente las urls permitidas"""
        usuarioPrueba=usuario.Usuario(self.username)
        url="http://www.google.com"
        respuesta, mensaje=usuarioPrueba.validarRemotamente(url)
        self.assertTrue(respuesta)
        self.assertEqual(mensaje, "")

    def testRechazoRemota(self):
        """El servidor rechaza correctamente las urls denegadas"""
        usuarioPrueba=usuario.Usuario(self.username)
        url="http://www.redtube.net"
        respuesta, mensaje=usuarioPrueba.validarRemotamente(url)
        self.assertFalse(respuesta)


if __name__ == '__main__':
    unittest.main()
