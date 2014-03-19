from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from accipiokey.modals import MessageModal

def showMessage(title, message, size=('300dp', '200dp')):

    def dismiss():
        modal.dismiss()

    modal = MessageModal(title=title, size=size, size_hint=(None, None), message=message, cancel=dismiss)
    modal.open()
