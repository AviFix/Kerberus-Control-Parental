# -*- coding: utf-8 -*-
import sys
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

        #Menu
        self.menu = QtGui.QMenu('Kerberus')
        #accion deshabilitar filtrado
        deshabilitarFiltrado = self.menu.addAction(self.style.standardIcon(QtGui.QStyle.SP_ArrowRight), 'Deshabilitar Filtrado')
        #accion salir
        exit = self.menu.addAction(self.style.standardIcon(QtGui.QStyle.SP_TitleBarCloseButton), 'Salir')

        #SIGNAL->SLOT
        QtCore.QObject.connect(exit, QtCore.SIGNAL("triggered()"), lambda: sys.exit())
        QtCore.QObject.connect(self.menu, QtCore.SIGNAL("clicked()"), lambda: self.menu.popup(QtGui.QCursor.pos()))
        QtCore.QObject.connect(deshabilitarFiltrado, QtCore.SIGNAL("triggered()"), self.deshabilitarFiltradoWindow)

        #SystemTray
        self.tray = QtGui.QSystemTrayIcon(QtGui.QIcon(pixmap), self)
        self.tray.setToolTip('KerberusSystray')
        self.tray.setVisible(True)
        self.tray.setContextMenu(self.menu)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def deshabilitarFiltradoWindow(self):
        self.tray.showMessage("Kerberus","Proteccion kerberus deshabilitada",1,3000)
        self.setVisible(True)




app = QtGui.QApplication(sys.argv)
pytest = KerberusSystray()
#pytest.show()

sys.exit(app.exec_())
