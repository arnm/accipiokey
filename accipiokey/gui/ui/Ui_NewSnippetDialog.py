# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/Ui_NewSnippetDialog.ui'
#
# Created: Wed Apr 16 10:46:48 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_NewSnippetDialog(object):
    def setupUi(self, NewSnippetDialog):
        NewSnippetDialog.setObjectName("NewSnippetDialog")
        NewSnippetDialog.resize(360, 110)
        self.gridLayout = QtGui.QGridLayout(NewSnippetDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.text_lbl = QtGui.QLabel(NewSnippetDialog)
        self.text_lbl.setObjectName("text_lbl")
        self.gridLayout.addWidget(self.text_lbl, 1, 0, 1, 1)
        self.snippet_lbl = QtGui.QLabel(NewSnippetDialog)
        self.snippet_lbl.setObjectName("snippet_lbl")
        self.gridLayout.addWidget(self.snippet_lbl, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(NewSnippetDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 5)
        self.snippet_le = QtGui.QLineEdit(NewSnippetDialog)
        self.snippet_le.setObjectName("snippet_le")
        self.gridLayout.addWidget(self.snippet_le, 0, 1, 1, 4)
        self.text_le = QtGui.QLineEdit(NewSnippetDialog)
        self.text_le.setObjectName("text_le")
        self.gridLayout.addWidget(self.text_le, 1, 1, 1, 4)

        self.retranslateUi(NewSnippetDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewSnippetDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), NewSnippetDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewSnippetDialog)

    def retranslateUi(self, NewSnippetDialog):
        NewSnippetDialog.setWindowTitle(QtGui.QApplication.translate("NewSnippetDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.text_lbl.setText(QtGui.QApplication.translate("NewSnippetDialog", "Text", None, QtGui.QApplication.UnicodeUTF8))
        self.snippet_lbl.setText(QtGui.QApplication.translate("NewSnippetDialog", "Snippet", None, QtGui.QApplication.UnicodeUTF8))

