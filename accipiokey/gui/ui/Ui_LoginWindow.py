# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/Ui_LoginWindow.ui'
#
# Created: Mon Apr 14 19:34:03 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(293, 177)
        self.centralwidget = QtGui.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.register_btn = QtGui.QPushButton(self.centralwidget)
        self.register_btn.setObjectName("register_btn")
        self.horizontalLayout.addWidget(self.register_btn)
        self.login_btn = QtGui.QPushButton(self.centralwidget)
        self.login_btn.setObjectName("login_btn")
        self.horizontalLayout.addWidget(self.login_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.username_lbl = QtGui.QLabel(self.centralwidget)
        self.username_lbl.setObjectName("username_lbl")
        self.verticalLayout.addWidget(self.username_lbl)
        self.username_le = QtGui.QLineEdit(self.centralwidget)
        self.username_le.setObjectName("username_le")
        self.verticalLayout.addWidget(self.username_le)
        self.password_lbl = QtGui.QLabel(self.centralwidget)
        self.password_lbl.setObjectName("password_lbl")
        self.verticalLayout.addWidget(self.password_lbl)
        self.password_le = QtGui.QLineEdit(self.centralwidget)
        self.password_le.setText("")
        self.password_le.setEchoMode(QtGui.QLineEdit.Password)
        self.password_le.setObjectName("password_le")
        self.verticalLayout.addWidget(self.password_le)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        LoginWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(LoginWindow)
        self.statusbar.setObjectName("statusbar")
        LoginWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)
        LoginWindow.setTabOrder(self.username_le, self.password_le)
        LoginWindow.setTabOrder(self.password_le, self.login_btn)
        LoginWindow.setTabOrder(self.login_btn, self.register_btn)

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle(QtGui.QApplication.translate("LoginWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.register_btn.setText(QtGui.QApplication.translate("LoginWindow", "Register", None, QtGui.QApplication.UnicodeUTF8))
        self.login_btn.setText(QtGui.QApplication.translate("LoginWindow", "Log In", None, QtGui.QApplication.UnicodeUTF8))
        self.username_lbl.setText(QtGui.QApplication.translate("LoginWindow", "User Name", None, QtGui.QApplication.UnicodeUTF8))
        self.password_lbl.setText(QtGui.QApplication.translate("LoginWindow", "Password", None, QtGui.QApplication.UnicodeUTF8))

