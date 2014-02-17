import sys

from PyQt4.QtGui import QSystemTrayIcon
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QThread
from PyQt4.QtCore import SIGNAL

import recursos

class TrayIconUpdates(QSystemTrayIcon):

    def __init__(self, parent):
        QSystemTrayIcon.__init__(self, parent)
        icon = QIcon(recursos.IMAGES['icon'])
        self.setIcon(icon)
        self.setup_menu()

    def setup_menu(self, show_downloads=False):
        self.menu = QMenu()

        #accion deshabilitar filtrado
        self.deshabilitarFiltradoAction = self.menu.addAction(
                            #self.style.standardIcon(QStyle.SP_DialogNoButton),
                            'Deshabilitar Filtrado'
                            )
        #accion habilitar filtrado
        self.habilitarFiltradoAction = self.menu.addAction(
                            #self.style.standardIcon(QStyle.SP_DialogYesButton),
                            'Habilitar Filtrado'
                            )
        self.habilitarFiltradoAction.setVisible(False)
        #cambiar password
        self.cambiarPasswordAction = self.menu.addAction(
                #self.style.standardIcon(QStyle.SP_BrowserReload),
                'Cambiar password de administrador'
                )
        #accion salir
        self.exitAction = self.menu.addAction(
                #self.style.standardIcon(QStyle.SP_TitleBarCloseButton),
                'Salir')
        self.setContextMenu(self.menu)

app = QApplication(sys.argv)
pytest = TrayIconUpdates(app)
pytest.show()
sys.exit(app.exec_())