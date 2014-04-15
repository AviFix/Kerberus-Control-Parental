# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import sys

class KerberusSystray(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        
	#Menu
        self.menu = QtGui.QMenu('Kerberus')
        self.style = self.style()
        
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

        #SystemTray
	icono = 'kerby.ico'
        pixmap = QtGui.QPixmap(icono)
        self.tray = QtGui.QSystemTrayIcon(QtGui.QIcon(pixmap), self)
        self.tray.setToolTip('KerberusSystray')
        self.tray.setVisible(True)
        self.tray.setContextMenu(self.menu)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

app = QtGui.QApplication(sys.argv)
pytest = KerberusSystray()
sys.exit(app.exec_())
