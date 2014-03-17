
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget

class MessageDialog(Widget):
    message = StringProperty()
    cancel = ObjectProperty(None)

class FileDialog(Widget):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
