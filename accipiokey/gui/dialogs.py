from PySide.QtCore import *
from PySide.QtGui import *
from accipiokey.gui.ui.Ui_NewSnippetDialog import Ui_NewSnippetDialog


class NewSnippetDialog(QDialog):

    new_snippet = Signal(dict)

    def __init__(self, parent):
        super(NewSnippetDialog, self).__init__(parent)

        self.ui = Ui_NewSnippetDialog()
        self.ui.setupUi(self)

        self.ui.buttonBox.accepted.connect(self._on_buttonBox_accepted)
        self.ui.buttonBox.rejected.connect(self_.on_buttonBox_rejected)

    def _on_buttonBox_accepted(self):
        pass

    def _on_buttonBox_rejected(self):
        pass
