from accipiokey.gui.ui.Ui_LoginWindow import Ui_LoginWindow
from accipiokey.gui.ui.Ui_RegisterWindow import Ui_RegisterWindow
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

    def _on_register_btn_click(self):
        username = self.ui.username_le.text().encode('utf-8').strip()
        passowrd1 = self.ui.password1_le.text().encode('utf-8').strip()
        password2 = self.ui.password2_le.text().encode('utf-8').strip()

        if not username:
            self.ui.statusbar.showMessage('Input a username', 3000)
            return
        if not password1 or not password2 or passowrd1 != password2:
            self.ui.statusbar.showMessage('Input matching passwords', 3000)
            return

        self.register_signal.emit({'username': username, 'password': password1})

    def _on_cancel_btn_click(self):
        self.cancel_signal.emit()
