from accipiokey.modals import FileModal
from accipiokey.widgets import *
from accipiokey.loggers import LinuxEventDistpatcher
from accipiokey.utils import *
from accipiokey.database import *

from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

import mimetypes
from textblob import TextBlob

# shared screen data
current_user = None

class LoginScreen(Screen):

    username = StringProperty()
    password = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def login(self):
        users = db.accipiokey_users
        [print(user) for user in users.find()]
        user = {'username': self.username, 'password': self.password}

        if not users.find(user).count():
            showMessage('Invalid credentials', 'Please try again.')
            return

        current_user = user
        self.manager.current = 'home'
        self.ids.ti_username.text = ''
        self.ids.ti_password.text = ''

class RegisterScreen(Screen):

    username = StringProperty()
    password1 = StringProperty()
    password2 = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def clear(self):
        self.ids.ti_username.text = ''
        self.ids.ti_password1.text = ''
        self.ids.ti_password2.text = ''

    def finish(self):
        self.clear()
        self.manager.current = 'login'

    def register(self):

        users = db.accipiokey_users

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
            # create user
            user = {
                'username': self.username,
            }

            # check if user is already registered
            if not users.find(user).count():
                # insert into db
                user['password'] = self.password1
                users.insert(user)
                self.finish()
                return
            else:
                # user already registered
                showMessage('Invalid Username', 'Username is already registered.')
                return
        else:
            # passwords do not match
            showMessage('Mismatched Passwords', 'Please enter matching passwords.')
            return


class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def logout(self):
        current_user = None
        self.manager.current = 'login'

class CorporaScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._corpora = []

    def show_file_dialog(self):
        def dismiss():
            modal.dismiss()

        modal = FileModal(title='Load Corpus',load=self.load, cancel=dismiss)
        modal.open()

    def load(self, selections):
        self.dismiss_file_dialog()

        invalid_selections = []

        # iterate each selection
        for corpus in selections:
            # try to open file
            try:
                f = open(corpus, 'r')
            except TypeError:
                # can't open file, continue with the rest
                invalid_selections.append(corpus)
                continue
            else:
                # opened file
                with f:
                    # check if plain text
                    if not mimetypes.guess_type(corpus)[0] == 'text/plain':
                        # unsupported file type
                        invalid_selections.append(corpus)
                        continue

                    # read and add to corpora
                    corpus_text = f.read()
                    self._corpora.append(corpus_text)

        for corpus in self._corpora:
            print(corpus)

        # notify user of errors
        if len(invalid_selections):
            showMessage('Unsupported Corpora', str(invalid_selections))
