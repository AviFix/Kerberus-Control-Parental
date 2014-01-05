# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore

import webbrowser

def main():
   app = QtGui.QApplication(sys.argv)

   trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon('kerby.ico'), app)
   menu = QtGui.QMenu('Kerberus Control Parental')
   trayIcon.setContextMenu(menu)
   filtradoHabilitado = True

   def deshabilitarFiltradoWindow():
        webbrowser.open(
                'http://inicio.kerberus.com.ar/!DeshabilitarFiltrado!',
                new=2
                )
        habilitarFiltradoAction.setVisible(True)
        deshabilitarFiltradoAction.setVisible(False)

   def habilitarFiltradoWindow():
        webbrowser.open(
                'http://inicio.kerberus.com.ar/!HabilitarFiltrado!',
                new=2
                )
        habilitarFiltradoAction.setVisible(False)
        deshabilitarFiltradoAction.setVisible(True)

   def cambiarPasswordWindow():
        webbrowser.open(
                'http://inicio.kerberus.com.ar/!CambiarPassword!',
                new=2
                )
   
   #SIGNAL->SLOT
   #accion deshabilitar filtrado
   deshabilitarFiltradoAction = menu.addAction(
                            'Deshabilitar Filtrado'
                            )
   #accion habilitar filtrado
   habilitarFiltradoAction = menu.addAction(
                            'Habilitar Filtrado'
                            )
   habilitarFiltradoAction.setVisible(False)
   #cambiar password
   cambiarPasswordAction = menu.addAction(
                'Cambiar password de administrador'
                )  
   exitAction = menu.addAction(
		  'Exit'
		)
   QtCore.QObject.connect(
           exitAction,
           QtCore.SIGNAL("triggered()"),
           lambda: sys.exit()
           )
   QtCore.QObject.connect(
           menu, QtCore.SIGNAL("clicked()"),
           lambda: menu.popup(QtGui.QCursor.pos())
           )

   QtCore.QObject.connect(
           deshabilitarFiltradoAction,
           QtCore.SIGNAL("triggered()"),
           deshabilitarFiltradoWindow
           )
   QtCore.QObject.connect(
           habilitarFiltradoAction,
           QtCore.SIGNAL("triggered()"),
           habilitarFiltradoWindow
           )
   QtCore.QObject.connect(
           cambiarPasswordAction,
           QtCore.SIGNAL("triggered()"),
           cambiarPasswordWindow
           )
   trayIcon.show()
   trayIcon.showMessage(u'Kerberus Control Parental',u'Navegación protegida por Kerberus',500)
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()


