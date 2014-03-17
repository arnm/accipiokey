from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

def showMessage(title, message, size=(300, 300)):
    gl = GridLayout()
    gl.rows = 2

    lb_msg = Label(text=message)
    btn_close = Button(text='Ok')

    gl.add_widget(lb_msg)
    gl.add_widget(btn_close)

    popup = Popup(title=title,
                content=gl,
                size_hint=(None, None),
                size=size)

    btn_close.bind(on_press=popup.dismiss)
    popup.open()
