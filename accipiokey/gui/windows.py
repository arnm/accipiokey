from accipiokey.gui.dialogs import *
from accipiokey.core.documents import *
from accipiokey.gui.delegates import *
from accipiokey.gui.ui.Ui_LoginWindow import Ui_LoginWindow
from accipiokey.gui.ui.Ui_NotificationWindow import Ui_NotificationWindow
from accipiokey.gui.ui.Ui_RegisterWindow import Ui_RegisterWindow
from accipiokey.gui.ui.Ui_UserWindow import Ui_UserWindow
from accipiokey.core.emitters import *
from accipiokey.core.logger import Logger
from itertools import izip
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class LoginWindow(QMainWindow):

    login_signal = pyqtSignal(dict)
    register_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)

        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)

        # signals
        self.ui.login_btn.clicked.connect(self._on_login_btn_click)
        self.ui.register_btn.clicked.connect(self._on_register_btn_click)
        self.ui.password_le.returnPressed.connect(
            self._on_password_le_return_pressed)

        # ui setup
        self.setWindowTitle('Accipio Key Login')
        self.ui.username_le.setFocus()

        # center window
        r = self.geometry()
        r.moveCenter(QApplication.desktop().availableGeometry().center())
        self.setGeometry(r)

    def _on_password_le_return_pressed(self):
        self._on_login_btn_click()

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

    register_signal = pyqtSignal(dict)
    cancel_signal = pyqtSignal()

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

    text_upload_signal = pyqtSignal(str)

    def __init__(self, user, parent=None):
        super(UserWindow, self).__init__(parent)

        self._user = user
        self._statsheet = StatSheet.objects(user=self._user)[0]

        # ui setup
        self.ui = Ui_UserWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(self._user.username)

        # usage table view
        self.stats_model_headers = ['Category', 'Statistic']
        self.stats_model = QStandardItemModel()
        self.stats_model.setHorizontalHeaderLabels(self.stats_model_headers)
        self.ui.stats_tv.setModel(self.stats_model)
        self.ui.stats_tv.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.stats_tv.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.update_stats_model()

       # snippets table view
        self.snippets_model_headers = ['Snippet', 'Text']
        self.snippets_model = QStandardItemModel()
        self.snippets_model.setHorizontalHeaderLabels(self.snippets_model_headers)
        self.ui.snippets_tv.setModel(self.snippets_model)
        self.ui.snippets_tv.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for snippet, text in self._user.snippets.items():
            self.snippets_model.appendRow([QStandardItem(snippet), QStandardItem(text)])

        # shortcuts table view
        self.shortcuts_model_headers = ['Shortcut', 'Binding']
        self.shortcuts_model = QStandardItemModel()
        self.shortcuts_model.setHorizontalHeaderLabels(self.shortcuts_model_headers)
        self.ui.shortcuts_tv.setModel(self.shortcuts_model)
        self.ui.shortcuts_tv.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.shortcuts_tv.setItemDelegate(QKeySequenceEditDelegate())

        for shortcut, binding in self._user.shortcuts.items():
            shortcut_item = QStandardItem(shortcut)
            shortcut_item.setFlags(shortcut_item.flags() & ~Qt.ItemIsEditable)
            binding_item = QStandardItem(','.join(binding))
            self.shortcuts_model.appendRow([shortcut_item, binding_item])

        # toolbar setup
        self.ui.toolBar.addAction(self.ui.actionToggleAppState)
        self.ui.toolBar.addAction(self.ui.actionLogout)

        # center window
        r = self.geometry()
        r.moveCenter(QApplication.desktop().availableGeometry().center())
        self.setGeometry(r)

        # icons
        self.ui.actionToggleAppState.setIcon(QIcon('ui/icons/play.png'))
        self.ui.actionLogout.setIcon(QIcon('ui/icons/cross.png'))
        self.ui.improve_btn.setIcon(QIcon('ui/icons/add-text.png'))
        self.ui.add_snippet_btn.setIcon(QIcon('ui/icons/plus.png'))
        self.ui.remove_snippet_btn.setIcon(QIcon('ui/icons/minus.png'))

        self.notification_window = NotificationWindow(user=self._user,
                                                    parent=self)
        self.ui.nw_pos_combo.addItems([
                NotificationWindow.TOP,
                NotificationWindow.BOTTOM,
                NotificationWindow.TOP_LEFT,
                NotificationWindow.TOP_RIGHT,
                NotificationWindow.BOTTOM_LEFT,
                NotificationWindow.BOTTOM_RIGHT
            ])

        # signal handling
        self.ui.actionToggleAppState.toggled.connect(
            self._on_action_toggle_app_state_toggled)

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

        self.ui.improve_btn.clicked.connect(self._on_improve_btn_clicked)

    # TODO: change starting directory
    def _on_improve_btn_clicked(self):
        filepath, type = QFileDialog.getOpenFileName(
            self,
            'Process File',
            '/home/',
            'Text Files (*.txt)')
        self.text_upload_signal.emit(filepath)

    def _on_action_toggle_app_state_toggled(self, checked):
        if not checked:
            self.ui.actionToggleAppState.setIcon(QIcon('ui/icons/play.png'))
            self.notification_window.close()
            return
        self.ui.actionToggleAppState.setIcon(QIcon('ui/icons/stop.png'))
        self.notification_window.show()

    # TODO: not the most efficient way to handle updates
    def update_stats_model(self):
        self.stats_model.clear()
        self.stats_model.setHorizontalHeaderLabels(self.stats_model_headers)
        self._statsheet = StatSheet.objects(user=self._user)[0]

        self.stats_model.appendRow(
            [QStandardItem('Words Corrected'),
            QStandardItem(str(self._statsheet.words_corrected))])

        self.stats_model.appendRow(
            [QStandardItem('Words Completed'),
            QStandardItem(str(self._statsheet.words_completed))])

        self.stats_model.appendRow(
            [QStandardItem('Snippets Used'),
            QStandardItem(str(self._statsheet.snippets_used))])

        self.stats_model.appendRow(
            [QStandardItem('Key Strokes Saved'),
            QStandardItem(str(self._statsheet.keystrokes_saved))])

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
            snippet = nsd.ui.snippet_le.text().strip()
            text = nsd.ui.text_le.text().strip()
            self._user.snippets[snippet] = text
            Logger.info('UserWindow: Adding Snippet (%s)', {snippet: text})
            self._user.save()
            self.snippets_model.appendRow(
                [QStandardItem(snippet), QStandardItem(text)])

        nsd.ui.buttonBox.accepted.connect(on_accepted)
        nsd.show()

    def _on_remove_snippet_btn_clicked(self):
        indexes = self.ui.snippets_tv.selectionModel().selection().indexes()
        for index in indexes:
            if self.snippets_model.hasIndex(index.row(), index.column()):
                snippet = self.snippets_model.data(index)
                Logger.info('UserWindow: Removing Snippet (%s)', snippet)
                self.snippets_model.removeRow(index.row())
                del self._user.snippets[snippet]
                self._user.save()

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

    def __init__(self, user, parent=None):
        super(NotificationWindow, self).__init__(parent,
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) # Window flags

        self._user = user

        # ui setup
        self.ui = Ui_NotificationWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Accipio Key Notifications')

        self.setWindowOpacity(0.85)
        self.set_position(self.TOP)

        # emitter signals
        CorrectionSignalEmitter.instance().possible_correction_signal.connect(
            self._on_possible_correction_signal)

        CompletionSignalEmitter.instance().possible_completion_signal.connect(
            self._on_possible_completion_signal)

        WordSignalEmitter.instance().current_word_signal.connect(
            self._on_current_word_signal)

    def _get_rich_text(self, msg, color, font_size=12):
        rich_text = '''
            <html>
            <head/>
            <body>
            <p align="center">
                <span style=" font-size:%spt; font-weight:600; color:#%s;">
                %s
                </span>
            </p>
            </body>
            </html>''' % (font_size, color, msg)
        return rich_text

    @pyqtSlot(str)
    def _on_possible_completion_signal(self, possible_completion_signal):
        rich_text = self._get_rich_text(possible_completion_signal, '00C20D')
        self.ui.completion_lbl.setText(rich_text)

    @pyqtSlot(str)
    def _on_possible_correction_signal(self, possible_correction_signal):
        if not possible_correction_signal:
            self.ui.correction_lbl.setText('')
            return

        rich_text = self._get_rich_text(possible_correction_signal, 'FF0000')
        self.ui.correction_lbl.setText(rich_text)

    @pyqtSlot(str)
    def _on_current_word_signal(self, current_word_signal):
        if not current_word_signal in self._user.snippets:
            self.ui.snippet_lbl.setText('')
            return

        rich_text = self._get_rich_text(current_word_signal, '245BFF')
        self.ui.snippet_lbl.setText(rich_text)

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
