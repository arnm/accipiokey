from accipiokey.gui.dialogs import *
from accipiokey.gui.ui.Ui_LoginWindow import Ui_LoginWindow
from accipiokey.gui.ui.Ui_NotificationWindow import Ui_NotificationWindow
from accipiokey.gui.ui.Ui_RegisterWindow import Ui_RegisterWindow
from accipiokey.gui.ui.Ui_UserWindow import Ui_UserWindow
from itertools import izip
from PySide.QtCore import *
from PySide.QtGui import *

class LoginWindow(QMainWindow):

    login_signal = Signal(dict)
    register_signal = Signal()

    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)

        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)

        # signals
        self.ui.login_btn.clicked.connect(self._on_login_btn_click)
        self.ui.register_btn.clicked.connect(self._on_register_btn_click)

        # ui setup
        self.setWindowTitle('Accipio Key Login')
        self.ui.username_le.setFocus()

        # center window
        r = self.geometry()
        r.moveCenter(QApplication.desktop().availableGeometry().center())
        self.setGeometry(r)

    def _on_login_btn_click(self):
        username = self.ui.username_le.text().encode('utf-8').strip()
        password = self.ui.password_le.text().encode('utf-8')

        if not username:
            self.ui.statusbar.showMessage('Input a username', 3000)
            return
        if not password:
            self.ui.statusbar.showMessage('Input a password', 3000)
            return

        credentials = {'username': username, 'password': password}
        self.login_signal.emit(credentials)

    def _on_register_btn_click(self):
        self.register_signal.emit()

class RegisterWindow(QMainWindow):

    register_signal = Signal(dict)
    cancel_signal = Signal()

    def __init__(self, parent=None):
        super(RegisterWindow, self).__init__(parent)

        self.ui = Ui_RegisterWindow()
        self.ui.setupUi(self)

        # signals
        self.ui.register_btn.clicked.connect(self._on_register_btn_click)
        self.ui.cancel_btn.clicked.connect(self._on_cancel_btn_click)

        # ui setup
        self.setWindowTitle('Accipio Key Registration')
        self.ui.username_le.setFocus()

        # center window
        r = self.geometry()
        r.moveCenter(QApplication.desktop().availableGeometry().center())
        self.setGeometry(r)

    def _on_register_btn_click(self):
        username = self.ui.username_le.text().encode('utf-8').strip()
        password1 = self.ui.password1_le.text().encode('utf-8').strip()
        password2 = self.ui.password2_le.text().encode('utf-8').strip()

        if not username:
            self.ui.statusbar.showMessage('Input a username', 3000)
            return
        if not password1 or not password2 or password1 != password2:
            self.ui.statusbar.showMessage('Input matching passwords', 3000)
            return

        self.register_signal.emit({'username': username, 'password': password1})

    def _on_cancel_btn_click(self):
        self.cancel_signal.emit()

class UserWindow(QMainWindow):

    def __init__(self, user, parent=None):
        super(UserWindow, self).__init__(parent)

        self._user = user

        # ui setup
        self.ui = Ui_UserWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(self._user.username)

        # snippets table view
        self.snippets_model_headers = ['Snippet', 'Text']
        self.snippets_model = QStandardItemModel()
        self.snippets_model.setHorizontalHeaderLabels(self.snippets_model_headers)
        self.ui.snippets_tv.setModel(self.snippets_model)
        self.ui.snippets_tv.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        for snippet, text in self._user.snippets.items():
            self.snippets_model.appendRow([QStandardItem(snippet), QStandardItem(text)])

        # shortcuts table view
        self.shortcuts_model_headers = ['Shortcut', 'Binding']
        self.shortcuts_model = QStandardItemModel()
        self.shortcuts_model.setHorizontalHeaderLabels(self.shortcuts_model_headers)
        self.ui.shortcuts_tv.setModel(self.shortcuts_model)
        self.ui.shortcuts_tv.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        for shortcut, binding in self._user.shortcuts.items():
            shortcut_item = QStandardItem(shortcut)
            shortcut_item.setFlags(shortcut_item.flags() & ~Qt.ItemIsEditable)
            binding_item = QStandardItem(','.join(binding))
            self.shortcuts_model.appendRow([shortcut_item, binding_item])

        # toolbar setup
        self.ui.app_state_toggle_btn = QPushButton()
        self.ui.app_state_toggle_btn.setText('On')
        self.ui.app_state_toggle_btn.setCheckable(True)
        self.ui.toolBar.addWidget(self.ui.app_state_toggle_btn)
        self.ui.toolBar.addAction(self.ui.actionLogout)

        self.notification_window = NotificationWindow(self)
        self.ui.nw_pos_combo.addItems([
            NotificationWindow.TOP,
            NotificationWindow.BOTTOM,
            NotificationWindow.TOP_LEFT,
            NotificationWindow.TOP_RIGHT,
            NotificationWindow.BOTTOM_LEFT,
            NotificationWindow.BOTTOM_RIGHT
            ])

        # center window
        r = self.geometry()
        r.moveCenter(QApplication.desktop().availableGeometry().center())
        self.setGeometry(r)

        # signal handling

        self.snippets_model.itemChanged.connect(
            self._on_snippets_model_item_changed)

        self.ui.add_snippet_btn.clicked.connect(
            self._on_add_snippet_btn_clicked)

        self.ui.remove_snippet_btn.clicked.connect(
            self._on_remove_snippet_btn_clicked)

        self.shortcuts_model.itemChanged.connect(
            self._on_shortcuts_model_item_changed)

        self.ui.nw_pos_combo.currentIndexChanged.connect(
            self._on_nw_pos_combo_change)

    # TODO: remove hard coded strings
    def _on_snippets_model_item_changed(self, item):
        changed_row = item.index().row()
        changed_column = item.index().column()

        # TODO: find a way to just change snippets that were changed, not all
        if self.snippets_model_headers[changed_column] == 'Snippet':
            items = []
            for row in xrange(self.snippets_model.rowCount()):
                for column in xrange(self.snippets_model.columnCount()):
                    index = self.snippets_model.index(row, column)
                    data = self.snippets_model.data(index)
                    items.append(data)
            items_iter = iter(items)
            snippets = dict(izip(items_iter, items_iter))
            self._user.snippets = snippets
            self._user.save()

        elif self.snippets_model_headers[changed_column] == 'Text':
            snippet_index = self.snippets_model.index(changed_row, changed_column-1)
            snippet = self.snippets_model.data(snippet_index)

            self._user.snippets[snippet] = item.text()
            self._user.save()

    def _on_add_snippet_btn_clicked(self):
        nsd = NewSnippetDialog(self)

        def on_accepted():
            print('accepted')

        def on_rejected():
            print('rejected')

        nsd.ui.buttonBox.accepted.connect(on_accepted)
        nsd.ui.buttonBox.rejected.connect(on_rejected)
        nsd.show()

    def _on_remove_snippet_btn_clicked(self):
        print('REMOVE')

    # TODO: changing shortcuts needs to be restricted to acceptable values
    def _on_shortcuts_model_item_changed(self, item):
        changed_row = item.index().row()
        changed_column = item.index().column()

        shortcut_index = self.shortcuts_model.index(changed_row, changed_column-1)
        shortcut = self.shortcuts_model.data(shortcut_index)
        self._user.shortcuts[shortcut] = item.text().split(',')
        self._user.save()

    def _on_nw_pos_combo_change(self, index):
        pos = self.ui.nw_pos_combo.itemText(index)
        self.notification_window.set_position(pos)

class NotificationWindow(QMainWindow):

    TOP, BOTTOM = ('Top', 'Bottom')
    TOP_LEFT, TOP_RIGHT = ('Top Left', 'Top Right')
    BOTTOM_LEFT, BOTTOM_RIGHT = ('Bottom Left', 'Bottom Right')

    def __init__(self, parent=None):
        super(NotificationWindow, self).__init__(parent,
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) # Window flags

        # ui setup
        self.ui = Ui_NotificationWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Accipio Key Notifications')

        self.setWindowOpacity(0.85)
        self.set_position(self.TOP)

    def set_position(self, pos):
        if pos == self.TOP: self.pin_top()
        elif pos == self.BOTTOM: self.pin_bottom()
        elif pos == self.TOP_LEFT: self.pin_top_left()
        elif pos == self.TOP_RIGHT: self.pin_top_right()
        elif pos == self.BOTTOM_LEFT: self.pin_bottom_left()
        elif pos == self.BOTTOM_RIGHT: self.pin_bottom_right()

    def pin_top(self):
        r = self.geometry()
        ag = QApplication.desktop().availableGeometry()
        r.moveCenter(ag.center())
        r.moveTop(ag.top())
        self.setGeometry(r)

    def pin_bottom(self):
        r = self.geometry()
        ag = QApplication.desktop().availableGeometry()
        r.moveCenter(ag.center())
        r.moveBottom(ag.bottom())
        self.setGeometry(r)

    def pin_bottom_left(self):
        r = self.geometry()
        ag = QApplication.desktop().availableGeometry()
        r.moveLeft(ag.left())
        r.moveBottom(ag.bottom())
        self.setGeometry(r)

    def pin_bottom_right(self):
        r = self.geometry()
        ag = QApplication.desktop().availableGeometry()
        r.moveLeft(ag.right())
        r.moveBottom(ag.bottom())
        self.setGeometry(r)

    def pin_top_left(self):
        r = self.geometry()
        ag = QApplication.desktop().availableGeometry()
        r.moveRight(ag.left())
        r.moveTop(ag.top())
        self.setGeometry(r)

    def pin_top_right(self):
        r = self.geometry()
        ag = QApplication.desktop().availableGeometry()
        r.moveRight(ag.right())
        r.moveTop(ag.top())
        self.setGeometry(r)



