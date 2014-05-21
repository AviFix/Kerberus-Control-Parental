#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtSql
from AdminPanelUI import Ui_MainWindow

def createConnection():
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('kerberus.db')
    if db.open():
        return True
    else:
        print db.lastError().text()
        return False

class adminPanel:
    def __init__(self, parent=None):
        self.MainWindow = QtGui.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.botonCancelar.clicked.connect(self.salir)
        self.ui.botonGuardar.clicked.connect(self.guardar)
        self.ui.pushButtonPermitir.clicked.connect(self.agregarPermitido)
        self.ui.pushButtonDenegar.clicked.connect(self.agregarDenegado)
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('kerberus.db')
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
        self.ui.tableViewDenegados.show()

        self.MainWindow.show()

    def salir(self):
        self.MainWindow.close()

    def guardar(self):
        self.modelPermitidos.submitAll()
        self.modelDenegados.submitAll()

    def agregarPermitido(self):
        dominio = self.ui.lineEditPermitidos.text()
        registro = QtSql.QSqlRecord()
        registro.setValue('url','prueba')
        registro.setValue('usuario',2)
        registro.setValue('estado',1)
        if self.modelPermitidos.insertRecord(1, registro):
            print "anda"
        else:
            print "nooo"
        self.modelPermitidos.submitAll()

    def agregarDenegado(self):
        pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    #if not createConnection():
        #sys.exit(1)

    admin = adminPanel()
    sys.exit(app.exec_())