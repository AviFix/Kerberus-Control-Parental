# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formulario.ui'
#
# Created: Mon Aug 29 21:41:22 2011
#      by: PyQt4 UI code generator 4.8.3
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
        Form.resize(503, 289)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(6, 6, 471, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(6, 33, 479, 41))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(6, 106, 75, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.password1 = QtGui.QLineEdit(Form)
        self.password1.setGeometry(QtCore.QRect(6, 133, 311, 27))
        self.password1.setEchoMode(QtGui.QLineEdit.Password)
        self.password1.setObjectName(_fromUtf8("password1"))
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(6, 166, 230, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.password2 = QtGui.QLineEdit(Form)
        self.password2.setGeometry(QtCore.QRect(6, 193, 311, 27))
        self.password2.setEchoMode(QtGui.QLineEdit.Password)
        self.password2.setObjectName(_fromUtf8("password2"))
        self.boton = QtGui.QPushButton(Form)
        self.boton.setGeometry(QtCore.QRect(230, 240, 80, 29))
        self.boton.setObjectName(_fromUtf8("boton"))
        self.label_3.setBuddy(self.password1)
        self.label_4.setBuddy(self.password2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.password1, self.password2)
        Form.setTabOrder(self.password2, self.boton)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Password de administrador", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Configure la password de Administrador.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Esta password le permitirá deshabilitar el filtrado de kerberus \n"
" de forma temporal en caso de necesitarlo.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Vuelva a ingresar la password", None, QtGui.QApplication.UnicodeUTF8))
        self.boton.setText(QtGui.QApplication.translate("Form", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))

