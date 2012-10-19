import sqlite3
import hashlib

try:
    conexion = sqlite3.connect('kerberus.db')
    cursor = conexion.cursor()
    respuesta = cursor.execute('select password from instalacion;').fetchone()
    if respuesta:
        password = respuesta[0]
        credencial = hashlib.md5(password).hexdigest()
        cursor.execute('ALTER TABLE instalacion ADD COLUMN credencial TEXT')
        cursor.execute('ALTER TABLE instalacion ADD COLUMN serverid INTEGER')
        registro = [(1, credencial, '', '1.1'),]
        cursor.executemany('update instalacion set serverid=?, credencial=?, '
                        'password=?, version=?', (registro),)
        conexion.commit()
        conexion.close()
except:
    pass
