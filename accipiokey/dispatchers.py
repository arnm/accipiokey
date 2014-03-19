from accipiokey.utils import keycodeToUnicode

from evdev import InputDevice, categorize, ecodes, KeyEvent

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, ListProperty

from select import select
from singleton.singleton import ThreadSafeSingleton


@ThreadSafeSingleton
class KeyboardEventDispatcher(EventDispatcher):

    key_event = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dev = InputDevice('/dev/input/event0')
        self.register_event_type('on_key_event')

    def on_key_event(self, *largs):
        pass

    def poll(self, dt=0):
        r, w, x = select([self._dev], [], [])
        for event in self._dev.read():
            if event.type == ecodes.EV_KEY:
                self.key_event = categorize(event)
                self.dispatch('on_key_event')

@ThreadSafeSingleton
class KeyboardStateEventDispatcher(EventDispatcher):

    active_keys = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_keyboard_state_change')

        # listen
        self._ked = KeyboardEventDispatcher.instance()
        self._ked.bind(on_key_event=self.on_key_event)

    def on_keyboard_state_change(self, *largs):
        pass

    def on_key_event(self, instance):
        keycode = instance.key_event.keycode
        keystate = instance.key_event.keystate

        if keystate == KeyEvent.key_down:
            if keycode not in self.active_keys:
                self.active_keys.append(instance.key_event.keycode)
                self.dispatch('on_keyboard_state_change')
        elif keystate == KeyEvent.key_up:
            if keycode in self.active_keys:
                self.active_keys.remove(instance.key_event.keycode)
                self.dispatch('on_keyboard_state_change')

@ThreadSafeSingleton
class ShortcutEventDistpacher(EventDispatcher):

    shortcut_event = ObjectProperty()
    shortcuts = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # register events
        self.register_event_type('on_shortcut_event')

        # listen
        self._ksd = KeyboardStateEventDispatcher.instance()
        self._ksd.bind(on_keyboard_state_change=self.on_keyboard_state_change)

    def on_shortcut_event(self, *largs):
        print(self.shortcut_event)

    def on_keyboard_state_change(self, instance):
        if instance.active_keys in self.shortcuts:
            self.shortcut_event = instance.active_keys
            self.dispatch('on_shortcut_event')

@ThreadSafeSingleton
class WordEventDispatcher(EventDispatcher):

    word_event = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_word_event')

        # listen
        self._ksd = KeyboardStateEventDispatcher.instance()
        self._ksd.bind(on_keyboard_state_change=self.on_keyboard_state_change)

    def on_word_event(self, *largs):
        pass

    def on_keyboard_state_change(self, instance):
        pass

@ThreadSafeSingleton
class SuggestionEventDispatcher(EventDispatcher):
    suggestion_event = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_suggestion_event')

        # listen
        self._ksd = KeyboardStateEventDispatcher.instance()
        self._ksd.bind(on_keyboard_state_change=self.on_keyboard_state_change)

    def on_suggestion_event(self, *largs):
        pass

    def on_keyboard_state_change(self, instance):
        pass

@ThreadSafeSingleton
class CorrectionEventDispatcher(EventDispatcher):
    correction_event = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_correction_event')

        self._wed = WordEventDispatcher.instance()
        self._wed.bind(on_word_event=self.on_word_event)

    def on_correction_event(self, *largs):
        pass

    def on_word_event(self, instance):
        pass
