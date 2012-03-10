# -*- coding: utf-8 -*-

# Modulos externos
import sys

# Modulos propios
sys.path.append('clases')
sys.path.append('conf')
sys.path.append('password')

import sincronizador
import config

# Lanza el sincronizador
syncd=sincronizador.Sincronizador()

if not syncd.passwordNotificada():
    print "notificando password"
    syncd.notificarPassword()

syncd.run()


