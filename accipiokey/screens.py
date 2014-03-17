from accipiokey.loggers import LinuxEventDistpatcher
from accipiokey.utils import *
from accipiokey.dialogs import FileDialog

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.properties import ObjectProperty

from pymongo import MongoClient


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

    def dismiss_file_dialog(self):
        self._popup.dismiss()

    def show_file_dialog(self):
        content = FileDialog(load=self.load, cancel=self.dismiss_file_dialog)
        self._popup = Popup(title='Load Corpus', content=content)
        self._popup.open()

    def load(self, path, filename):
        print(path, filename)









