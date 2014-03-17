
from accipiokey.dialogs import FileDialog
from accipiokey.loggers import LinuxEventDistpatcher
from accipiokey.utils import *

from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

import mimetypes
from pymongo import MongoClient
from textblob import TextBlob

# establish mongodb connection
client = MongoClient()
db = client.accipiokey

# shared screen data
current_user = None

class LoginScreen(Screen):

    def login(self):
        users = db.accipiokey_users

        username = self.ids.ti_username.text
        password = self.ids.ti_password.text

        user = {'username': username, 'password': password}

        if not users.find(user).count():
            showMessage('', 'Invalid login credentials')
            return

        current_user = user
        self.manager.current = 'main'
        self.ids.ti_username.text = ''
        self.ids.ti_password.text = ''

class RegisterScreen(Screen):

    def register(self):

        users = db.accipiokey_users

        # get registration fields
        username = self.ids.ti_username.text
        password1 = self.ids.ti_password1.text
        password2 = self.ids.ti_password2.text

        # check if username field is empty
        if not username:
            showMessage("Empty Field", "Please enter in a user name.")
            return

        # check if either password field is empty
        if not password1 or not password2:
            showMessage('Empty Field', 'Please enter matching passwords.')
            return

        # check if passwords match
        if password1 == password2:
            # create user
            user = {
                'username': username,
            }

            # check if user is already registered
            if not users.find(user).count():
                # insert into db
                user['password'] = password1
                users.insert(user)
                self.manager.current = 'login'
                self.ids.ti_username.text = ''
                self.ids.ti_password1.text = ''
                self.ids.ti_password2.text = ''
                return
            else:
                # user already registered
                showMessage('Ivalid User Name', 'User name is already registered.')
                return
        else:
            # passwords do not match
            showMessage('Mismatched Passwords', 'Please enter matching passwords.')
            return


class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def logout(self):
        current_user = None
        self.manager.current = 'login'


class CorpusScreen(Screen):

    def __init__(self, **kwargs):
        super(CorpusScreen, self).__init__(**kwargs)
        self._corpora = []
        self._popup = None

    def dismiss_file_dialog(self):
        self._popup.dismiss()

    def show_file_dialog(self):
        content = FileDialog(load=self.load, cancel=self.dismiss_file_dialog)
        self._popup = Popup(title='Load Corpus', content=content)
        self._popup.open()

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
