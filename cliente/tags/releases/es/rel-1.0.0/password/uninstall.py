from PyQt4 import QtGui, QtCore
import sys

sys.path.append('../')
sys.path.append('../clases')

import pedirUsuario
import funciones
import _winreg, subprocess
import registrar
import time

app = QtGui.QApplication(sys.argv)
myapp = pedirUsuario.formularioUsuario('Desinstalar Kerberus', 'Ingrese la password de administrador de Kerberus \n(la que ingreso al momento de instalarlo)')
myapp.show()
app.exec_()
desinstalar=myapp.verificado
if desinstalar:
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\kerberus')
    path_common = _winreg.QueryValueEx(key,'kerberus-common')[0]
    origen = path_common +'\kcpwu.dat'
    desinstalador = path_common +'\kcpwu.exe'
    comando = "move \"%s\" \"%s\"" % (origen, desinstalador)
    print "El comando es: %s" % comando
    subprocess.Popen(comando,stdout=subprocess.PIPE, shell=True)
    time.sleep(1)
    print "Ejecutando %s" % desinstalador
    subprocess.call(desinstalador)
    reg=registar.Registradores()
    reg.eliminarRemotamente()




