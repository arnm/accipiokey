from evdev import InputDevice, categorize, ecodes

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty

from select import select
from singleton.singleton import ThreadSafeSingleton

class MouseEventDispatcher(EventDispatcher):

    mouse_event = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dev = InputDevice('/dev/input/event11')
        self.register_event_type('on_mouse_event')

    def on_mouse_event(self):
        pass

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
class ShortcutEventDistpacher(EventDispatcher):

    shortcut_event = ObjectProperty()

    def __init__(self, shortcuts, **kwargs):
        super().__init__(**kwargs)
        self._shortcuts = shortcuts

        # register events
        self.register_event_type('on_shortcut_event')

        # listen
        self._ked = KeyboardEventDispatcher.instance()
        self._ked.bind(on_key_event=self.on_key_event_callback)

    def on_shortcut_event(self):
        pass

    def on_key_event_callback(self, instance):
        pass

@ThreadSafeSingleton
class WordEventDispatcher(EventDispatcher):

    word_event = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_word_event')

        self._ked = KeyboardEventDispatcher.instance()
        self._ked.bind(on_key_event=self.on_key_event_callback)

    def on_word_event(self):
        pass

    def on_key_event_callback(self, instance):
        pass

@ThreadSafeSingleton
class SuggestionEventDispatcher(EventDispatcher):
    suggestion_event = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_suggestion_event')

        self._ked = KeyboardEventDispatcher.instance()
        self._ked.bind(on_key_event=self.on_key_event_callback)

    def on_suggestion_event(self):
        pass

    def on_key_event_callback(self, instance):
        pass

@ThreadSafeSingleton
class CorrectionEventDispatcher(EventDispatcher):
    correction_event = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_correction_event')

        self._wed = WordEventDispatcher.instance()
        self._wed.bind(on_word_event=self.on_word_event_callback)

    def on_correction_event(self):
        pass

    def on_word_event_callback(self, instance):
        pass
