# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/Ui_UserWindow.ui'
#
# Created: Mon Apr 14 11:24:52 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_UserWindow(object):
    def setupUi(self, UserWindow):
        UserWindow.setObjectName("UserWindow")
        UserWindow.resize(410, 342)
        self.centralwidget = QtGui.QWidget(UserWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.stats_tab = QtGui.QWidget()
        self.stats_tab.setObjectName("stats_tab")
        self.gridLayout_2 = QtGui.QGridLayout(self.stats_tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableView = QtGui.QTableView(self.stats_tab)
        self.tableView.setObjectName("tableView")
        self.gridLayout_2.addWidget(self.tableView, 0, 0, 1, 1)
        self.tabWidget.addTab(self.stats_tab, "")
        self.settings_tab = QtGui.QWidget()
        self.settings_tab.setObjectName("settings_tab")
        self.tabWidget.addTab(self.settings_tab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        UserWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(UserWindow)
        self.statusbar.setObjectName("statusbar")
        UserWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(UserWindow)
        self.toolBar.setObjectName("toolBar")
        UserWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionLogout = QtGui.QAction(UserWindow)
        self.actionLogout.setObjectName("actionLogout")
        self.actionStart = QtGui.QAction(UserWindow)
        self.actionStart.setObjectName("actionStart")
        self.actionStop = QtGui.QAction(UserWindow)
        self.actionStop.setObjectName("actionStop")
        self.toolBar.addAction(self.actionStart)
        self.toolBar.addAction(self.actionStop)
        self.toolBar.addAction(self.actionLogout)

        self.retranslateUi(UserWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(UserWindow)

    def retranslateUi(self, UserWindow):
        UserWindow.setWindowTitle(QtGui.QApplication.translate("UserWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.stats_tab), QtGui.QApplication.translate("UserWindow", "Usage Stats", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings_tab), QtGui.QApplication.translate("UserWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("UserWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLogout.setText(QtGui.QApplication.translate("UserWindow", "logout", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStart.setText(QtGui.QApplication.translate("UserWindow", "start", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStop.setText(QtGui.QApplication.translate("UserWindow", "stop", None, QtGui.QApplication.UnicodeUTF8))

