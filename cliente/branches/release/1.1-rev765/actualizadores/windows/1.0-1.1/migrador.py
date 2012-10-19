import sqlite3
import hashlib

conexion = sqlite3.connect('kerberus.db')
cursor = conexion.cursor()
password = cursor.execute('select password from instalacion;').fetchone()[0]
credencial = hashlib.md5(password).hexdigest()
cursor.execute('ALTER TABLE instalacion ADD COLUMN credencial TEXT default %s;' % credencial)
cursor.execute('ALTER TABLE instalacion ADD COLUMN serverid INTEGER default 1;')
conexion.commit()
conexion.close()
