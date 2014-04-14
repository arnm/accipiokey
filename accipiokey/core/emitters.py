from accipiokey.core import settings
from accipiokey.core.apputils import keycode_to_unicode, check_if_indexed
from accipiokey.core.logger import Logger
from accipiokey.core.mappings import WordMappingType
from datetime import datetime
from elasticutils import S, get_es
from evdev import InputDevice, categorize, ecodes, KeyEvent
from PySide.QtCore import QObject, Signal, Slot
from select import select
from singleton.singleton import ThreadSafeSingleton
from textblob import TextBlob, Word
from threading import Thread
from time import clock, sleep


@ThreadSafeSingleton
class KeySignalEmitter(QObject):

    key_signal = Signal(object)

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self._dev = InputDevice('/dev/input/event0')
        self._running = False

        # debug statements
        # self.key_signal.connect(
        #     lambda ks: Logger.debug('KeySignalEmitter: Key Signal (%s)', ks))

    @property
    def running(self):
        return self._running

    def poll(self):
        r, w, x = select([self._dev], [], [])
        for event in self._dev.read():
            if event.type == ecodes.EV_KEY:
                self.key_signal.emit(categorize(event))

    # TODO: this is probably completely wrong but it kinda works
    def poll_forever(self):
        if not self._running:
            thread = Thread(target=self._poll_forever)
            thread.daemon = True
            self._running = True
            thread.start()

    def stop(self):
        self._running = False

    def _poll_forever(self):
        while self._running:
            sleep(0.2)
            self.poll()

@ThreadSafeSingleton
class KeyboardStateSignalEmitter(QObject):

    keyboard_state_signal = Signal(dict)

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self._keyboard_state = {}

        # connect signals to handlers
        KeySignalEmitter.instance().key_signal.connect(self.on_key_signal)

        # debug statements
        # self.keyboard_state_signal.connect(
        #     lambda kbs: Logger.debug(
        #         'KeyBoardStateSignalEmitter: Keyboard State (%s)', kbs))

    @Slot(object)
    def on_key_signal(self, key_signal):
        keycode = key_signal.keycode
        keystate = key_signal.keystate
        timestamp = clock()

        if keystate == KeyEvent.key_down or keystate == KeyEvent.key_hold:
            if keycode not in self._keyboard_state:
                self._keyboard_state[keycode] = timestamp
                self.keyboard_state_signal.emit(self._keyboard_state)
        elif keystate == KeyEvent.key_up:
            if keycode in self._keyboard_state:
                del self._keyboard_state[keycode]
                self.keyboard_state_signal.emit(self._keyboard_state)

@ThreadSafeSingleton
class WordSignalEmitter(QObject):

    current_word_signal = Signal(str)
    last_word_signal = Signal(str)
    word_buffer_signal = Signal(list)
    indexed_word_signal = Signal(str)
    user = None

    current_word = ''
    last_word = ''
    word_buffer = []

    def __init__(self, **kwargs):
        QObject.__init__(self, **kwargs)

        self._word_delimiter_pressed = False
        self._backspace_pressed = False

        KeySignalEmitter.instance().key_signal.connect(self.on_key_signal)
        self.word_buffer_signal.connect(self.on_word_buffer_signal)

        self.current_word_signal.connect(lambda cws:
            Logger.info(
                'WordSignalEmitter: Last Word (%s) Word Event (%s)',
                self.last_word, cws))

    # TODO: verify this is correct
    @Slot(list)
    def on_word_buffer_signal(self, word_buffer):

        word_list = TextBlob(''.join(word_buffer)).words

        # check words have been typed
        if word_list:
            # if backspace was pressed and last key typed was whitespace
            if self._backspace_pressed and not self.word_buffer[-1].strip():
                self.last_word = word_list[-1]
                self.current_word = ''
                self._backspace_pressed = False

                self.last_word_signal.emit(self.last_word)
                self.current_word_signal.emit(self.current_word)
                return

            # TODO: first word typed in buffer does not emitt indexed signal
            if self._word_delimiter_pressed:
                self.last_word = word_list[-1]
                self.current_word = ''
                self._word_delimiter_pressed = False

                self.last_word_signal.emit(self.last_word)
                self.current_word_signal.emit(self.current_word)

                if check_if_indexed(self.user, self.last_word):
                    self.indexed_word_signal.emit(self.last_word)

                return

            # append current key to current word
            if len(word_list) >= 2:
                self.last_word = word_list[-2]
                self.last_word_signal.emit(self.last_word)
            elif self.last_word:
                self.last_word = ''
            self.current_word = word_list[-1]
            self.current_word_signal.emit(self.current_word)
        else:
            self.last_word = ''

    @Slot(object)
    def on_key_signal(self, key_signal):

        keycode = key_signal.keycode
        keystate = key_signal.keystate

        if keystate == KeyEvent.key_down or keystate == KeyEvent.key_hold:
            string = keycode_to_unicode(keycode)
            if len(string) == 1:
                self.word_buffer.append(string)
                self.word_buffer_signal.emit(self.word_buffer)
            elif string == 'space':
                self._word_delimiter_pressed = True
                self.word_buffer.append(' ')
                self.word_buffer_signal.emit(self.word_buffer)
            elif string == 'enter':
                self._word_delimiter_pressed = True
                self.word_buffer.append(' ')
                self.word_buffer_signal.emit(self.word_buffer)
            elif string == 'tab':
                self._word_delimiter_pressed = True
                self.word_buffer.append(' ')
                self.word_buffer_signal.emit(self.word_buffer)
            elif string == 'backspace':
                if self.word_buffer:
                    self._backspace_pressed = True
                    del self.word_buffer[-1]
                    self.word_buffer_signal.emit(self.word_buffer)

# TODO: review this
@ThreadSafeSingleton
class ShortcutSignalEmitter(QObject):

    shortcut_signal = Signal(dict)
    user = None

    def __init__(self, **kwargs):
        QObject.__init__(self, **kwargs)

        KeyboardStateSignalEmitter.instance().keyboard_state_signal.connect(
            self.on_keyboard_state_signal)

        self.shortcut_signal.connect(lambda ss:
            Logger.info('ShortcutEventDispatcher: Shortcut Event(%s)', ss))

    @Slot(dict)
    def on_keyboard_state_signal(self, keyboard_state_signal):
        for name, shortcut in self.user.shortcuts.iteritems():
            if keyboard_state_signal.keys() == shortcut:
                self.shortcut_signal.emit({name: shortcut})
                break

@ThreadSafeSingleton
class CompletionSignalEmitter(QObject):

    completion_signal = Signal(str)
    possible_completion_signal = Signal(str)

    @classmethod
    def get_shortcut(cls):
        return 'completion'

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self._possible_completion = ''

        ShortcutSignalEmitter.instance().shortcut_signal.connect(
            self.on_shortcut_signal)
        WordSignalEmitter.instance().current_word_signal.connect(
            self.on_current_word_signal)

        self.completion_signal.connect(lambda cs:
            Logger.info(
                'CompletionSignalEmitter: Completion Signal (%s)', cs))

    @Slot(dict)
    def on_shortcut_signal(self, shortcut_signal):
        if not self.get_shortcut() in shortcut_signal:
            Logger.debug(
                'CompletionSignalEmitter: Shortcut Not Recognized (%s)',
                shortcut_signal)
            return

        Logger.debug(
            'CompletionSignalEmitter: Shortcut Recognized (%s)',
            shortcut_signal)

        if not self._possible_completion:
            Logger.debug(
                'CompletionSignalEmitter: No Completion Found (%s)',
                self.WordSignalEmitter.instance().current_word)
            return

        self.completion_signal.emit(self._possible_completion)

    @Slot(str)
    def on_current_word_signal(self, word_signal):
        suggestion_name = 'completion_suggestion'
        compl_resp = get_es().suggest(index=WordMappingType.get_index(),
            body={
                suggestion_name: {
                    'text': word_signal,
                    'completion': {
                        'field': 'text'
                    }
                }
            })
        suggestions = compl_resp[suggestion_name][0]['options']
        if suggestions:
            top_suggestion = suggestions[0]['text']
            self._possible_completion = top_suggestion
        else:
            self._possible_completion_event = ''

@ThreadSafeSingleton
class CorrectionSignalEmitter(QObject):

    correction_signal = Signal(str)
    user = None

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        WordSignalEmitter.instance().last_word_signal.connect(
            self.on_last_word_signal)

        self.correction_signal.connect(lambda cs:
            Logger.info(
                'CorrectionSignalEmitter: Correction Signal (%s)', cs))

    @Slot(str)
    def on_last_word_signal(self, last_word_signal):
        # check if last word is blank
        if not str(last_word_signal): return

        if check_if_indexed(self.user, last_word_signal):
            Logger.info(
                'CorrectionSignalEmitter: Word Already Indexed (%s, %s)',
                last_word_signal, str(self.user.id))
            return

        Logger.info(
            'CorrectionSignalEmitter: Word Not Found: (%s)',
            last_word_signal)

        # get suggestion for unknown word
        searcher = S(WordMappingType)
        suggestion_name = 'correction_suggestion'
        suggest_query = searcher.suggest(
            suggestion_name,
            last_word_signal,
            field='text')
        suggestions = suggest_query.suggestions()[suggestion_name][0]['options']

        if not suggestions: return

        # correct last word if necessary
        top_suggestion = suggestions[0]['text']
        self.correction_signal.emit(top_suggestion)

@ThreadSafeSingleton
class SnippetSignalEmitter(QObject):

    snippet_signal = Signal(dict)
    user = None

    @classmethod
    def get_shortcut(cls):
        return 'snippet'

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        ShortcutSignalEmitter.instance().shortcut_signal.connect(
            self.on_shortcut_signal)

        self.snippet_signal.connect(lambda ss:
            Logger.info('SnippetSignalEmitter: Snippet Signal (%s)', ss))

    # TODO: currently only works with function key shortcuts (no combos)
    @Slot(dict)
    def on_shortcut_signal(self, shortcut_signal):

        if not self.get_shortcut() in shortcut_signal:
            Logger.info(
                'SnippetSignalEmitter: Shortcut Not Recognized (%s)',
                shortcut_signal)
            return

        Logger.info(
            'SnippetSignalEmitter: Shortcut Recognized (%s)',
            shortcut_signal)

        # TODO: this is where the extra key gets tack on if its a letter
        snippet = str(WordSignalEmitter.instance().current_word)

        if not snippet in self.user.snippets:
            Logger.info(
                'SnippetSignalEmitter: Snippet Not Recognized (%s)',
                snippet)
            return

        self.snippet_signal.emit({snippet: self.user.snippets[snippet]})