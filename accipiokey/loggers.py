from abc import ABCMeta, abstractmethod
from singleton.singleton import ThreadSafeSingleton
import threading
from kivy.event import EventDispatcher

class BaseLogger(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        self._thread = None

    @abstractmethod
    def _fetch_keys(self):
        pass

    @abstractmethod
    def log_forever(self):
        pass

    def log_start(self):
        if self._thread is not None:
            raise Exception('Thread Already Running')

        self._thread = threading.Thread(target=self._thread_main)
        self._thread.daemon = True
        self._thread.start()

    def _thread_main(self):
        self.log_forever()

@ThreadSafeSingleton
class LinuxLogger(BaseLogger):

    import sys
    import ctypes as ct
    from ctypes.util import find_library

    assert("linux" in sys.platform)

    x11 = ct.cdll.LoadLibrary(find_library("X11"))
    display = x11.XOpenDisplay(None)

    # this will hold the self.keyboard state.  32 bytes, with each
    # bit representing the state for a single key.
    keyboard = (ct.c_char * 32)()

    # these are the locations (byte, byte value) of special
    # keys to watch
    shift_keys = ((6,4), (7,64))
    modifiers = {
        "left shift": (6,4),
        "right shift": (7,64),
        "left ctrl": (4,32),
        "right ctrl": (13,2),
        "left alt": (8,1),
        "right alt": (13,16)
    }
    last_pressed = set()
    last_pressed_adjusted = set()
    last_modifier_state = {}
    caps_lock_state = 0

    # key is byte number, value is a dictionary whose
    # keys are values for that byte, and values are the
    # keys corresponding to those byte values
    key_mapping = {
        1: {
            0b00000010: "<esc>",
            0b00000100: ("1", "!"),
            0b00001000: ("2", "@"),
            0b00010000: ("3", "#"),
            0b00100000: ("4", "$"),
            0b01000000: ("5", "%"),
            0b10000000: ("6", "^"),
        },
        2: {
            0b00000001: ("7", "&"),
            0b00000010: ("8", "*"),
            0b00000100: ("9", "("),
            0b00001000: ("0", ")"),
            0b00010000: ("-", "_"),
            0b00100000: ("=", "+"),
            0b01000000: "<backspace>",
            0b10000000: "<tab>",
        },
        3: {
            0b00000001: ("q", "Q"),
            0b00000010: ("w", "W"),
            0b00000100: ("e", "E"),
            0b00001000: ("r", "R"),
            0b00010000: ("t", "T"),
            0b00100000: ("y", "Y"),
            0b01000000: ("u", "U"),
            0b10000000: ("i", "I"),
        },
        4: {
            0b00000001: ("o", "O"),
            0b00000010: ("p", "P"),
            0b00000100: ("[", "{"),
            0b00001000: ("]", "}"),
            0b00010000: "<enter>",
            #0b00100000: "<left ctrl>",
            0b01000000: ("a", "A"),
            0b10000000: ("s", "S"),
        },
        5: {
            0b00000001: ("d", "D"),
            0b00000010: ("f", "F"),
            0b00000100: ("g", "G"),
            0b00001000: ("h", "H"),
            0b00010000: ("j", "J"),
            0b00100000: ("k", "K"),
            0b01000000: ("l", "L"),
            0b10000000: (";", ":"),
        },
        6: {
            0b00000001: ("'", "\""),
            0b00000010: ("`", "~"),
            #0b00000100: "<left shift>",
            0b00001000: ("\\", "|"),
            0b00010000: ("z", "Z"),
            0b00100000: ("x", "X"),
            0b01000000: ("c", "C"),
            0b10000000: ("v", "V"),
        },
        7: {
            0b00000001: ("b", "B"),
            0b00000010: ("n", "N"),
            0b00000100: ("m", "M"),
            0b00001000: (",", "<"),
            0b00010000: (".", ">"),
            0b00100000: ("/", "?"),
            #0b01000000: "<right shift>",
        },
        8: {
            #0b00000001: "<left alt>",
            0b00000010: " ",
            0b00000100: "<caps lock>",
        },
        13: {
            #0b00000010: "<right ctrl>",
            #0b00010000: "<right alt>",
        },
    }

    def __init__(self):
        BaseLogger.__init__(self)

    def _fetch_keys_raw(self):
        self.x11.XQueryKeymap(self.display, self.keyboard)
        return self.keyboard

    def _fetch_keys(self):
        keypresses_raw = self._fetch_keys_raw()

        # check modifier states (ctrl, alt, shift keys)
        modifier_state = {}
        for mod, (i, byte) in self.modifiers.items():
            modifier_state[mod] = bool(ord(keypresses_raw[i]) & byte)

        # shift pressed?
        shift = 0
        for i, byte in self.shift_keys:
            if ord(keypresses_raw[i]) & byte:
                shift = 1
                break

        # caps lock state
        if ord(keypresses_raw[8]) & 4: self.caps_lock_state = int(not self.caps_lock_state)

        # aggregate the pressed keys
        pressed = []
        for i, k in enumerate(keypresses_raw):
            o = ord(k)
            if o:
                for byte,key in self.key_mapping.get(i, {}).items():
                    if byte & o:
                        if isinstance(key, tuple): key = key[shift or self.caps_lock_state]
                        pressed.append(key)

        tmp = pressed
        pressed = list(set(pressed).difference(self.last_pressed))
        state_changed = tmp != self.last_pressed and (pressed or self.last_pressed_adjusted)
        self.last_pressed = tmp
        self.last_pressed_adjusted = pressed

        if pressed: pressed = pressed[0]
        else: pressed = None

        state_changed = self.last_modifier_state and (state_changed or modifier_state != self.last_modifier_state)
        self.last_modifier_state = modifier_state

        return state_changed, modifier_state, pressed

    def log_forever(self):
        from time import sleep, time
        while True:
            sleep(.005)
            changed, modifiers, keys = self._fetch_keys()
            if changed: print("%.2f   %r   %r" % (time(), modifiers, keys))

@ThreadSafeSingleton
class WindowsLogger(BaseLogger):

    def __init__(self):
        WindowsLogger.__init__(self)

    def _fetch_keys():
        pass

    def log_forever():
        pass


@ThreadSafeSingleton
class LinuxEventDistpatcher(EventDispatcher):

    def __init__(self, **kwargs):

        import sys
        import ctypes as ct
        from ctypes.util import find_library

        assert("linux" in sys.platform)

        self._x11 = ct.cdll.LoadLibrary(find_library("X11"))
        self._display = self._x11.XOpenDisplay(None)

        # this will hold the self.keyboard state.  32 bytes, with each
        # bit representing the state for a single key.
        self._keyboard = (ct.c_char * 32)()

        # these are the locations (byte, byte value) of special
        # keys to watch
        self._shift_keys = ((6,4), (7,64))
        self._modifiers = {
            "left shift": (6,4),
            "right shift": (7,64),
            "left ctrl": (4,32),
            "right ctrl": (13,2),
            "left alt": (8,1),
            "right alt": (13,16)
        }
        self._last_pressed = set()
        self._last_pressed_adjusted = set()
        self._last_modifier_state = {}
        self._caps_lock_state = 0

        # key is byte number, value is a dictionary whose
        # keys are values for that byte, and values are the
        # keys corresponding to those byte values
        self._key_mapping = {
            1: {
                0b00000010: "<esc>",
                0b00000100: ("1", "!"),
                0b00001000: ("2", "@"),
                0b00010000: ("3", "#"),
                0b00100000: ("4", "$"),
                0b01000000: ("5", "%"),
                0b10000000: ("6", "^"),
            },
            2: {
                0b00000001: ("7", "&"),
                0b00000010: ("8", "*"),
                0b00000100: ("9", "("),
                0b00001000: ("0", ")"),
                0b00010000: ("-", "_"),
                0b00100000: ("=", "+"),
                0b01000000: "<backspace>",
                0b10000000: "<tab>",
            },
            3: {
                0b00000001: ("q", "Q"),
                0b00000010: ("w", "W"),
                0b00000100: ("e", "E"),
                0b00001000: ("r", "R"),
                0b00010000: ("t", "T"),
                0b00100000: ("y", "Y"),
                0b01000000: ("u", "U"),
                0b10000000: ("i", "I"),
            },
            4: {
                0b00000001: ("o", "O"),
                0b00000010: ("p", "P"),
                0b00000100: ("[", "{"),
                0b00001000: ("]", "}"),
                0b00010000: "<enter>",
                0b01000000: ("a", "A"),
                0b10000000: ("s", "S"),
            },
            5: {
                0b00000001: ("d", "D"),
                0b00000010: ("f", "F"),
                0b00000100: ("g", "G"),
                0b00001000: ("h", "H"),
                0b00010000: ("j", "J"),
                0b00100000: ("k", "K"),
                0b01000000: ("l", "L"),
                0b10000000: (";", ":"),
            },
            6: {
                0b00000001: ("'", "\""),
                0b00000010: ("`", "~"),
                0b00001000: ("\\", "|"),
                0b00010000: ("z", "Z"),
                0b00100000: ("x", "X"),
                0b01000000: ("c", "C"),
                0b10000000: ("v", "V"),
            },
            7: {
                0b00000001: ("b", "B"),
                0b00000010: ("n", "N"),
                0b00000100: ("m", "M"),
                0b00001000: (",", "<"),
                0b00010000: (".", ">"),
                0b00100000: ("/", "?"),
            },
            8: {
                0b00000010: " ",
                0b00000100: "<caps lock>",
            }
        }

        self.register_event_type('on_keyboard_state_change')

    def on_keyboard_state_change(self, *args):
        pass

    def _fetch_keys_raw(self):
        self._x11.XQueryKeymap(self._display, self._keyboard)
        return self._keyboard

    def fetch_keys(self, *args):
        keypresses_raw = self._fetch_keys_raw()

        # check modifier states (ctrl, alt, shift keys)
        modifier_state = {}
        for mod, (i, byte) in self._modifiers.items():
            modifier_state[mod] = bool(ord(keypresses_raw[i]) & byte)

        # shift pressed?
        shift = 0
        for i, byte in self._shift_keys:
            if ord(keypresses_raw[i]) & byte:
                shift = 1
                break

        # caps lock state
        if ord(keypresses_raw[8]) & 4: self._caps_lock_state = int(not self._caps_lock_state)

        # aggregate the pressed keys
        pressed = []
        for i, k in enumerate(keypresses_raw):
            o = ord(k)
            if o:
                for byte,key in self._key_mapping.get(i, {}).items():
                    if byte & o:
                        if isinstance(key, tuple): key = key[shift or self._caps_lock_state]
                        pressed.append(key)

        tmp = pressed
        pressed = list(set(pressed).difference(self._last_pressed))
        state_changed = tmp != self._last_pressed and (pressed or self._last_pressed_adjusted)
        self._last_pressed = tmp
        self._last_pressed_adjusted = pressed

        if pressed: pressed = pressed[0]
        else: pressed = None

        state_changed = self._last_modifier_state and (state_changed or modifier_state != self._last_modifier_state)
        self._last_modifier_state = modifier_state

        if state_changed:
            self.dispatch('on_keyboard_state_change', (modifier_state, pressed))

        return (state_changed, modifier_state, pressed)
