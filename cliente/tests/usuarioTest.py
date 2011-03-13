"""Test de unidad para el modulo usuario.py"""

# Modulos externos
import sys,  unittest, sqlite3, time

# Modulos propios
sys.path.append('../clases')
sys.path.append('../config')

import usuario
import config

class verificadorUsuarios(unittest.TestCase):
    username='test_user'
    password='test'
    adminuser='test_admin'
    
    def testUserAdmin(self):
        """Prueba que si se le pasa el usuario test_admin, devuelva que es admin"""
        usuarioAdmin=usuario.Usuario(self.adminuser)
        self.assertTrue(usuarioAdmin.es_admin)
        
    def testUserNoAdmin(self):
        """Prueba que si se le pasa el usuario test_user, devuelva que NO es admin"""
        usuarioNoAdmin=usuario.Usuario(self.username)
        self.assertFalse(usuarioNoAdmin.es_admin)

    def testRecargaCacheDenegadas(self):
        """Prueba la recarga de la cache de denegadas"""
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
        self.assertTrue(url in usuarioPrueba.cache_urls_denegadas)

    def testRecargaCacheAceptadas(self):
        """Prueba la recarga de la cache de aceptadas"""
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
        self.assertTrue(url in usuarioPrueba.cache_urls_aceptadas)

    def testRecargaDominiosPermitidos(self):
        """Prueba la recarga de los dominios permitidos"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor=conexion.cursor()
        hora_url=time.time()
        usuarioPrueba=usuario.Usuario(self.username)        
        url="http://urldeprueba.com/prueba"
        cursor.execute('insert into dominios_permitidos(url,usuario) values (?,?)',(url,usuarioPrueba.id, ))
        conexion.commit()
        usuarioPrueba.recargarDominiosPermitidos()
        cursor.execute('delete from dominios_permitidos where url=? and usuario=?',(url,usuarioPrueba.id, ))
        conexion.commit()
        conexion.close()
        self.assertTrue(url in usuarioPrueba.dominios_permitidos)

    def testRecargaDominiosDenegados(self):
        """Prueba la recarga de los dominios denegados"""
        conexion = sqlite3.connect(config.PATH_DB)
        cursor=conexion.cursor()
        hora_url=time.time()
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
        cursor.execute('insert into dominios_publicamente_denegados(url,tipo) values (?,?)',(url,1, ))
        conexion.commit()
        usuarioPrueba.recargarDominiosPublicamenteDenegados()
        cursor.execute('delete from dominios_publicamente_denegados where url=? and tipo=?',(url,1, ))
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
        cursor.execute('insert into dominios_publicamente_permitidos(url,tipo) values (?,?)',(url,1, ))
        conexion.commit()
        usuarioPrueba.recargarDominiosPublicamentePermitidos()
        cursor.execute('delete from dominios_publicamente_permitidos where url=? and tipo=?',(url,1, ))
        conexion.commit()
        conexion.close()
        self.assertTrue(url in usuarioPrueba.dominios_publicamente_permitidos)

if __name__ == '__main__':
    unittest.main()
