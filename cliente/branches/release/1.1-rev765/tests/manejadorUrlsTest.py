# -*- coding: utf-8 -*-

"""Test de unidad para el modulo manejadorUrls.py"""

# Modulos externos
import sys
import unittest

# Modulos propios
sys.path.append('../clases')
import manejadorUrls


class modificadoresUrls(unittest.TestCase):
    buscadores_con_SafeSearch = (
        ("Google", "http://www.google.com/search?", "&safe=active"),
        ("Yahoo", "http://www.yahoo.com/search", "&vm=r"),
        ("Bing", "http://www.bing.com/search?q=securedfamily", "&adlt=strict"),
        ("Youtube", "http://www.youtube.com/results?", "&safe=active")
    )
    buscadores_sin_SafeSearch = (
        ("Exalead", "http://www.exalead.com/search/"),
        )
    verificador = manejadorUrls.ManejadorUrls()

    def test1DeteccionCorrectaDeBuscador(self):
        """Verificar que se detecten correctamente los buscadores
        conocidos y manejados"""
        for buscador, url, agregado in self.buscadores_con_SafeSearch:
            self.assertEqual(
                buscador,
                self.verificador.identificarBuscador(url)
                    )

    def test2DeteccionCorrectaDeSafeSearch(self):
        """Verifica que se detecten correctamente los navegadores que
        soportan SafeSearch"""
        for buscador, url, agregado in self.buscadores_con_SafeSearch:
            self.assertTrue(self.verificador.soportaSafeSearch(url))

    def test3NavegadoresSinSafeSearch(self):
        """Verifica que no se detecte el safesearch en navegadores
        que no lo tienen"""
        for buscadores, url in self.buscadores_sin_SafeSearch:
            self.assertFalse(self.verificador.soportaSafeSearch(url))

    def test4ForzadoDeSafeSearch(self):
        """Verifica que para cada navegador con soporte de safesearch,
        se le agregue lo correcto para forzarlo"""
        for buscador, url, agregado in self.buscadores_con_SafeSearch:
            self.assertEqual(
                self.verificador.agregarSafeSearch(url),
                url + agregado,
                )

    def test5NoSeFuerzaSafeSearch(self):
        """Verifica que para cada navegador que NO soporte de safesearch,
        No se le agregue safesearch"""
        for buscador, url in self.buscadores_sin_SafeSearch:
            self.assertEqual(self.verificador.agregarSafeSearch(url), url)

if __name__ == '__main__':
    unittest.main()
