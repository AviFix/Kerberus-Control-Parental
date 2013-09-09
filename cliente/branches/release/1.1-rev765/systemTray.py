# -*- coding: utf-8 -*-
import sys
import cambiarPassword
import pedirUsuario

from PyQt4 import QtGui, QtCore

class KerberusSystray(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        #cargar imagen para icono
        pixmap = QtGui.QPixmap('kerby.ico')
        #setear el nombre de la ventana
        self.setWindowTitle('Kerberus Control Parental')
        #colocar el icono cargado a la ventana
        self.setWindowIcon(QtGui.QIcon(pixmap))
        #creamos objeto Style para hacer uso de los iconos de Qt
        self.style = self.style()

        #Formulario de cambio de password
        self.cambiarPassForm = cambiarPassword.formularioPassword()

        #Formulario de pedido de password
        self.pedirUsuarioForm = pedirUsuario.formularioUsuario()

        #Menu
        self.menu = QtGui.QMenu('Kerberus')

        #accion deshabilitar filtrado
        deshabilitarFiltradoAction = self.menu.addAction(self.style.standardIcon(QtGui.QStyle.SP_ArrowRight), 'Deshabilitar Filtrado')

        #cambiar password
        cambiarPasswordAction = self.menu.addAction(
                self.style.standardIcon(QtGui.QStyle.SP_ArrowRight),
                'Cambiar password de administrador'
                )

        #recordar password
        recordarPasswordAction = self.menu.addAction(
                self.style.standardIcon(QtGui.QStyle.SP_ArrowRight),
                'Recordar password de administrador'
                )

        #accion salir
        exitAction = self.menu.addAction(self.style.standardIcon(QtGui.QStyle.SP_TitleBarCloseButton), 'Salir')

        #SIGNAL->SLOT
        QtCore.QObject.connect(exitAction, QtCore.SIGNAL("triggered()"), lambda: sys.exit())
        QtCore.QObject.connect(self.menu, QtCore.SIGNAL("clicked()"), lambda: self.menu.popup(QtGui.QCursor.pos()))
        QtCore.QObject.connect(deshabilitarFiltradoAction, QtCore.SIGNAL("triggered()"), self.deshabilitarFiltradoWindow)
        QtCore.QObject.connect(cambiarPasswordAction, QtCore.SIGNAL("triggered()"), self.cambiarPasswordWindow)
        QtCore.QObject.connect(recordarPasswordAction, QtCore.SIGNAL("triggered()"), self.recordarPasswordWindow)

        #SystemTray
        self.tray = QtGui.QSystemTrayIcon(QtGui.QIcon(pixmap), self)
        self.tray.setToolTip('KerberusSystray')
        self.tray.setVisible(True)
        self.tray.setContextMenu(self.menu)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def deshabilitarFiltradoWindow(self):
        self.tray.showMessage(u'Kerberus',u'Protección kerberus deshabilitada',1,3000)
        self.pedirUsuarioForm.setVisible(True)

    def cambiarPasswordWindow(self):
        self.cambiarPassForm.setVisible(True)
        self.tray.showMessage(u'Kerberus',u'Cambio de password',1,3000)

    def recordarPasswordWindow(self):
        self.tray.showMessage(u'Kerberus',u'Le hemos enviado un e-mail a su cuenta de correo con la contraseña de Kerberus',1,3000)


app = QtGui.QApplication(sys.argv)
pytest = KerberusSystray()
#pytest.show()

sys.exit(app.exec_())
