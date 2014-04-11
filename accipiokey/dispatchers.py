from accipiokey import settings
from accipiokey.apputils import keycode_to_unicode
from accipiokey.mappings import WordMappingType
from datetime import datetime
from elasticutils import S, get_es
from evdev import InputDevice, categorize, ecodes, KeyEvent
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, ListProperty, DictProperty, StringProperty
from select import select
from singleton.singleton import ThreadSafeSingleton
from textblob import TextBlob, Word
from threading import Thread
from time import clock, sleep
import logging


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

@ThreadSafeSingleton
class KeyboardEventDispatcher(EventDispatcher):

    key_event = ObjectProperty()

    def __init__(self, **kwargs):
        EventDispatcher.__init__(self, **kwargs)

        self._dev = InputDevice('/dev/input/event0')
        self._th = None
        self._running = False

    @property
    def running(self):
        return self._running

    def poll(self, dt=0):
        r, w, x = select([self._dev], [], [])
        for event in self._dev.read():
            if event.type == ecodes.EV_KEY:
                self.key_event = categorize(event)

    def poll_forever(self):
        if not self._running:
            settings.HANDLE_EVENTS = True
            self._running = True
            self._th = Thread(target=self._poll_forever)
            self._th.daemon = True
            self._th.start()

    def stop(self):
        self._running = False
        settings.HANDLE_EVENTS = False

    def _poll_forever(self):
        while self._running:
            sleep(0.2)
            self.poll()

@ThreadSafeSingleton
class KeyboardStateEventDispatcher(EventDispatcher):

    keyboard_state = DictProperty()

    def __init__(self, **kwargs):
        EventDispatcher.__init__(self, **kwargs)

        self._ked = KeyboardEventDispatcher.instance()
        self._ked.bind(key_event=self.on_key_event)

    def on_key_event(self, instance, key_event):
        if not settings.HANDLE_EVENTS:
            return

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
class WordEventDispatcher(EventDispatcher):

    last_word_event = StringProperty()
    word_event = StringProperty()
    word_buffer = ListProperty()

    def __init__(self, **kwargs):
        EventDispatcher.__init__(self, **kwargs)

        self._word_delimiter_pressed = False
        self._backspace_pressed = False

        self._ked = KeyboardEventDispatcher.instance()
        self._ked.bind(key_event=self.on_key_event)

        self.bind(word_buffer=self.on_word_buffer)
        self.bind(word_event= lambda i, we:
            logging.info(
                'Last Word (%s) Word Event (%s)',
                self.last_word_event, we))

    def on_word_buffer(self, instance, word_buffer):
        if not settings.HANDLE_EVENTS:
            return

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
        if not settings.HANDLE_EVENTS:
            return

        keycode = key_event.keycode
        keystate = key_event.keystate

        if keystate == KeyEvent.key_down or keystate == KeyEvent.key_hold:
            string = keycode_to_unicode(keycode)
            if len(string) == 1:
                self.word_buffer.append(string)
            elif string == 'space':
                self._word_delimiter_pressed = True
                self.word_buffer.append(' ')
            elif string == 'enter':
                self._word_delimiter_pressed = True
                self.word_buffer.append(' ')
            elif string == 'tab':
                self._word_delimiter_pressed = True
                self.word_buffer.append(' ')
            elif string == 'backspace' and self.word_buffer:
                self._backspace_pressed = True
                del self.word_buffer[-1]

@ThreadSafeSingleton
class ShortcutEventDistpacher(EventDispatcher):

    shortcut_event = DictProperty()

    def __init__(self, shortcuts=[], **kwargs):
        EventDispatcher.__init__(self, **kwargs)

        from accipiokey import AccipioKeyApp
        self._app = AccipioKeyApp.get_running_app()

        self._ksd = KeyboardStateEventDispatcher.instance()
        self._ksd.bind(keyboard_state=self.on_keyboard_state_change)

        self.bind(shortcut_event=lambda i, se:
            logging.info('Shortcut Event: (%s)', se))

    def on_keyboard_state_change(self, instance, keyboard_state):
        if not settings.HANDLE_EVENTS:
            return

        for name, shortcut in self._app.user.shortcuts.iteritems():
            if sorted(keyboard_state.keys()) == sorted(shortcut):
                self.shortcut_event = {name: shortcut}

@ThreadSafeSingleton
class CompletionEventDispatcher(EventDispatcher):

    completion_event = StringProperty()
    possible_completion_event = StringProperty()

    @classmethod
    def get_shortcut(cls):
        return 'completion'

    def __init__(self, shortcut=None, **kwargs):
        EventDispatcher.__init__(self, **kwargs)

        from accipiokey import AccipioKeyApp
        self._app = AccipioKeyApp.get_running_app()

        self._sed = ShortcutEventDistpacher.instance()
        self._wed = WordEventDispatcher.instance()

        self._sed.bind(shortcut_event=self.on_shortcut_event)
        self._wed.bind(word_event=self.on_word_event)

        self.bind(completion_event=lambda i, ce:
            logging.info('Completion Event (%s)', ce))

    def on_shortcut_event(self, instance, shortcut_event):
        if not settings.HANDLE_EVENTS:
            return

        if not self.get_shortcut() in shortcut_event:
            return

        if not self.possible_completion_event:
            return

        self.completion_event = self.possible_completion_event

    def on_word_event(self, instance, word_event):
        if not settings.HANDLE_EVENTS:
            return

        suggestion_name = 'completion_suggestion'
        compl_resp = get_es().suggest(index=WordMappingType.get_index(),
            body={
                suggestion_name: {
                    'text': word_event,
                    'completion': {
                        'field': 'text'
                    }
                }
            })
        suggestions = compl_resp[suggestion_name][0]['options']
        if suggestions:
            top_suggestion = suggestions[0]['text']
            self.possible_completion_event = top_suggestion
        else:
            self.possible_completion_event = ''

@ThreadSafeSingleton
class CorrectionEventDispatcher(EventDispatcher):

    correction_event = StringProperty()

    def __init__(self, **kwargs):
        EventDispatcher.__init__(self, **kwargs)

        from accipiokey import AccipioKeyApp
        self._app = AccipioKeyApp.get_running_app()

        self._wed = WordEventDispatcher.instance()
        self._wed.bind(last_word_event=self.on_last_word_event)

        self.bind(correction_event=lambda i, ce:
            logging.info('Correction Event: (%s)', ce))

    def on_last_word_event(self, instance, last_word_event):
        if not settings.HANDLE_EVENTS:
            return

        searcher = S(WordMappingType)
        # check if word is already indexed
        word_search_result = searcher.query(
            user__term=str(self._app.user.id),
            text__term=str(last_word_event),
            must=True)

        if word_search_result.count():
            for r in word_search_result:
                print('RESULT:', (r.text, r.user))
            return

        print('NOT INDEXED:', last_word_event)
        # get suggestion for unknown word
        suggestion_name = 'correction_suggestion'
        suggest_query = searcher.suggest(
            suggestion_name,
            last_word_event,
            field='text')
        suggestions = suggest_query.suggestions()[suggestion_name][0]['options']

        if not suggestions:
            return

        # correct last word if necessary
        top_suggestion = suggestions[0]['text']
        self.correction_event = top_suggestion

@ThreadSafeSingleton
class SnippetEventDispatcher(EventDispatcher):

    snippet_event = DictProperty()

    @classmethod
    def get_shortcut(cls):
        return 'snippet'

    def __init__(self, **kwargs):
        EventDispatcher.__init__(self, **kwargs)

        from accipiokey import AccipioKeyApp
        self._app = AccipioKeyApp.get_running_app()

        self._sed = ShortcutEventDistpacher.instance()
        self._sed.bind(shortcut_event=self.on_shortcut_event)

        self.bind(snippet_event=lambda i, se:
            logging.info('Snippet Event: (%s)', se))

    def on_shortcut_event(self, instance, shortcut_event):
        if not settings.HANDLE_EVENTS:
            return

        if not self.get_shortcut() in shortcut_event:
            return

        snippet = str(WordEventDispatcher.instance().word_event)
        if snippet in self._app.user.snippets:
            self.snippet_event = {snippet: self._app.user.snippets[snippet]}
