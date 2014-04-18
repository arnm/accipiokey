from accipiokey.core.apputils import unicode_to_keycode
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class QKeySequenceEditDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(QKeySequenceEditDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        qkse = QKeySequenceEdit(parent)
        return qkse

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setKeySequence(value)

    def setModelData(self, editor, model, index):
        sequence = editor.keySequence().toString().split('+')
        binding = [unicode_to_keycode(key) for key in sequence]
        model.setData(index, ','.join(binding), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
