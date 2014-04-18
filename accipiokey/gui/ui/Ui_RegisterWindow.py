# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/Ui_RegisterWindow.ui'
#
# Created: Fri Apr 18 10:16:45 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RegisterWindow(object):
    def setupUi(self, RegisterWindow):
        RegisterWindow.setObjectName("RegisterWindow")
        RegisterWindow.resize(292, 227)
        self.centralwidget = QtWidgets.QWidget(RegisterWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancel_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout.addWidget(self.cancel_btn)
        self.register_btn = QtWidgets.QPushButton(self.centralwidget)
        self.register_btn.setObjectName("register_btn")
        self.horizontalLayout.addWidget(self.register_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.username_lbl = QtWidgets.QLabel(self.centralwidget)
        self.username_lbl.setObjectName("username_lbl")
        self.verticalLayout.addWidget(self.username_lbl)
        self.username_le = QtWidgets.QLineEdit(self.centralwidget)
        self.username_le.setObjectName("username_le")
        self.verticalLayout.addWidget(self.username_le)
        self.password_lbl = QtWidgets.QLabel(self.centralwidget)
        self.password_lbl.setObjectName("password_lbl")
        self.verticalLayout.addWidget(self.password_lbl)
        self.password1_le = QtWidgets.QLineEdit(self.centralwidget)
        self.password1_le.setText("")
        self.password1_le.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password1_le.setObjectName("password1_le")
        self.verticalLayout.addWidget(self.password1_le)
        self.confirm_password_lbl = QtWidgets.QLabel(self.centralwidget)
        self.confirm_password_lbl.setObjectName("confirm_password_lbl")
        self.verticalLayout.addWidget(self.confirm_password_lbl)
        self.password2_le = QtWidgets.QLineEdit(self.centralwidget)
        self.password2_le.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password2_le.setObjectName("password2_le")
        self.verticalLayout.addWidget(self.password2_le)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        RegisterWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(RegisterWindow)
        self.statusbar.setObjectName("statusbar")
        RegisterWindow.setStatusBar(self.statusbar)

        self.retranslateUi(RegisterWindow)
        QtCore.QMetaObject.connectSlotsByName(RegisterWindow)
        RegisterWindow.setTabOrder(self.username_le, self.password1_le)
        RegisterWindow.setTabOrder(self.password1_le, self.password2_le)
        RegisterWindow.setTabOrder(self.password2_le, self.register_btn)
        RegisterWindow.setTabOrder(self.register_btn, self.cancel_btn)

    def retranslateUi(self, RegisterWindow):
        _translate = QtCore.QCoreApplication.translate
        RegisterWindow.setWindowTitle(_translate("RegisterWindow", "MainWindow"))
        self.cancel_btn.setText(_translate("RegisterWindow", "Cancel"))
        self.register_btn.setText(_translate("RegisterWindow", "Register"))
        self.username_lbl.setText(_translate("RegisterWindow", "User Name"))
        self.password_lbl.setText(_translate("RegisterWindow", "Password"))
        self.confirm_password_lbl.setText(_translate("RegisterWindow", "Confirm Password"))

