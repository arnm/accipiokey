from accipiokey.modals import MessageModal

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from evdev import ecodes, UInput

def show_message(title, message, size=('300dp', '200dp')):

    def dismiss():
        modal.dismiss()

    modal = MessageModal(title=title, size=size, size_hint=(None, None),
        message=message, cancel=dismiss)
    modal.open()

# ToDo: fix this hack
def keycode_to_unicode(keycode):
    return keycode.replace('KEY_', '').lower()

# ToDo: fix this hack
def unicode_to_keycode(unicode):
    if unicode == ' ':
        return 'KEY_' + 'space'.upper()
    return 'KEY_' + unicode.upper()

# ToDo: fix this hack
def emulate_key_events(unicodes):
    for uni in unicodes:
        keycode = unicode_to_keycode(uni)
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

