from accipiokey.loggers import LinuexEventDistpatcher

from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from pymongo import MongoClient


# establish mongodb connection
client = MongoClient()
db = client.accipiokey

class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self._logger = LinuexEventDistpatcher.instance()
        self._logger.bind(on_keyboard_state_change=self.callback)

        Clock.schedule_interval(self._logger.fetch_keys, 1 / 30.0)

    def callback(self, instance, value):
        self.ids.lb_simple.text = str(value)

class LoginScreen(Screen):

    def login(self):
        pass

class RegisterScreen(Screen):

    def register(self):

        users = db.accipiokey_users

        # get registration fields
        username = self.ids.ti_username.text
        password1 = self.ids.ti_password1.text
        password2 = self.ids.ti_password2.text

        # check if username field is empty
        if not username:
            popup = Popup(title='Empty User Name',
                content=Label(text='Please enter in a user name.'),
                size_hint=(None, None),
                size=(300, 300))
            popup.open()
            return

        # check if either password field is empty
        if not password1 or not password2:
            popup = Popup(title='Empty Password',
                content=Label(text='Please enter matching passwords.'),
                size_hint=(None, None),
                size=(300, 300))
            popup.open()
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
            else:
                # user already registered
                popup = Popup(title='Invalid User Name',
                    content=Label(text='User is already registered'),
                    size_hint=(None, None),
                    size=(300, 300))
                popup.open()
                return
        else:
            # passwords do not match
            popup = Popup(title='Mismatched Password',
                content=Label(text='Please enter matching passwords.'),
                size_hint=(None, None),
                size=(300, 300))
            popup.open()
            return






