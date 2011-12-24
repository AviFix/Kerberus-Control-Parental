# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formulario.ui'
#
# Created: Sat Dec 24 17:49:27 2011
#      by: PyQt4 UI code generator 4.8.5
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
        Form.resize(684, 319)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Password de administrador", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setText(QtGui.QApplication.translate("Form", "Configure la password de Administrador.", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setText(QtGui.QApplication.translate("Form", "Esta password le permitirá deshabilitar temporalmente el filtrado de kerberus \n"
"y a su vez,  le será requerida para desinstalarlo.\n"
"Es muy recomendable que la recuerde.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setScaledContents(False)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.label_passwordActual = QtGui.QLabel(Form)
        self.label_passwordActual.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setBold(True)
        font.setWeight(75)
        self.label_passwordActual.setFont(font)
        self.label_passwordActual.setText(QtGui.QApplication.translate("Form", "Password actual", None, QtGui.QApplication.UnicodeUTF8))
        self.label_passwordActual.setObjectName(_fromUtf8("label_passwordActual"))
        self.verticalLayout.addWidget(self.label_passwordActual)
        self.password_actual = QtGui.QLineEdit(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        self.password_actual.setFont(font)
        self.password_actual.setObjectName(_fromUtf8("password_actual"))
        self.verticalLayout.addWidget(self.password_actual)
        self.label_3 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setText(QtGui.QApplication.translate("Form", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.password1 = QtGui.QLineEdit(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        self.password1.setFont(font)
        self.password1.setEchoMode(QtGui.QLineEdit.Password)
        self.password1.setObjectName(_fromUtf8("password1"))
        self.verticalLayout.addWidget(self.password1)
        self.label_4 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setText(QtGui.QApplication.translate("Form", "Vuelva a ingresar la password", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.password2 = QtGui.QLineEdit(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        self.password2.setFont(font)
        self.password2.setEchoMode(QtGui.QLineEdit.Password)
        self.password2.setObjectName(_fromUtf8("password2"))
        self.verticalLayout.addWidget(self.password2)
        self.boton = QtGui.QPushButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.boton.sizePolicy().hasHeightForWidth())
        self.boton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        self.boton.setFont(font)
        self.boton.setText(QtGui.QApplication.translate("Form", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))
        self.boton.setObjectName(_fromUtf8("boton"))
        self.verticalLayout.addWidget(self.boton)
        self.label_3.setBuddy(self.password1)
        self.label_4.setBuddy(self.password2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.password_actual, self.password1)
        Form.setTabOrder(self.password1, self.password2)

    def retranslateUi(self, Form):
        pass

