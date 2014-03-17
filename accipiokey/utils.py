from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from accipiokey.dialogs import *

def showMessage(title, message):

    def dismiss():
        popup.dismiss()

    content = MessageDialog(message=message, cancel=dismiss)
    popup = Popup(title=title, content=content)
    popup.open()
