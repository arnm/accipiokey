import kivy

kivy.require('1.8.0')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.config import Config
from accipiokey.screens import LoginScreen, RegisterScreen, MainScreen, CorpusScreen


class AccipioKeyApp(App):
    title = 'AccipioKey'

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(CorpusScreen(name='corpus'))

        return sm
