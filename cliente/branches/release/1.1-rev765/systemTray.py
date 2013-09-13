# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import sys


sys.path.append('conf')
sys.path.append('clases')

import webbrowser
import config

class KerberusSystray(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        #cargar imagen para icono
	icono = config.PATH_COMMON + '/kerby.ico'
	print "Seteando icono en %s" % icono
        pixmap = QtGui.QPixmap(icono)
        #setear el nombre de la ventana
        #self.setWindowTitle('Kerberus Control Parental')
        #colocar el icono cargado a la ventana
        #self.setWindowIcon(QtGui.QIcon(pixmap))
        #creamos objeto Style para hacer uso de los iconos de Qt
        self.style = self.style()
        self.filtradoHabilitado = True

        #Menu
        self.menu = QtGui.QMenu('Kerberus')

        #accion deshabilitar filtrado
        self.deshabilitarFiltradoAction = self.menu.addAction(
                            self.style.standardIcon(QtGui.QStyle.SP_ArrowRight),
                            'Deshabilitar Filtrado'
                            )
        #accion habilitar filtrado
        self.habilitarFiltradoAction = self.menu.addAction(
                            self.style.standardIcon(QtGui.QStyle.SP_ArrowRight),
                            'Habilitar Filtrado'
                            )
        self.habilitarFiltradoAction.setVisible(False)
        #cambiar password
        self.cambiarPasswordAction = self.menu.addAction(
                self.style.standardIcon(QtGui.QStyle.SP_ArrowRight),
                'Cambiar password de administrador'
                )
        #accion salir
        self.exitAction = self.menu.addAction(
                self.style.standardIcon(QtGui.QStyle.SP_TitleBarCloseButton),
                'Salir')

        #SIGNAL->SLOT
        QtCore.QObject.connect(
                self.exitAction,
                QtCore.SIGNAL("triggered()"),
                lambda: sys.exit()
                )
        QtCore.QObject.connect(
                self.menu, QtCore.SIGNAL("clicked()"),
                lambda: self.menu.popup(QtGui.QCursor.pos())
                )
        QtCore.QObject.connect(
                self.deshabilitarFiltradoAction,
                QtCore.SIGNAL("triggered()"),
                self.deshabilitarFiltradoWindow
                )
        QtCore.QObject.connect(
                self.habilitarFiltradoAction,
                QtCore.SIGNAL("triggered()"),
                self.habilitarFiltradoWindow
                )
        QtCore.QObject.connect(
                self.cambiarPasswordAction,
                QtCore.SIGNAL("triggered()"),
                self.cambiarPasswordWindow
                )

        #SystemTray
        self.tray = QtGui.QSystemTrayIcon(QtGui.QIcon(pixmap), self)
        self.tray.setToolTip('KerberusSystray')
        self.tray.setVisible(True)
        self.tray.setContextMenu(self.menu)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def deshabilitarFiltradoWindow(self):
        webbrowser.open(
                'http://inicio.kerberus.com.ar/!DeshabilitarFiltrado!',
                new=2
                )
        self.habilitarFiltradoAction.setVisible(True)
        self.deshabilitarFiltradoAction.setVisible(False)

    def habilitarFiltradoWindow(self):
        webbrowser.open(
                'http://inicio.kerberus.com.ar/!HabilitarFiltrado!',
                new=2
                )
        self.habilitarFiltradoAction.setVisible(False)
        self.deshabilitarFiltradoAction.setVisible(True)

    def cambiarPasswordWindow(self):
        webbrowser.open(
                'http://inicio.kerberus.com.ar/!CambiarPassword!',
                new=2
                )

app = QtGui.QApplication(sys.argv)
pytest = KerberusSystray()
#pytest.show()

sys.exit(app.exec_())
