# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/Ui_UserWindow.ui'
#
# Created: Fri Apr 18 15:26:20 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_UserWindow(object):
    def setupUi(self, UserWindow):
        UserWindow.setObjectName("UserWindow")
        UserWindow.resize(410, 525)
        self.centralwidget = QtWidgets.QWidget(UserWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.main_tw = QtWidgets.QTabWidget(self.centralwidget)
        self.main_tw.setObjectName("main_tw")
        self.stats_tab = QtWidgets.QWidget()
        self.stats_tab.setObjectName("stats_tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.stats_tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.improve_btn = QtWidgets.QPushButton(self.stats_tab)
        self.improve_btn.setObjectName("improve_btn")
        self.gridLayout_2.addWidget(self.improve_btn, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.stats_tv = QtWidgets.QTableView(self.stats_tab)
        self.stats_tv.setObjectName("stats_tv")
        self.gridLayout_2.addWidget(self.stats_tv, 0, 0, 1, 2)
        self.main_tw.addTab(self.stats_tab, "")
        self.settings_tab = QtWidgets.QWidget()
        self.settings_tab.setObjectName("settings_tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.settings_tab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.snippets_gb = QtWidgets.QGroupBox(self.settings_tab)
        self.snippets_gb.setObjectName("snippets_gb")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.snippets_gb)
        self.gridLayout_6.setObjectName("gridLayout_6")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem1, 1, 0, 1, 1)
        self.snippets_tv = QtWidgets.QTableView(self.snippets_gb)
        self.snippets_tv.setObjectName("snippets_tv")
        self.gridLayout_6.addWidget(self.snippets_tv, 0, 0, 1, 3)
        self.remove_snippet_btn = QtWidgets.QPushButton(self.snippets_gb)
        self.remove_snippet_btn.setText("")
        self.remove_snippet_btn.setObjectName("remove_snippet_btn")
        self.gridLayout_6.addWidget(self.remove_snippet_btn, 1, 1, 1, 1)
        self.add_snippet_btn = QtWidgets.QPushButton(self.snippets_gb)
        self.add_snippet_btn.setText("")
        self.add_snippet_btn.setObjectName("add_snippet_btn")
        self.gridLayout_6.addWidget(self.add_snippet_btn, 1, 2, 1, 1)
        self.gridLayout_3.addWidget(self.snippets_gb, 3, 0, 1, 2)
        self.shortcuts_gb = QtWidgets.QGroupBox(self.settings_tab)
        self.shortcuts_gb.setObjectName("shortcuts_gb")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.shortcuts_gb)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.shortcuts_tv = QtWidgets.QTableView(self.shortcuts_gb)
        self.shortcuts_tv.setObjectName("shortcuts_tv")
        self.gridLayout_4.addWidget(self.shortcuts_tv, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.shortcuts_gb, 2, 0, 1, 2)
        self.general_gb = QtWidgets.QGroupBox(self.settings_tab)
        self.general_gb.setObjectName("general_gb")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.general_gb)
        self.gridLayout_7.setObjectName("gridLayout_7")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem2, 1, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.general_gb)
        self.label.setObjectName("label")
        self.gridLayout_7.addWidget(self.label, 0, 2, 1, 1)
        self.nw_pos_combo = QtWidgets.QComboBox(self.general_gb)
        self.nw_pos_combo.setObjectName("nw_pos_combo")
        self.gridLayout_7.addWidget(self.nw_pos_combo, 1, 2, 1, 1)
        self.gridLayout_3.addWidget(self.general_gb, 1, 0, 1, 2)
        self.main_tw.addTab(self.settings_tab, "")
        self.playground_tab = QtWidgets.QWidget()
        self.playground_tab.setObjectName("playground_tab")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.playground_tab)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.playground_te = QtWidgets.QTextEdit(self.playground_tab)
        self.playground_te.setObjectName("playground_te")
        self.gridLayout_5.addWidget(self.playground_te, 0, 0, 1, 1)
        self.main_tw.addTab(self.playground_tab, "")
        self.gridLayout.addWidget(self.main_tw, 0, 0, 1, 1)
        UserWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(UserWindow)
        self.statusbar.setObjectName("statusbar")
        UserWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(UserWindow)
        self.toolBar.setObjectName("toolBar")
        UserWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionLogout = QtWidgets.QAction(UserWindow)
        self.actionLogout.setObjectName("actionLogout")
        self.actionToggleAppState = QtWidgets.QAction(UserWindow)
        self.actionToggleAppState.setCheckable(True)
        self.actionToggleAppState.setObjectName("actionToggleAppState")

        self.retranslateUi(UserWindow)
        self.main_tw.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(UserWindow)
        UserWindow.setTabOrder(self.main_tw, self.stats_tv)
        UserWindow.setTabOrder(self.stats_tv, self.shortcuts_tv)
        UserWindow.setTabOrder(self.shortcuts_tv, self.snippets_tv)
        UserWindow.setTabOrder(self.snippets_tv, self.playground_te)

    def retranslateUi(self, UserWindow):
        _translate = QtCore.QCoreApplication.translate
        UserWindow.setWindowTitle(_translate("UserWindow", "MainWindow"))
        self.improve_btn.setText(_translate("UserWindow", "Improve..."))
        self.main_tw.setTabText(self.main_tw.indexOf(self.stats_tab), _translate("UserWindow", "Usage Stats"))
        self.snippets_gb.setTitle(_translate("UserWindow", "Snippets"))
        self.shortcuts_gb.setTitle(_translate("UserWindow", "Shortcuts"))
        self.general_gb.setTitle(_translate("UserWindow", "General"))
        self.label.setText(_translate("UserWindow", "Notifications"))
        self.main_tw.setTabText(self.main_tw.indexOf(self.settings_tab), _translate("UserWindow", "Settings"))
        self.main_tw.setTabText(self.main_tw.indexOf(self.playground_tab), _translate("UserWindow", "Playground"))
        self.toolBar.setWindowTitle(_translate("UserWindow", "toolBar"))
        self.actionLogout.setText(_translate("UserWindow", "Log Out"))
        self.actionLogout.setToolTip(_translate("UserWindow", "Log Out"))
        self.actionToggleAppState.setText(_translate("UserWindow", "ToggleAppState"))
        self.actionToggleAppState.setToolTip(_translate("UserWindow", "Start/Stop"))

