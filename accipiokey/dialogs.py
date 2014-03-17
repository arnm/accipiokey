
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

class FileDialog(Widget):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
