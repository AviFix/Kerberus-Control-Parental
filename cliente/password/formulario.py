# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formulario.ui'
#
# Created: Wed Aug 31 10:10:00 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(435, 337)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget = QtGui.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 411, 311))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.label_passwordActual = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_passwordActual.setEnabled(True)
        self.label_passwordActual.setObjectName("label_passwordActual")
        self.verticalLayout.addWidget(self.label_passwordActual)
        self.password_actual = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.password_actual.setObjectName("password_actual")
        self.verticalLayout.addWidget(self.password_actual)
        self.label_3 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.password1 = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.password1.setEchoMode(QtGui.QLineEdit.Password)
        self.password1.setObjectName("password1")
        self.verticalLayout.addWidget(self.password1)
        self.label_4 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.password2 = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.password2.setEchoMode(QtGui.QLineEdit.Password)
        self.password2.setObjectName("password2")
        self.verticalLayout.addWidget(self.password2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.boton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.boton.setObjectName("boton")
        self.verticalLayout.addWidget(self.boton)
        self.label_3.setBuddy(self.password1)
        self.label_4.setBuddy(self.password2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Password de administrador", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Configure la password de Administrador.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Esta password le permitirá deshabilitar el filtrado de kerberus \n"
" de forma temporal en caso de necesitarlo.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_passwordActual.setText(QtGui.QApplication.translate("Form", "Password actual", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Vuelva a ingresar la password", None, QtGui.QApplication.UnicodeUTF8))
        self.boton.setText(QtGui.QApplication.translate("Form", "Aceptar", None, QtGui.QApplication.UnicodeUTF8))

