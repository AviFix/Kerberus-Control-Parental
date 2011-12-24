import sys
from PyQt4 import QtCore, QtGui
from formulario import Ui_Form
sys.path.append('../clases')
sys.path.append('../conf')
import administradorDeUsuarios

class formularioPassword(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # Conexiones
        QtCore.QObject.connect(self.ui.boton,QtCore.SIGNAL("clicked()"), self.acentarPassword)
        self.ui.label_passwordActual.setVisible(False)
        self.ui.password_actual.setVisible(False)
        self.center()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def acentarPassword(self):
        if (self.ui.password1.text() <> self.ui.password2.text() or (len(self.ui.password1.text()) < 1)):
            QtGui.QMessageBox.critical(self, 'Kerberus', 'Las password no coinciden, reescribalas.', QtGui.QMessageBox.Ok)
            self.ui.password1.clear()
            self.ui.password2.clear()
            self.ui.password1.setFocus()
        else:
            admUser=administradorDeUsuarios.AdministradorDeUsuarios()
            admUser.cambiarPassword('admin', 'perico', str(self.ui.password1.text()))
#            QtGui.QMessageBox.question(self, 'Kerberus', 'Password seteada correctamente.', QtGui.QMessageBox.Ok)
            self.close()


#if __name__ == "__main__":
#    app = QtGui.QApplication(sys.argv)
#    myapp = formularioPassword()
#    myapp.show()
#    sys.exit(app.exec_())
