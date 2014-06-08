#!/usr/bin/python
# -*- coding: utf-8 -*-
# Modulos externos
import sys
import re
import httplib
from PyQt4 import QtGui, QtSql, QtCore

# Modulos propios
sys.path.append('conf')
sys.path.append('adminpanel')

from AdminPanelUI import Ui_MainWindow
import config

class adminPanel:
    def __init__(self, parent=None):
        self.MainWindow = QtGui.QMainWindow()
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

    def salir(self):
        self.db.close()
        self.MainWindow.close()

    def guardar(self):
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
        con = httplib.HTTPConnection(config.BIND_ADDRESS,config.BIND_PORT)
        respuesta = con.request(method='KERBERUSREFRESH', url=url)

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

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    #if not createConnection():
        #sys.exit(1)

    admin = adminPanel()
    sys.exit(app.exec_())