from PyQt4 import QtGui
import sys

sys.path.append('../')
import pedirUsuario
import funciones

app = QtGui.QApplication(sys.argv)
myapp = pedirUsuario.formularioUsuario('Desinstalar Kerberus', 'Ingrese la password de administrador de Kerberus \n(la que ingreso al momento de instalarlo)')
myapp.show()
app.exec_()
desinstalar=myapp.verificado
if desinstalar:
    print "Desinstalando kerberus..."

