# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/Ui_RegisterWindow.ui'
#
# Created: Mon Apr 14 11:24:52 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_RegisterWindow(object):
    def setupUi(self, RegisterWindow):
        RegisterWindow.setObjectName("RegisterWindow")
        RegisterWindow.resize(292, 227)
        self.centralwidget = QtGui.QWidget(RegisterWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancel_btn = QtGui.QPushButton(self.centralwidget)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout.addWidget(self.cancel_btn)
        self.register_btn = QtGui.QPushButton(self.centralwidget)
        self.register_btn.setObjectName("register_btn")
        self.horizontalLayout.addWidget(self.register_btn)
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
        self.password1_le = QtGui.QLineEdit(self.centralwidget)
        self.password1_le.setText("")
        self.password1_le.setEchoMode(QtGui.QLineEdit.Password)
        self.password1_le.setObjectName("password1_le")
        self.verticalLayout.addWidget(self.password1_le)
        self.confirm_password_lbl = QtGui.QLabel(self.centralwidget)
        self.confirm_password_lbl.setObjectName("confirm_password_lbl")
        self.verticalLayout.addWidget(self.confirm_password_lbl)
        self.password2_le = QtGui.QLineEdit(self.centralwidget)
        self.password2_le.setEchoMode(QtGui.QLineEdit.Password)
        self.password2_le.setObjectName("password2_le")
        self.verticalLayout.addWidget(self.password2_le)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        RegisterWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(RegisterWindow)
        self.statusbar.setObjectName("statusbar")
        RegisterWindow.setStatusBar(self.statusbar)

        self.retranslateUi(RegisterWindow)
        QtCore.QMetaObject.connectSlotsByName(RegisterWindow)
        RegisterWindow.setTabOrder(self.username_le, self.password1_le)
        RegisterWindow.setTabOrder(self.password1_le, self.password2_le)
        RegisterWindow.setTabOrder(self.password2_le, self.register_btn)
        RegisterWindow.setTabOrder(self.register_btn, self.cancel_btn)

    def retranslateUi(self, RegisterWindow):
        RegisterWindow.setWindowTitle(QtGui.QApplication.translate("RegisterWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_btn.setText(QtGui.QApplication.translate("RegisterWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.register_btn.setText(QtGui.QApplication.translate("RegisterWindow", "Register", None, QtGui.QApplication.UnicodeUTF8))
        self.username_lbl.setText(QtGui.QApplication.translate("RegisterWindow", "User Name", None, QtGui.QApplication.UnicodeUTF8))
        self.password_lbl.setText(QtGui.QApplication.translate("RegisterWindow", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.confirm_password_lbl.setText(QtGui.QApplication.translate("RegisterWindow", "Confirm Password", None, QtGui.QApplication.UnicodeUTF8))

