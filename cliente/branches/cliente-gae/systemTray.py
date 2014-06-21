# -*- coding: utf-8 -*-

# Modulos externos
#from PyQt4.QtGui import QWidget, QPixmap, QIcon, QSystemTrayIcon, QMenu
from PyQt4.QtGui import QWidget, QSystemTrayIcon, QMenu, QDialog, QPushButton
from PyQt4.QtGui import QStyle, QApplication, QCursor, QLabel, QLineEdit
from PyQt4.QtGui import QVBoxLayout, QMessageBox, QMainWindow
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4 import QtSql
import sys
import os.path
import threading
import time
import httplib
import re
import webbrowser

sys.path.append('adminpanel')
sys.path.append('clases')
sys.path.append('conf')

# Modulos propios
import administradorDeUsuarios
from AdminPanelUI import Ui_MainWindow
import config
import loguear

modulo_logger = loguear.logSetup(
    config.SYSTRAY_LOGFILE,
    config.LOGLEVEL, config.LOG_SIZE_MB,
    config.LOG_CANT_ROTACIONES, 'kerberus'
    )


class Login(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.texto = QLabel(self)
        self.texto.setText('Ingrese la password del administrador de Kerberus')
        self.textPass = QLineEdit(self)
        self.textPass.setEchoMode(2)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QVBoxLayout(self)
        layout.addWidget(self.texto)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        admUser = administradorDeUsuarios.AdministradorDeUsuarios()
        password = unicode(self.textPass.text().toUtf8(), 'utf-8')
        valido = admUser.usuario_valido('admin', password)
        if valido:
            self.accept()
        else:
            QMessageBox.warning(
                self, 'Error', u'Password incorrecta')


class adminPanel:
    def __init__(self, parent=None):
        self.MainWindow = QMainWindow()
        if Login().exec_() == QDialog.Accepted:
            self.panel()

    def panel(self):
        modulo_logger.debug('Creando panel de admin...')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.labelErrorPermitidos.setVisible(False)
        self.ui.labelErrorDenegados.setVisible(False)
        self.ui.botonCancelar.clicked.connect(self.salir)
        self.ui.pushButtonPermitir.clicked.connect(self.agregarPermitido)
        self.ui.pushButtonDenegar.clicked.connect(self.agregarDenegado)
        self.ui.botonEliminarPermitido.clicked.connect(self.eliminarPermitido)
        self.ui.botonEliminarDenegado.clicked.connect(self.eliminarDenegado)
        self.ui.botonGuardar.clicked.connect(self.refrezcarDominios)
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(config.PATH_COMMON + '/kerberus.db')
        self.db.open()
        # Listo los dominios denegados
        self.modelPermitidos = QtSql.QSqlTableModel(None, self.db)
        self.modelPermitidos.setTable("dominios_usuario")
        # requiere de un submit para que se apliquen los cambios
        self.modelPermitidos.setEditStrategy(2)
        self.modelPermitidos.setFilter('estado=1')
        self.modelPermitidos.select()
        self.modelPermitidos.setHeaderData(0, 1, "Dominios permitidos")
        self.ui.tableViewPermitidos.setModel(self.modelPermitidos)
        self.ui.tableViewPermitidos.hideColumn(1)
        self.ui.tableViewPermitidos.hideColumn(2)
        self.ui.tableViewPermitidos.resizeRowsToContents()
        self.ui.tableViewPermitidos.show()
        # Listo los dominios denegados
        self.modelDenegados = QtSql.QSqlTableModel(None, self.db)
        self.modelDenegados.setTable("dominios_usuario")
        # requiere de un submit para que se apliquen los cambios
        self.modelDenegados.setEditStrategy(2)
        self.modelDenegados.setFilter('estado=2')
        self.modelDenegados.select()
        self.modelDenegados.setHeaderData(0, 1, "Dominios permitidos")
        self.ui.tableViewDenegados.setModel(self.modelDenegados)
        self.ui.tableViewDenegados.hideColumn(1)
        self.ui.tableViewDenegados.hideColumn(2)
        self.ui.tableViewDenegados.resizeRowsToContents()
        self.ui.tableViewDenegados.show()
        self.MainWindow.show()
        modulo_logger.debug('Fin de la creacion del panel de admin...')

    def salir(self):
        self.db.close()
        self.MainWindow.close()

    def guardar(self):
        modulo_logger.debug('Guardando dominios')
        self.modelPermitidos.submitAll()
        self.modelDenegados.submitAll()

    def verificarDominio(self, dominio):
        domvalido = re.match(
            '^(?:[a-zA-Z0-9]+(?:\-*[a-zA-Z0-9])*\.)+[a-zA-Z]{2,6}$', dominio
            )
        return domvalido

    def eliminarPermitido(self):
        rows = self.ui.tableViewPermitidos.selectedIndexes()
        for row in rows:
            self.ui.tableViewPermitidos.model().removeRow(row.row())
        self.modelPermitidos.submitAll()

    def eliminarDenegado(self):
        rows = self.ui.tableViewDenegados.selectedIndexes()
        for row in rows:
            self.ui.tableViewDenegados.model().removeRow(row.row())
        self.modelDenegados.submitAll()

    def refrezcarDominios(self):
        url = 'http://%s:%s/!RecargarDominiosKerberus!' % (config.BIND_ADDRESS,
                                                           config.BIND_PORT)
        con = httplib.HTTPConnection(config.BIND_ADDRESS, config.BIND_PORT)
        con.request(method='KERBERUSREFRESH', url=url)

    def agregarPermitido(self):
        self.ui.labelErrorPermitidos.setVisible(False)
        dominio = self.ui.lineEditPermitidos.text()
        valido = self.verificarDominio(dominio)
        if valido:
            consulta = QtSql.QSqlQuery()
            consulta.prepare("Insert into dominios_usuario (url,usuario,estado)"
                                "values (:url, :usuario, :estado)")
            consulta.bindValue(":url", dominio)
            consulta.bindValue(":usuario", 2)
            consulta.bindValue(":estado", 1)
            consulta.exec_()
            self.modelPermitidos.submitAll()
        else:
            self.ui.labelErrorPermitidos.setVisible(True)

    def agregarDenegado(self):
        self.ui.labelErrorDenegados.setVisible(False)
        dominio = self.ui.lineEditDenegados.text()
        valido = self.verificarDominio(dominio)
        if valido:
            consulta = QtSql.QSqlQuery()
            consulta.prepare("Insert into dominios_usuario (url,usuario,estado)"
                                "values (:url, :usuario, :estado)")
            consulta.bindValue(":url", dominio)
            consulta.bindValue(":usuario", 2)
            consulta.bindValue(":estado", 2)
            consulta.exec_()
            self.modelDenegados.submitAll()
        else:
            self.ui.labelErrorDenegados.setVisible(True)


class KerberusSystray(QWidget):
    def __init__(self):
        self.chequeos_activos = True
        self.ultimo_estado_kerberus = True
        QWidget.__init__(self)
        #icono = 'kerby-activo.ico'
        #pixmap = QPixmap(icono)
        self.style = self.style()
        ##setear el nombre de la ventana
        self.setWindowTitle('Kerberus Control Parental')
        #colocar el icono cargado a la ventana
        self.setWindowIcon(self.style.standardIcon(
            QStyle.SP_DialogYesButton))

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
        # esta conexion es utilizada para refrezcar el icono en caso de
        # que se desactive/active kerberus
        QObject.connect(
                self,
                SIGNAL("update()"),
                #lambda: sys.exit()
                self.setIconStatus
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
            QStyle.SP_DialogYesButton), self)
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

        # Lanzo el thead que verifica si esta activo o no kerberus
        self.t = threading.Thread(target=self.chequeosPeriodicos)
        self.t.start()

    def chequeosPeriodicos(self):
        while self.chequeos_activos:
            time.sleep(3)
            status = self.checkKerberusStatus()
            if status != self.ultimo_estado_kerberus:
                self.ultimo_estado_kerberus = status
                self.emit(SIGNAL('update()'))

    def setIconStatus(self):
        if self.ultimo_estado_kerberus:
            self.habilitarFiltradoAction.setVisible(False)
            self.deshabilitarFiltradoAction.setVisible(True)
            self.tray.setIcon(self.style.standardIcon(
                QStyle.SP_DialogYesButton))
            self.tray.setToolTip('Kerberus Control Parental - Activado')
            self.tray.showMessage(
                    u'Kerberus Control Parental',
                    u'Filtro de Protección para menores de edad Activado',
                    2000
                    )
        else:
            self.habilitarFiltradoAction.setVisible(True)
            self.deshabilitarFiltradoAction.setVisible(False)
            self.tray.setIcon(self.style.standardIcon(
                QStyle.SP_DialogNoButton))
            self.tray.setToolTip('Kerberus Control Parental - Inactivo')
            self.tray.showMessage(
                    u'Kerberus Control Parental',
                    u'Filtro de Protección para menores de edad Desactivado',
                    2000
                    )

    def salir(self):
        self.chequeos_activos = False
        sys.exit()

    def configurarDominios(self):
        admin = adminPanel()
        admin.show()

    def noMostrarMasMensaje(self):
        try:
            open('dontShowMessage', 'a').close()
        except IOError:
            print 'No se pudo crear el archivo dontShowMessage'

    def deshabilitarFiltradoWindow(self):
        url = 'http://%s:%s/!DeshabilitarFiltrado!' % ('inicio.kerberus.com.ar',
                                                        '80')
        webbrowser.open(
                url,
                new=2
                )

    def checkKerberusStatus(self):
        try:
            url = 'http://%s:%s/' % (config.BIND_ADDRESS, config.BIND_PORT)
            con = httplib.HTTPConnection(config.BIND_ADDRESS, config.BIND_PORT)
            con.request(method='KERBERUSESTADO', url=url)
            respuesta = con.getresponse().read()
            return respuesta == 'Activo'
        except:
            return False

    def habilitarFiltradoWindow(self):
        url = "http://%s:%s/!HabilitarFiltrado!" % ('inicio.kerberus.com.ar',
                                                    '80')
        webbrowser.open(
                url,
                new=2
                )

    def cambiarPasswordWindow(self):
        url = "http:/%s:%s/!CambiarPassword!" % ('inicio.kerberus.com.ar',
                                                 '80')
        webbrowser.open(
                url,
                new=2
                )

modulo_logger.info('Iniciando SystemTray...')
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
kerberusTray = KerberusSystray()
modulo_logger.info('Se lanzo el SystemTray')
sys.exit(app.exec_())
modulo_logger.info('Se cerro el SystemTray...')

