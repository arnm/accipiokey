# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/Ui_NotificationWindow.ui'
#
# Created: Wed Apr 16 19:10:53 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_NotificationWindow(object):
    def setupUi(self, NotificationWindow):
        NotificationWindow.setObjectName("NotificationWindow")
        NotificationWindow.resize(423, 88)
        self.centralwidget = QtGui.QWidget(NotificationWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.completion_lbl = QtGui.QLabel(self.centralwidget)
        self.completion_lbl.setObjectName("completion_lbl")
        self.gridLayout.addWidget(self.completion_lbl, 0, 0, 1, 1)
        self.correction_lbl = QtGui.QLabel(self.centralwidget)
        self.correction_lbl.setText("")
        self.correction_lbl.setObjectName("correction_lbl")
        self.gridLayout.addWidget(self.correction_lbl, 1, 0, 1, 1)
        self.snippet_lbl = QtGui.QLabel(self.centralwidget)
        self.snippet_lbl.setText("")
        self.snippet_lbl.setObjectName("snippet_lbl")
        self.gridLayout.addWidget(self.snippet_lbl, 2, 0, 1, 1)
        NotificationWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(NotificationWindow)
        QtCore.QMetaObject.connectSlotsByName(NotificationWindow)

    def retranslateUi(self, NotificationWindow):
        NotificationWindow.setWindowTitle(QtGui.QApplication.translate("NotificationWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.completion_lbl.setText(QtGui.QApplication.translate("NotificationWindow", "<html><head/><body><p align=\"center\"><br/></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

