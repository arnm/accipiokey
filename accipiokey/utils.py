from accipiokey.modals import MessageModal

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from evdev import ecodes, UInput

def showMessage(title, message, size=('300dp', '200dp')):

    def dismiss():
        modal.dismiss()

    modal = MessageModal(title=title, size=size, size_hint=(None, None), message=message, cancel=dismiss)
    modal.open()

def keycodeToUnicode(keycode):
    return keycode.replace('KEY_', '').lower()

def unicodeToKeyCode(unicode):
    if unicode == ' ':
        return 'KEY_' + 'space'.upper()
    return 'KEY_' + unicode.upper()

def emulate_key_events(unicodes):
    for uni in unicodes:
        keycode = unicodeToKeyCode(uni)
        with UInput() as uinput:
            exec('uinput.write(ecodes.EV_KEY, ecodes.' + keycode + ', 1)')
            exec('uinput.write(ecodes.EV_KEY, ecodes.' + keycode + ', 0)')
            uinput.syn()

def find_second_to_last(haystack, needle):
    found = []
    for i, e in enumerate(haystack):
        if e == needle:
            found.append(i)

    if len(found) >= 2:
        return found[-2]
    else:
        return None


