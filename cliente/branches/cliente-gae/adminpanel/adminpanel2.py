import sys
from testdbtableform import *
from PyQt4 import QtSql, QtGui, QtCore, QtSql

def createConnection():
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('kerberus.db')
    if db.open():
        return True
    else:
        print db.lastError().text()
        return False

class MyForm(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable("dominios_usuario")
        self.model.setEditStrategy(2)
        self.model.select()
        self.ui.tableView.setModel(self.model)
        self.ui.Submit.clicked.connect(self.dbinput)

    def dbinput(self):
        self.model.insertRow(-1)
        text = self.ui.lineEdit.text()
        if self.model.setData(self.model.index(-1, 0), text):
            self.model.submitAll()
        else:
            print "There was a problem setting the data."

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    if not createConnection():
        sys.exit(1)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())