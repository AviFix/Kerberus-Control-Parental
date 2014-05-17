# -*- coding: utf-8 -*-

# Modulos externos
import sys

sys.path.append('clases')
sys.path.append('conf')
sys.path.append('password')

# Modulos propios
import config
import loguear

# esto va primero porque sino cuando se importan los modulos restantes,
# necesitan el modulo_logger
modulo_logger = loguear.logSetup(
    config.SYNC_LOG_FILENAME,
    config.SYNC_LOGLEVEL, config.SYNC_LOG_SIZE_MB,
    config.SYNC_LOG_CANT_ROTACIONES, 'kerberus'
    )


import sincronizador
import servidores
import peticion

servers = servidores.Servidor()
peticionRemota = peticion.Peticion(servers)

# Lanza el sincronizador
syncd = sincronizador.Sincronizador(peticionRemota)
syncd.checkRegistro()
syncd.checkPasswordNotificada()
syncd.obtenerDatosDeActualizacion()
syncd.run()
