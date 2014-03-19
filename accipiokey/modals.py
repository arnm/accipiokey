
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup

class MessageModal(Popup):
    message = StringProperty()
    cancel = ObjectProperty()

class FileModal(Popup):
    load = ObjectProperty()
    cancel = ObjectProperty()
