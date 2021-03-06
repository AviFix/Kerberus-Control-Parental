#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import sys

sys.path.append('conf')
sys.path.append('clases')

import pedirUsuario
import subprocess
import registrar
import time
import config

app = QtGui.QApplication(sys.argv)
myapp = pedirUsuario.formularioUsuario('Desinstalar Kerberus',
        u'Ingrese la contraseña de administrador de Kerberus \n'
        u'(la que ingreso al momento de instalarlo)')
myapp.show()
app.exec_()
desinstalar = myapp.verificado

if desinstalar:
    if config.PLATAFORMA == 'Linux':
        desinstalador = "%s/uninstaller" % config.PATH_COMMON
        print "Ejecutando %s" % desinstalador
        subprocess.Popen(desinstalador)
        reg = registrar.Registradores()
        reg.eliminarRemotamente()
    else:
        import _winreg
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\kerberus')
        except WindowsError:
            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\kerberus')
        except:
            print "Error al leer la clave del registro kerberus-common"
        path_common = _winreg.QueryValueEx(key, 'kerberus-common')[0]
        origen = path_common + '\kcpwu.dat'
        desinstalador = path_common + '\kcpwu.exe'
        comando = "copy /Y \"%s\" \"%s\"" % (origen, desinstalador)
        subprocess.Popen(comando, stdout=subprocess.PIPE, shell=True)
        time.sleep(1)
        subprocess.call(desinstalador)
        reg = registrar.Registradores()
        reg.eliminarRemotamente()



