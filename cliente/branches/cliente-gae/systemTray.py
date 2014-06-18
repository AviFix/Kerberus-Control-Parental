# -*- coding: utf-8 -*-

# Modulos externos
from PyQt4.QtGui import QWidget, QPixmap, QIcon, QSystemTrayIcon, QMenu
from PyQt4.QtGui import QStyle, QApplication, QCursor
from PyQt4.QtCore import QObject, SIGNAL, pyqtSignal

import sys
import os.path
import threading
import time
import httplib

sys.path.append('adminpanel')
sys.path.append('password')
sys.path.append('clases')


# Modulos propios
import webbrowser
import adminPanel
import config


class KerberusSystray(QWidget):
    def __init__(self):
        self.chequeos_activos = True
        self.ultimo_estado_kerberus = True
        self.simpleSig = pyqtSignal()
        QWidget.__init__(self)
        icono = 'kerby-activo.ico'
        #pixmap = QPixmap(icono)
        self.style = self.style()
        ##setear el nombre de la ventana
        self.setWindowTitle('Kerberus Control Parental')
        #colocar el icono cargado a la ventana
        self.setWindowIcon(self.style.standardIcon(
            QStyle.SP_DialogYesButton))
        ##creamos objeto Style para hacer uso de los iconos de Qt

        self.filtradoHabilitado = True

        if not os.path.isfile('dontShowMessage'):
            self.mostrarMensaje = True
            self.noMostrarMasMensaje()
        else:
            self.mostrarMensaje = False

        #Menu
        self.menu = QMenu('Kerberus')

        #accion configurar Dominios
        self.configurarDominiosAction = self.menu.addAction(
                            'Permitir/Denegar dominios'
                            )
        #accion deshabilitar filtrado
        self.deshabilitarFiltradoAction = self.menu.addAction(
                            'Deshabilitar Filtrado'
                            )
        #accion habilitar filtrado
        self.habilitarFiltradoAction = self.menu.addAction(
                            'Habilitar Filtrado'
                            )
        self.habilitarFiltradoAction.setVisible(False)
        #cambiar password
        self.cambiarPasswordAction = self.menu.addAction(
                'Cambiar password de administrador'
                )
        #accion salir
        self.exitAction = self.menu.addAction(
                'Salir')

        #SIGNAL->SLOT
        QObject.connect(
                self.exitAction,
                SIGNAL("triggered()"),
                #lambda: sys.exit()
                self.salir
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
        QObject.connect(
                self.configurarDominiosAction,
                SIGNAL("triggered()"),
                self.configurarDominios
                )

        #SystemTray
        #self.tray = QSystemTrayIcon(QIcon(pixmap), self)
        self.tray = QSystemTrayIcon(self.style.standardIcon(
            QStyle.SP_DialogYesButton), self
            )
        self.tray.setToolTip('Kerberus Control Parental - Activado')
        self.tray.setContextMenu(self.menu)
        self.tray.setVisible(True)

        QObject.connect(
                self.tray,
                SIGNAL("messageClicked()"),
                self.noMostrarMasMensaje
                )

        #self.simpleSig.connect(self.setIconStatus)
        QObject.connect(
                self,
                SIGNAL("triggered()"),
                self.setIconStatus
                )

        if self.mostrarMensaje:
            self.tray.showMessage(
                    u'Kerberus Control Parental',
                    u'Filtro de Protección para menores de edad Activado',
                    2000
                    )

        # Lanzo el thead que verifica si esta activo o no kerberus
        self.t = threading.Thread(target=self.chequeosPeriodicos)
        self.t.start()


    def chequeosPeriodicos(self):
        while self.chequeos_activos:
            time.sleep(3)
            status = self.checkKerberusStatus()
            if status != self.ultimo_estado_kerberus:
                print "Cambio el status:", status
                self.ultimo_estado_kerberus = status
                self.simpleSig.emit()
            print status

    def setIconStatus(self):
        print "se lanzo"
        if self.ultimo_estado_kerberus:
            self.habilitarFiltradoAction.setVisible(False)
            self.deshabilitarFiltradoAction.setVisible(True)
            self.tray.setIcon(self.style.standardIcon(
                QStyle.SP_DialogYesButton))
            self.tray.setToolTip('Kerberus Control Parental - Activado')
        else:
            self.habilitarFiltradoAction.setVisible(True)
            self.deshabilitarFiltradoAction.setVisible(False)
            self.tray.setIcon(self.style.standardIcon(
                QStyle.SP_DialogYesButton))
            self.tray.setToolTip('Kerberus Control Parental')

    def salir(self):
        self.chequeos_activos = False
        sys.exit()

    def configurarDominios(self):
        admin = adminPanel.adminPanel()
        admin.show()

    def noMostrarMasMensaje(self):
        try:
            open('dontShowMessage', 'a').close()
        except IOError:
            print 'No se pudo crear el archivo dontShowMessage'

    def deshabilitarFiltradoWindow(self):
        url = 'http://%s:%s/!DeshabilitarFiltrado!' % ('inicio.kerberus.com.ar','80')
        webbrowser.open(
                url,
                new=2
                )

    def checkKerberusStatus(self):
        try:
            url = 'http://%s:%s/' % (config.BIND_ADDRESS, config.BIND_PORT)
            con = httplib.HTTPConnection(config.BIND_ADDRESS, config.BIND_PORT)
            respuesta = con.request(method='KERBERUSESTADO', url=url)
            print respuesta
            return respuesta == 'Activo'
        except:
            print "error: ", url
            return False

    def habilitarFiltradoWindow(self):
        url = "http://%s:%s/!HabilitarFiltrado!" % ('inicio.kerberus.com.ar','80')
        webbrowser.open(
                url,
                new=2
                )

    def cambiarPasswordWindow(self):
        url = "http:/%s:%s/!CambiarPassword!" % ('inicio.kerberus.com.ar','80')
        webbrowser.open(
                url,
                new=2
                )

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
kerberusTray = KerberusSystray()
sys.exit(app.exec_())
