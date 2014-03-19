from evdev import InputDevice, categorize, ecodes

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty

from select import select

class KeyboardEventDispatcher(EventDispatcher):

    key_event = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dev = InputDevice('/dev/input/event0')
        self.register_event_type('on_key_event')

    def on_key_event(self, *largs):
        pass

    def poll_keyboard(self, dt=0):
        r, w, x = select([self._dev], [], [])
        for event in self._dev.read():
            if event.type == ecodes.EV_KEY:
                self.key_event = categorize(event)
                self.dispatch('on_key_event')

