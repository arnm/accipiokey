
from accipiokey.screens import LoginScreen, RegisterScreen, MainScreen, CorpusScreen

from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager
from kivy.config import Config

import kivy


kivy.require('1.8.0')
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')

class AccipioKeyApp(App):
    title = 'AccipioKey'

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(CorpusScreen(name='corpus'))

        return sm
