# -*- coding: utf-8 -*-

# Modulos externos
from PyQt4.QtGui import QWidget, QPixmap, QIcon, QSystemTrayIcon, QMenu
from PyQt4.QtGui import QStyle, QApplication, QCursor
from PyQt4.QtCore import QObject, SIGNAL
import sys
import os.path

# Modulos propios
import webbrowser


class KerberusSystray(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        icono = 'kerby-activo.ico'
        pixmap = QPixmap(icono)
        ##setear el nombre de la ventana
        self.setWindowTitle('Kerberus Control Parental')
        #colocar el icono cargado a la ventana
        self.setWindowIcon(QIcon(pixmap))
        ##creamos objeto Style para hacer uso de los iconos de Qt
        self.style = self.style()
        self.filtradoHabilitado = True

        if not os.path.isfile('dontShowMessage'):
            self.mostrarMensaje = True
            self.noMostrarMasMensaje()
        else:
            self.mostrarMensaje = False

        #Menu
        self.menu = QMenu('Kerberus')

        #accion deshabilitar filtrado
        self.deshabilitarFiltradoAction = self.menu.addAction(
                            self.style.standardIcon(QStyle.SP_DialogNoButton),
                            'Deshabilitar Filtrado'
                            )
        #accion habilitar filtrado
        self.habilitarFiltradoAction = self.menu.addAction(
                            self.style.standardIcon(QStyle.SP_DialogYesButton),
                            'Habilitar Filtrado'
                            )
        self.habilitarFiltradoAction.setVisible(False)
        #cambiar password
        self.cambiarPasswordAction = self.menu.addAction(
                self.style.standardIcon(QStyle.SP_BrowserReload),
                'Cambiar password de administrador'
                )
        #accion salir
        self.exitAction = self.menu.addAction(
                self.style.standardIcon(QStyle.SP_TitleBarCloseButton),
                'Salir')

        #SIGNAL->SLOT
        QObject.connect(
                self.exitAction,
                SIGNAL("triggered()"),
                lambda: sys.exit()
                )
        QObject.connect(
                self.menu, SIGNAL("clicked()"),
                lambda: self.menu.popup(QCursor.pos())
                )
        QObject.connect(
                self.deshabilitarFiltradoAction,
                SIGNAL("triggered()"),
                self.deshabilitarFiltradoWindow
                )
        QObject.connect(
                self.habilitarFiltradoAction,
                SIGNAL("triggered()"),
                self.habilitarFiltradoWindow
                )
        QObject.connect(
                self.cambiarPasswordAction,
                SIGNAL("triggered()"),
                self.cambiarPasswordWindow
                )

        #SystemTray
        self.tray = QSystemTrayIcon(QIcon(pixmap), self)
        #self.tray = QtGui.QSystemTrayIcon(self.style.standardIcon(
            #QtGui.QStyle.SP_DialogYesButton), self
            #)
        self.tray.setToolTip('Kerberus Control Parental - Activado')
        self.tray.setContextMenu(self.menu)
        self.tray.setVisible(True)

        QObject.connect(
                self.tray,
                SIGNAL("messageClicked()"),
                self.noMostrarMasMensaje
                )

        if self.mostrarMensaje:
            self.tray.showMessage(
                    u'Kerberus Control Parental',
                    u'Filtro de Protección para menores de edad Activado',
                    2000
                    )

    def noMostrarMasMensaje(self):
        try:
            open('dontShowMessage', 'a').close()
        except IOError:
            print 'No se pudo crear el archivo dontShowMessage'

    def deshabilitarFiltradoWindow(self):
        webbrowser.open(
                'http://inicio.kerberus.com.ar/!DeshabilitarFiltrado!',
                new=2
                )
        self.habilitarFiltradoAction.setVisible(True)
        self.deshabilitarFiltradoAction.setVisible(False)
        self.tray.setIcon(QIcon('kerby-inactivo.ico'))
        self.tray.setToolTip('Kerberus Control Parental')

    def habilitarFiltradoWindow(self):
        webbrowser.open(
                'http://inicio.kerberus.com.ar/!HabilitarFiltrado!',
                new=2
                )
        self.habilitarFiltradoAction.setVisible(False)
        self.deshabilitarFiltradoAction.setVisible(True)
        self.tray.setIcon(QIcon('kerby-activo.ico'))
        self.tray.setToolTip('Kerberus Control Parental - Activado')

    def cambiarPasswordWindow(self):
        webbrowser.open(
                'http://inicio.kerberus.com.ar/!CambiarPassword!',
                new=2
                )

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
pytest = KerberusSystray()
sys.exit(app.exec_())
