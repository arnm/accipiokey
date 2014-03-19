
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty

class TabTextInput(TextInput):
    """ TabTextInput class.

    Properties:
        'next'
            Specifies object which will inherit focus when tab key is pressed.
    """

    next_widget = ObjectProperty()
    multiline = False

    def _keyboard_on_key_down(self, window, keycode, text, modifiers):

        # check for <TAB> keycode
        if keycode[0] == 9:
            self.next_widget.focus = True
        else:
            super()._keyboard_on_key_down(window, keycode, text, modifiers)

