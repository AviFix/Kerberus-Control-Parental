import sys, os
from PyQt4 import QtCore, QtGui

sys.path.append('../clases')
sys.path.append('../conf')
sys.path.append('../')

import administradorDeUsuarios
import config
from cambiarPasswordForm import Ui_Form


class formularioPassword(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.temp_file="%s/kerberus.lock" % config.PATH_COMMON
        self.lock()
        # Conexiones
        QtCore.QObject.connect(self.ui.boton,QtCore.SIGNAL("clicked()"), self.acentarPassword)
        self.center()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def acentarPassword(self):
        admUser=administradorDeUsuarios.AdministradorDeUsuarios()
        pass_actual=str(self.ui.password_actual.text())
        pass_valida=admUser.usuario_valido('admin', pass_actual)
        if pass_valida:
            if (self.ui.password1.text() <> self.ui.password2.text() or (len(self.ui.password1.text()) < 1)):
                QtGui.QMessageBox.critical(self, 'Kerberus', 'Las passwords no coinciden, reescribalas.', QtGui.QMessageBox.Ok)
                self.ui.password1.clear()
                self.ui.password2.clear()
                self.ui.password1.setFocus()
            else:
                admUser.cambiarPassword('admin', pass_actual, str(self.ui.password1.text()))
                self.unlock()
                self.close()
        else:
                QtGui.QMessageBox.critical(self, 'Kerberus', 'Las antigua password es incorrecta.', QtGui.QMessageBox.Ok)
                self.ui.password_actual.clear()
                self.ui.password_actual.setFocus()


    def lock(self):
        if config.PLATAFORMA == 'Linux':
            os.open(self.temp_file,os.O_RDWR|os.O_CREAT)

    def unlock(self):
        if config.PLATAFORMA == 'Linux':
            os.remove(self.temp_file)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = formularioPassword()
    myapp.show()
    sys.exit(app.exec_())
