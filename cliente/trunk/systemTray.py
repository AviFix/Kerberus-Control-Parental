#!/usr/bin/python
# -*- coding: latin-1 -*-
import sys
from PyQt4 import QtGui, QtCore

import cliente

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent,demonio):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.parent=parent
        self.demonio=demonio
        self.showMessage("Kerberus","Protección kerberus habilitada",1,2000)
        menu = QtGui.QMenu(self.parent)
        deshabilitar = menu.addAction("Deshabilitar Filtrado")
        QtCore.QObject.connect(deshabilitar, QtCore.SIGNAL('triggered()'), self.deshabilitar)
        self.setContextMenu(menu)
        self.demonio.habilitarFiltrado()

        self.demonio.iniciar()


    def deshabilitar(self):
        self.showMessage("Kerberus","Protección kerberus deshabilitada",1,2000)
        menu = QtGui.QMenu(self.parent)
        habilitar = menu.addAction("Habilitar Filtrado")
        QtCore.QObject.connect(habilitar, QtCore.SIGNAL('triggered()'), self.habilitar)
        self.setContextMenu(menu)
        self.demonio.deshabilitarFiltrado()

    def habilitar(self):
        self.showMessage("Kerberus","Protección kerberus habilitada",1,2000)
        menu = QtGui.QMenu(self.parent)
        deshabilitar = menu.addAction("Deshabilitar Filtrado")
        QtCore.QObject.connect(deshabilitar, QtCore.SIGNAL('triggered()'), self.deshabilitar)
        self.setContextMenu(menu)
        self.demonio.habilitarFiltrado()

    def salir(self):
        self.exit()

def main():
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    cliente2=cliente.client()
    trayIcon = SystemTrayIcon(QtGui.QIcon("Bomb.xpm"), w,cliente2)
    trayIcon.show()
    app.exec_()
    cliente2.iniciar()
#
if __name__ == '__main__':
    main()
