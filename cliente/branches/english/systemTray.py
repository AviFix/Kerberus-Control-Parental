# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import sys
import os.path

#sys.path.append('conf')
#sys.path.append('clases')

import webbrowser
#import imagenes_qr

class KerberusSystray(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        #icono = ':/imagenes/kerby.ico'
        #pixmap = QtGui.QPixmap(icono)
        ##setear el nombre de la ventana
        #self.setWindowTitle('Kerberus Control Parental')
        #colocar el icono cargado a la ventana
        #self.setWindowIcon(QtGui.QIcon(pixmap))
        ##creamos objeto Style para hacer uso de los iconos de Qt
        self.style = self.style()
        self.filtradoHabilitado = True

        if not os.path.isfile('dontShowMessage'):
            self.mostrarMensaje = True
            self.noMostrarMasMensaje()
        else:
            self.mostrarMensaje = False

        #Menu
        self.menu = QtGui.QMenu('Kerberus')

        #accion deshabilitar filtrado
        self.deshabilitarFiltradoAction = self.menu.addAction(
                            self.style.standardIcon(QtGui.QStyle.SP_DialogNoButton),
                            'Disable Kerberus'
                            )
        #accion habilitar filtrado
        self.habilitarFiltradoAction = self.menu.addAction(
                            self.style.standardIcon(QtGui.QStyle.SP_DialogYesButton),
                            'Enable Kerberus'
                            )
        self.habilitarFiltradoAction.setVisible(False)
        #cambiar password
        self.cambiarPasswordAction = self.menu.addAction(
                self.style.standardIcon(QtGui.QStyle.SP_BrowserReload),
                'Change administrator\'s password'
                )
        #accion salir
        #self.exitAction = self.menu.addAction(
                #self.style.standardIcon(QtGui.QStyle.SP_TitleBarCloseButton),
                #'Salir')

        #SIGNAL->SLOT
        #QtCore.QObject.connect(
                #self.exitAction,
                #QtCore.SIGNAL("triggered()"),
                #lambda: sys.exit()
                #)
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
        #self.tray = QtGui.QSystemTrayIcon(QtGui.QIcon(pixmap), self)
        self.tray = QtGui.QSystemTrayIcon(self.style.standardIcon(QtGui.QStyle.SP_DialogYesButton), self)
        self.tray.setToolTip('Kerberus Control Parental - Enabled')
        self.tray.setVisible(True)
        self.tray.setContextMenu(self.menu)

        QtCore.QObject.connect(
                self.tray,
                QtCore.SIGNAL("messageClicked()"),
                self.noMostrarMasMensaje
                )

        if self.mostrarMensaje:
            self.tray.showMessage(
                    u'Kerberus Control Parental',
                    u'Kerberus Control Parental Enabled!',
                    2000
                    )

    #def closeEvent(self, event):
        #event.ignore()
        #self.hide()

    def noMostrarMasMensaje(self):
        try:
            open('dontShowMessage','a').close()
        except IOError:
            print 'No se pudo crear el archivo dontShowMessage'

    def deshabilitarFiltradoWindow(self):
        webbrowser.open(
                'http://inicio.kerberus.com.ar/en/!DisableKerberus!',
                new=2
                )
        self.habilitarFiltradoAction.setVisible(True)
        self.deshabilitarFiltradoAction.setVisible(False)
        self.tray.setIcon(self.style.standardIcon(QtGui.QStyle.SP_DialogNoButton))
        self.tray.setToolTip('Kerberus Control Parental')

    def habilitarFiltradoWindow(self):
        webbrowser.open(
                'http://inicio.kerberus.com.ar/en/!EnableKerberus!',
                new=2
                )
        self.habilitarFiltradoAction.setVisible(False)
        self.deshabilitarFiltradoAction.setVisible(True)
        self.tray.setIcon(self.style.standardIcon(QtGui.QStyle.SP_DialogYesButton))
        self.tray.setToolTip('Kerberus Control Parental - Activado')

    def cambiarPasswordWindow(self):
        webbrowser.open(
                'http://inicio.kerberus.com.ar/en/!ChangePassword!',
                new=2
                )

app = QtGui.QApplication(sys.argv)
pytest = KerberusSystray()
sys.exit(app.exec_())
