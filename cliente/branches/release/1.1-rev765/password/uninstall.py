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
        'Ingrese la password de administrador de Kerberus \n'
        '(la que ingreso al momento de instalarlo)')
myapp.show()
app.exec_()
desinstalar = myapp.verificado

if desinstalar:
    reg = registrar.Registradores()
    reg.eliminarRemotamente()
    if config.PLATAFORMA == 'Linux':
        desinstalador = "%s/uninstaller" % config.PATH_COMMON
        print "Ejecutando %s" % desinstalador
        subprocess.call(desinstalador)
    else:
        import _winreg
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\kerberus')
        path_common = _winreg.QueryValueEx(key, 'kerberus-common')[0]
        origen = path_common + '\kcpwu.dat'
        desinstalador = path_common + '\kcpwu.exe'
        comando = "move \"%s\" \"%s\"" % (origen, desinstalador)
        subprocess.Popen(comando, stdout=subprocess.PIPE, shell=True)
        time.sleep(1)
        subprocess.call(desinstalador)




