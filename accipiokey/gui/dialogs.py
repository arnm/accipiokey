from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from accipiokey.gui.ui.Ui_NewSnippetDialog import Ui_NewSnippetDialog


class NewSnippetDialog(QDialog):

    new_snippet = pyqtSignal(dict)

    def __init__(self, parent):
        super(NewSnippetDialog, self).__init__(parent)

        # ui setup
        self.ui = Ui_NewSnippetDialog()
        self.ui.setupUi(self)

        self.setWindowTitle('Add New Snippet')
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.snippet_le.setFocus()

        self.ui.snippet_le.textChanged.connect(self._on_snippet_le_change)
        self.ui.text_le.textChanged.connect(self._on_text_le_change)

    def _on_snippet_le_change(self, text):
        self._update_le()

    def _on_text_le_change(self, text):
        self._update_le()

    def _update_le(self):
        snippet = self.ui.snippet_le.text().strip()
        text = self.ui.text_le.text().strip()
        if not snippet:
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            return

        if not text or len(snippet) > len(text):
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            return

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
