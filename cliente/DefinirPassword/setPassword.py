import sys
from PyQt4 import QtCore, QtGui
from formulario import Ui_Form

class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # Conexiones
        QtCore.QObject.connect(self.ui.boton,QtCore.SIGNAL("clicked()"), self.acentarPassword)
    def acentarPassword(self):
		if (self.ui.password1.text() <> self.ui.password2.text() or (len(self.ui.password1.text()) < 1)):
			QtGui.QMessageBox.critical(self, 'No coinciden', 'Las password no coinciden, reescribalas.', QtGui.QMessageBox.Ok)
			self.ui.password1.clear()
			self.ui.password2.clear()
			self.ui.password1.setFocus()
		else:
			QtGui.QMessageBox.question(self, 'No coinciden', 'Password seteada correcamente', QtGui.QMessageBox.Ok)
			sys.exit(app.exec_())
				
		
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())
