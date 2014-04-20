# -*- coding: utf-8 -*-

# Modulos externos
import sys

# Modulos propios
sys.path.append('clases')
sys.path.append('conf')
sys.path.append('password')

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
modulo_logger.info('creando objeto server 1')
servers = servidores.Servidor()
modulo_logger.info('Fin creacion objeto server 1')
peticionRemota = peticion.Peticion(servers)

# Lanza el sincronizador
syncd = sincronizador.Sincronizador(peticionRemota)

syncd.run()
