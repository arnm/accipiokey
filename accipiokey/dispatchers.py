from accipiokey.utils import keycodeToUnicode
from datetime import datetime
from evdev import InputDevice, categorize, ecodes, KeyEvent
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, ListProperty, DictProperty, StringProperty
from select import select
from singleton.singleton import ThreadSafeSingleton
from textblob import TextBlob, Word
from threading import Thread
from time import clock, sleep


@ThreadSafeSingleton
class KeyboardEventDispatcher(EventDispatcher):

    key_event = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dev = InputDevice('/dev/input/event0')
        self._th = None

    def poll(self, dt=0):
        r, w, x = select([self._dev], [], [])
        for event in self._dev.read():
            if event.type == ecodes.EV_KEY:
                self.key_event = categorize(event)

    def poll_forever(self):
        self._th = Thread(target=self._poll_forever)
        self._th.daemon = True
        self._th.start()

    def _poll_forever(self):
        while 1:
            sleep(0.2)
            self.poll()

@ThreadSafeSingleton
class KeyboardStateEventDispatcher(EventDispatcher):

    keyboard_state = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._ked = KeyboardEventDispatcher.instance()
        self._ked.bind(key_event=self.on_key_event)

    def on_key_event(self, instance, key_event):
        keycode = key_event.keycode
        keystate = key_event.keystate
        timestamp = clock()

        if keystate == KeyEvent.key_down or keystate == KeyEvent.key_hold:
            if keycode not in self.keyboard_state:
                self.keyboard_state[keycode] = timestamp
        elif keystate == KeyEvent.key_up:
            if keycode in self.keyboard_state:
                del self.keyboard_state[keycode]

@ThreadSafeSingleton
class ShortcutEventDistpacher(EventDispatcher):

    shortcut_event = DictProperty()
    shortcuts = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._ksd = KeyboardStateEventDispatcher.instance()
        self._ksd.bind(keyboard_state=self.on_keyboard_state_change)

    def on_keyboard_state_change(self, instance, keyboard_state):
        if keyboard_state in self.shortcuts:
            self.shortcut_event = keyboard_state

@ThreadSafeSingleton
class WordEventDispatcher(EventDispatcher):

    last_word_event = StringProperty()
    word_event = StringProperty()
    word_buffer = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._word_delimiter_pressed = False
        self._backspace_pressed = False

        self._ked = KeyboardEventDispatcher.instance()
        self._ked.bind(key_event=self.on_key_event)

        self.bind(word_buffer=self.on_word_buffer)
        self.bind(word_event= lambda i, we: print('Word Event:', we, 'Last Word:', self.last_word_event))

    def on_word_buffer(self, instance, word_buffer):
        word_list = TextBlob(''.join(word_buffer)).words

        if word_list:

            if self._backspace_pressed and not self.word_buffer[-1].strip():
                self.last_word_event = word_list[-1]
                self.word_event = ''
                self._backspace_pressed = False
                return

            if self._word_delimiter_pressed:
                self.last_word_event = word_list[-1]
                self.word_event = ''
                self._word_delimiter_pressed = False
                return

            if len(word_list) >= 2:
                self.last_word_event = word_list[-2]
            elif self.last_word_event:
                self.last_word_event = ''

            self.word_event = word_list[-1]

        else:
            self.last_word_event = ''

    def on_key_event(self, instance, key_event):
        keycode = key_event.keycode
        keystate = key_event.keystate

        if keystate == KeyEvent.key_down or keystate == KeyEvent.key_hold:
            string = keycodeToUnicode(keycode)
            if len(string) == 1:
                self.word_buffer.append(string)
            elif string == 'space':
                self._word_delimiter_pressed = True
                self.word_buffer.append(' ')
            elif string == 'enter':
                self._word_delimiter_pressed = True
                self.word_buffer.append('\n')
            elif string == 'tab':
                self._word_delimiter_pressed = True
                self.word_buffer.append('\t')
            elif string == 'backspace' and self.word_buffer:
                self._backspace_pressed = True
                del self.word_buffer[-1]

@ThreadSafeSingleton
class SuggestionEventDispatcher(EventDispatcher):

    suggestion_event = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._ksd = WordEventDispatcher.instance()
        self._ksd.bind(word_event=self.on_word_event)

    def on_word_event(self, instance, word_event):
        print('\nWord Event:', word_event)

@ThreadSafeSingleton
class CorrectionEventDispatcher(EventDispatcher):

    correction_event = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._wed = WordEventDispatcher.instance()
        self._wed.bind(last_word_event=self.on_last_word_event)

        self.bind(correction_event= lambda i, ce: print('Correction Event:', ce))

    def on_last_word_event(self, instance, last_word_event):
        correction_list = Word(last_word_event).spellcheck()
        if correction_list:
            correction = correction_list[0][0]
            self.correction_event = correction
