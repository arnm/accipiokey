# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/Ui_NotificationWindow.ui'
#
# Created: Fri Apr 18 10:16:45 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NotificationWindow(object):
    def setupUi(self, NotificationWindow):
        NotificationWindow.setObjectName("NotificationWindow")
        NotificationWindow.resize(423, 88)
        self.centralwidget = QtWidgets.QWidget(NotificationWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.completion_lbl = QtWidgets.QLabel(self.centralwidget)
        self.completion_lbl.setObjectName("completion_lbl")
        self.gridLayout.addWidget(self.completion_lbl, 0, 0, 1, 1)
        self.correction_lbl = QtWidgets.QLabel(self.centralwidget)
        self.correction_lbl.setText("")
        self.correction_lbl.setObjectName("correction_lbl")
        self.gridLayout.addWidget(self.correction_lbl, 1, 0, 1, 1)
        self.snippet_lbl = QtWidgets.QLabel(self.centralwidget)
        self.snippet_lbl.setText("")
        self.snippet_lbl.setObjectName("snippet_lbl")
        self.gridLayout.addWidget(self.snippet_lbl, 2, 0, 1, 1)
        NotificationWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(NotificationWindow)
        QtCore.QMetaObject.connectSlotsByName(NotificationWindow)

    def retranslateUi(self, NotificationWindow):
        _translate = QtCore.QCoreApplication.translate
        NotificationWindow.setWindowTitle(_translate("NotificationWindow", "MainWindow"))
        self.completion_lbl.setText(_translate("NotificationWindow", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))

