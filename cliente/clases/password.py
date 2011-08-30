# -*- coding: utf-8 -*-

"""Modulo que permite la definicion y cambio de contraseña"""

# Modulos externos
import sqlite3, hashlib

# Modulos propios
sys.path.append('../conf')
import config

# Clase
class Password:
    def __init__(self, usuario):
        self.usuario=usuario
        conexion = sqlite3.connect(config.PATH_DB)
        self.cursor=conexion.cursor()
        self.id, self.es_admin=self.getU
