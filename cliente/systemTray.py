#!/usr/bin/python
# -*- coding: latin-1 -*-
import sys
from PyQt4 import QtGui, QtCore

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)
        menu.addSeparator()
        deshabilitar = menu.addAction("Deshabilitar Filtrado")
        exitAction = menu.addAction("Exit")
        self.setContextMenu(menu)
        QtCore.QObject.connect(deshabilitar, QtCore.SIGNAL('triggered()'), self.deshabilitar)

    def deshabilitar(self):
        self.showMessage("Kerberus","Protección kerberus deshabilitada",1,2000)

def main():
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("Bomb.xpm"), w)

    trayIcon.show()
    trayIcon.showMessage("Kerberus","Navegación protegida por kerberus",1,2000)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
