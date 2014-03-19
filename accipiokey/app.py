
from accipiokey.screens import LoginScreen, RegisterScreen, HomeScreen, CorporaScreen

from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager
from kivy.config import Config

import kivy


kivy.require('1.8.0')

class AccipioKeyApp(App):
    title = 'AccipioKey'

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(CorporaScreen(name='corpora'))

        return sm
