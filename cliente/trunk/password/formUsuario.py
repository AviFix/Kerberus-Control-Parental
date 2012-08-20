# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formUsuario.ui'
#
# Created: Mon Aug 20 15:02:01 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.setWindowModality(QtCore.Qt.ApplicationModal)
        Form.resize(594, 190)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.gridLayoutWidget = QtGui.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 570, 111))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        self.gridLayoutWidget.setFont(font)
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.Descripcion = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setPointSize(11)
        self.Descripcion.setFont(font)
        self.Descripcion.setObjectName(_fromUtf8("Descripcion"))
        self.gridLayout.addWidget(self.Descripcion, 3, 0, 1, 3)
        self.password = QtGui.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        self.password.setFont(font)
        self.password.setFocusPolicy(QtCore.Qt.NoFocus)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName(_fromUtf8("password"))
        self.gridLayout.addWidget(self.password, 4, 0, 1, 1)
        self.titulo = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.titulo.setFont(font)
        self.titulo.setObjectName(_fromUtf8("titulo"))
        self.gridLayout.addWidget(self.titulo, 2, 0, 1, 1)
        self.boton = QtGui.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        self.boton.setFont(font)
        self.boton.setObjectName(_fromUtf8("boton"))
        self.gridLayout.addWidget(self.boton, 4, 1, 1, 1)
        self.botoncancelar = QtGui.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        self.botoncancelar.setFont(font)
        self.botoncancelar.setObjectName(_fromUtf8("botoncancelar"))
        self.gridLayout.addWidget(self.botoncancelar, 4, 2, 1, 1)
        self.Descripcion_2 = QtGui.QLabel(Form)
        self.Descripcion_2.setGeometry(QtCore.QRect(20, 120, 568, 34))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setPointSize(11)
        self.Descripcion_2.setFont(font)
        self.Descripcion_2.setOpenExternalLinks(True)
        self.Descripcion_2.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.Descripcion_2.setObjectName(_fromUtf8("Descripcion_2"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.password, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.boton.click)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.password, self.boton)
        Form.setTabOrder(self.boton, self.botoncancelar)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Password de administrador", None, QtGui.QApplication.UnicodeUTF8))
        self.Descripcion.setText(QtGui.QApplication.translate("Form", "Ingrese la password del usuario adminitrador de kerberus", None, QtGui.QApplication.UnicodeUTF8))
        self.titulo.setText(QtGui.QApplication.translate("Form", "Deshabilitar Filtrado de Kerberus", None, QtGui.QApplication.UnicodeUTF8))
        self.boton.setText(QtGui.QApplication.translate("Form", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))
        self.botoncancelar.setText(QtGui.QApplication.translate("Form", "Cancelar", None, QtGui.QApplication.UnicodeUTF8))
        self.Descripcion_2.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><a href=\"http://images.kerberus.com.ar/!RecordarPassword!\"><span style=\" text-decoration: underline; color:#0000ff;\">¿Olvido su contraseña?</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

