#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui
from formUsuario import Ui_Form
sys.path.append('../clases')
sys.path.append('../conf')
import administradorDeUsuarios

class formularioUsuario(QtGui.QMainWindow):
    def __init__(self, titulo='',descripcion='', parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.Descripcion.setText(descripcion)
        self.ui.titulo.setText(titulo)
        self.center()
        self.ui.password.setFocus()
        # Conexiones
        QtCore.QObject.connect(self.ui.boton,QtCore.SIGNAL("clicked()"), self.checkPassword)
        QtCore.QObject.connect(self.ui.botoncancelar,QtCore.SIGNAL("clicked()"), self.cancelar)
        self.verificado=False

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def checkPassword(self):
        admUser=administradorDeUsuarios.AdministradorDeUsuarios()
        password=unicode(self.ui.password.text().toUtf8(), 'utf-8')
        valido=admUser.usuario_valido('admin', password)
        if valido:
            self.verificado=True
            self.close()
        else:
            QtGui.QMessageBox.critical(self, 'Kerberus', u'Wrong password!.', QtGui.QMessageBox.Ok)
            self.ui.password.clear()
            self.ui.password.setFocus()
        return True

    def cancelar(self):
        self.verificado=False
        self.close()
        return True





