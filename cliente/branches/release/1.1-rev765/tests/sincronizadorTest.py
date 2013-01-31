# -*- coding: utf-8 -*-

"""Test de unidad para sincronizador.py"""
# Este modulo esta muy acoplado con registrar y no esta bueno el tema de los
# tests hasta que no se limpie un poco

# Modulos externos
import sys
import unittest
import sqlite3

# Modulos propios
sys.path.append('../clases')

from sincronizador import Sincronizador, config


class verificadorDeSincronizacion(unittest.TestCase):
        global sync
        sync = Sincronizador()

        def test1SincronizacionDeDominios(self):
            """Verificacion de sincronizacion de dominios publicamente """\
            """denegados/permitidos con el server"""

            # Me conecto a la base y borro los dominios que est
            conexion_db = sqlite3.connect(config.PATH_DB)
            cursor = conexion_db.cursor()
            cursor.execute('delete from dominios_publicamente_permitidos')
            cursor.execute('delete from dominios_publicamente_denegados')
            conexion_db.commit()

            # Pido la sincronizacion
            sync.sincronizarDominiosDenegados()
            sync.sincronizarDominiosPermitidos()
            cantidadDominiosPermitidos = cursor.execute(
                'select count(*) from dominios_publicamente_permitidos'
                ).fetchone()[0]
            cantidadDominiosDenegados = cursor.execute(
                'select count(*) from dominios_publicamente_denegados'
                ).fetchone()[0]

            self.assertTrue(
                cantidadDominiosPermitidos > 0 and
                cantidadDominiosDenegados > 0
                )

if __name__ == '__main__':
    unittest.main()
