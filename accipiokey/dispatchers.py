from evdev import InputDevice, categorize, ecodes

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty

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

    keyboard_state = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_keyboard_state_change')

        # listen
        self._ked = KeyboardStateEventDispatcher.instance()
        self._ked.bind(on_key_event=self.on_key_event)

    def on_keyboard_state_change(self, *largs):
        pass

    def on_key_event(self):
        pass

@ThreadSafeSingleton
class ShortcutEventDistpacher(EventDispatcher):

    shortcut_event = ObjectProperty()

    def __init__(self, shortcuts, **kwargs):
        super().__init__(**kwargs)
        self._shortcuts = shortcuts

        # register events
        self.register_event_type('on_shortcut_event')

        # listen
        self._ksd = KeyboardStateEventDispatcher.instance()
        self._ksd.bind(on_key_event=self.on_keyboard_state_change)

    def on_shortcut_event(self):
        pass

    def on_keyboard_state_change(self, instance):
        pass

@ThreadSafeSingleton
class WordEventDispatcher(EventDispatcher):

    word_event = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_word_event')

        # listen
        self._ked = KeyboardStateEventDispatcher.instance()
        self._ked.bind(on_key_event=self.on_key_event)

    def on_word_event(self):
        pass

    def on_key_event(self, instance):
        pass

@ThreadSafeSingleton
class SuggestionEventDispatcher(EventDispatcher):
    suggestion_event = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_suggestion_event')

        self._ked = KeyboardEventDispatcher.instance()
        self._ked.bind(on_key_event=self.on_key_event)

    def on_suggestion_event(self):
        pass

    def on_key_event(self, instance):
        pass

@ThreadSafeSingleton
class CorrectionEventDispatcher(EventDispatcher):
    correction_event = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_correction_event')

        self._wed = WordEventDispatcher.instance()
        self._wed.bind(on_word_event=self.on_word_event)

    def on_correction_event(self):
        pass

    def on_word_event(self, instance):
        pass
