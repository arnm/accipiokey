from accipiokey.documents import User
from accipiokey.modals import FileModal
from accipiokey.utils import *
from accipiokey.widgets import *
from accipiokey.dispatchers import *
from accipiokey.handlers import *

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager

from textblob import TextBlob
import mimetypes
import os


class AccipioKeyApp(App):
    title = 'Accipio Key'
    LOGIN_SCREEN, REGISTER_SCREEN, HOME_SCREEN = [str(i) for i in range(3)]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._user = None
        self._sm = ScreenManager()

        # dispatchers
        self._ked = KeyboardEventDispatcher.instance()
        self._ced = CorrectionEventDispatcher.instance()
        self._sed = ShortcutEventDistpacher.instance()
        self._sed.shortcuts = [['KEY_LEFTALT']]

        # handlers
        self._ced.bind(correction_event=correction_event_handler)
        self._sed.bind(shortcut_event=shortcut_event_handler)

    @property
    def user(self):
        return self._user

    @property
    def is_logged_in(self):
        return True if self._user else False

    def build(self):
        self._sm.add_widget(LoginScreen(name=self.LOGIN_SCREEN))
        self._sm.add_widget(RegisterScreen(name=self.REGISTER_SCREEN))
        self._sm.add_widget(HomeScreen(name=self.HOME_SCREEN))
        return self._sm

    def login(self, username, password):
        # check if someone is already logged in
        if self.is_logged_in:
            return False

        # check if user exists
        if not User.objects(username=username).count():
            return False

        self._user = User(username, password)
        self._sm.current = self.HOME_SCREEN
        self._ked.poll_forever()
        return True

    def logout(self):
        if self.is_logged_in:
            self._user = None
        return True

    def register(self, username, password):
        if User.objects(username=username).count():
            return False

        User(username, password).save()
        return True

    def add_corpus(self, path):
        if not self.is_logged_in:
            return False

        if not mimetypes.guess_type(path)[0] == 'text/plain':
            return False

        with open(path, 'r') as f:
            blob = TextBlob(f.read())

        return True

class LoginScreen(Screen):

    username = StringProperty()
    password = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._app = AccipioKeyApp.get_running_app()

    def login(self):
        if self._app.login(self.username, self.password):
            self.ids.ti_username.text = ''
            self.ids.ti_password.text = ''
        else:
            showMessage('Login Failed', 'Invalid credentials, please try again.')

class RegisterScreen(Screen):

    username = StringProperty()
    password1 = StringProperty()
    password2 = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._app = AccipioKeyApp.get_running_app()

    def clear(self):
        self.ids.ti_username.text = ''
        self.ids.ti_password1.text = ''
        self.ids.ti_password2.text = ''

    def finish(self):
        self.clear()
        self.manager.current = self._app.LOGIN_SCREEN

    def register(self):
        # check if username field is empty
        if not self.username:
            showMessage("Empty Field", "Please enter in a username.")
            return

        # check if either password field is empty
        if not self.password1 or not self.password2:
            showMessage('Empty Field', 'Please enter matching passwords.')
            return

        # check if passwords match
        if self.password1 == self.password2:
            if not self._app.register(self.username, self.password1):
                showMessage('Registration Failed', 'Please choose a different username.')
                return
            self.finish()

class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._app = AccipioKeyApp.get_running_app()

    def dismiss_file_modal(self):
        self._file_modal.dismiss()

    def show_file_dialog(self):
        self._file_modal = FileModal(title='Load Corpus',load=self.load, cancel=self.dismiss_file_modal)
        self._file_modal.open()

    def load(self, selections):
        self.dismiss_file_modal();

        invalid_selections = []
        for selection in selections:
            if not self._app.add_corpus(selection):
                invalid_selections.append(selection)

        if not selections:
            showMessage('Invalid Corpora', str(invalid_selections))
