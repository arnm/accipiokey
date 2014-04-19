# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/Ui_NewSnippetDialog.ui'
#
# Created: Fri Apr 18 16:03:52 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewSnippetDialog(object):
    def setupUi(self, NewSnippetDialog):
        NewSnippetDialog.setObjectName("NewSnippetDialog")
        NewSnippetDialog.resize(360, 110)
        self.gridLayout = QtWidgets.QGridLayout(NewSnippetDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.text_lbl = QtWidgets.QLabel(NewSnippetDialog)
        self.text_lbl.setObjectName("text_lbl")
        self.gridLayout.addWidget(self.text_lbl, 1, 0, 1, 1)
        self.snippet_lbl = QtWidgets.QLabel(NewSnippetDialog)
        self.snippet_lbl.setObjectName("snippet_lbl")
        self.gridLayout.addWidget(self.snippet_lbl, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewSnippetDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 5)
        self.snippet_le = QtWidgets.QLineEdit(NewSnippetDialog)
        self.snippet_le.setObjectName("snippet_le")
        self.gridLayout.addWidget(self.snippet_le, 0, 1, 1, 4)
        self.text_le = QtWidgets.QLineEdit(NewSnippetDialog)
        self.text_le.setObjectName("text_le")
        self.gridLayout.addWidget(self.text_le, 1, 1, 1, 4)

        self.retranslateUi(NewSnippetDialog)
        self.buttonBox.accepted.connect(NewSnippetDialog.accept)
        self.buttonBox.rejected.connect(NewSnippetDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewSnippetDialog)
        NewSnippetDialog.setTabOrder(self.snippet_le, self.text_le)
        NewSnippetDialog.setTabOrder(self.text_le, self.buttonBox)

    def retranslateUi(self, NewSnippetDialog):
        _translate = QtCore.QCoreApplication.translate
        NewSnippetDialog.setWindowTitle(_translate("NewSnippetDialog", "Dialog"))
        self.text_lbl.setText(_translate("NewSnippetDialog", "Text"))
        self.snippet_lbl.setText(_translate("NewSnippetDialog", "Snippet"))

