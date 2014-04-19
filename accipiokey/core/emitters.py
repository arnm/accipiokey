from accipiokey.core import settings
from accipiokey.core.apputils import keycode_to_unicode, check_if_indexed
from accipiokey.core.logger import Logger
from accipiokey.core.mappings import WordMappingType
from datetime import datetime
from elasticutils import S, get_es
from evdev import InputDevice, categorize, ecodes, KeyEvent
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from select import select
from singleton.singleton import ThreadSafeSingleton
from textblob import TextBlob, Word
from time import clock, sleep
import threading


@ThreadSafeSingleton
class KeySignalEmitter(QObject):

    key_signal = pyqtSignal(object)

    @property
    def input_device(self):
        return self._dev

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self._dev = InputDevice('/dev/input/event0')
        self._polling = True
        self._running = False

        self.thread = threading.Thread(target=self._loop)
        self.thread.daemon = True
        self.thread.start()

        # debug statements
        # self.key_signal.connect(
        #     lambda ks: Logger.debug('KeySignalEmitter: Key Signal (%s)', ks))

    @property
    def running(self):
        return self._running

    def _poll(self):
        r, w, x = select([self._dev], [], [])
        for event in self._dev.read():
            if self._running and event.type == ecodes.EV_KEY:
                self.key_signal.emit(categorize(event))

    def run(self):
        self._running = True
        self._polling = True

    # will allow polling but will not emit key events therefore flushing queue
    # user for discarding unwanted key events
    def stop(self):
        self._running = False

    # will pause polling but will allow events to be queued to later read
    def pause(self):
        self._polling = False

    def _loop(self):
        while True:
            if self._polling:
                sleep(0.2)
                self._poll()

@ThreadSafeSingleton
class KeyboardStateSignalEmitter(QObject):

    key_down_signal = pyqtSignal(str)
    key_up_signal = pyqtSignal(str)
    keyboard_state_signal = pyqtSignal(dict)

    @property
    def keyboard_state(self):
        return self._keyboard_state

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self._keyboard_state = {}

        # connect signals to handlers
        KeySignalEmitter.instance().key_signal.connect(self.on_key_signal)

        # debug statements
        # self.keyboard_state_signal.connect(
        #     lambda kbs: Logger.debug(
        #         'KeyBoardStateSignalEmitter: Keyboard State (%s)', kbs))

    @pyqtSlot(object)
    def on_key_signal(self, key_signal):
        keycode = key_signal.keycode
        keystate = key_signal.keystate
        timestamp = clock()

        if keystate == KeyEvent.key_down or keystate == KeyEvent.key_hold:
            if keycode not in self._keyboard_state:
                self._keyboard_state[keycode] = timestamp
                self.keyboard_state_signal.emit(self._keyboard_state)
            self.key_down_signal.emit(keycode)
        elif keystate == KeyEvent.key_up:
            if keycode in self._keyboard_state:
                del self._keyboard_state[keycode]
                self.keyboard_state_signal.emit(self._keyboard_state)
            self.key_up_signal.emit(keycode)

@ThreadSafeSingleton
class WordSignalEmitter(QObject):

    current_word_signal = pyqtSignal(str)
    last_word_signal = pyqtSignal(str)
    word_buffer_signal = pyqtSignal(list)
    indexed_word_signal = pyqtSignal(str)
    user = None

    @property
    def current_word(self):
        return self._current_word

    @property
    def last_word(self):
        return self._last_word

    @property
    def word_buffer(self):
        return self._word_buffer

    # TODO: check if these need to be exposed
    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self._backspace_pressed = False
        self._current_word = ''
        self._last_word = ''
        self._word_buffer = []

        KeyboardStateSignalEmitter.instance().key_down_signal.connect(self.on_key_down_signal)
        self.word_buffer_signal.connect(self.on_word_buffer_signal)

        self.current_word_signal.connect(lambda cws:
            Logger.info(
                'WordSignalEmitter: Last Word (%s) Current Word (%s)',
                self.last_word, cws))

    # TODO: verify this is correct
    def update(self):
        word_list = TextBlob(''.join(self.word_buffer)).words

        # check words have been typed
        if word_list:

            # check if whitespace was entered last
            if not self.word_buffer[-1].strip():
                self._last_word = word_list[-1]
                self._current_word = ''

                self.last_word_signal.emit(self.last_word)
                self.current_word_signal.emit(self.current_word)

                if check_if_indexed(self.user, self.last_word):
                    self.indexed_word_signal.emit(self.last_word)
                return

            # if backspace was pressed and last key typed was whitespace
            if self._backspace_pressed and not self.word_buffer[-1].strip():
                self._last_word = word_list[-1]
                self._current_word = ''
                self._backspace_pressed = False

                self.last_word_signal.emit(self.last_word)
                self.current_word_signal.emit(self.current_word)
                return

            # append current key to current word
            if len(word_list) >= 2:
                self._last_word = word_list[-2]
                self.last_word_signal.emit(self.last_word)
            elif self.last_word:
                self._last_word = ''
            self._current_word = word_list[-1]
            self.current_word_signal.emit(self.current_word)
        else:
            self._current_word = ''
            self._last_word = ''

            self.last_word_signal.emit(self.last_word)
            self.current_word_signal.emit(self.current_word)

    @pyqtSlot(list)
    def on_word_buffer_signal(self, word_buffer):
        self.update()

    @pyqtSlot(str)
    def on_key_down_signal(self, key_down_signal):
        keyboard_state = KeyboardStateSignalEmitter.instance().keyboard_state

        # TODO: create/use constants
        if 'KEY_LEFTALT' in keyboard_state: return
        elif 'KEY_RIGHTALT' in keyboard_state: return
        elif 'KEY_LEFTCTRL' in keyboard_state: return
        elif 'KEY_RIGHTCTRL' in keyboard_state: return

        # TODO: create/find constants
        key_down_signal = keycode_to_unicode(key_down_signal)
        if len(key_down_signal) == 1:
            self._word_buffer.append(key_down_signal)
            self.word_buffer_signal.emit(self.word_buffer)
        elif key_down_signal == 'space':
            self._word_buffer.append(' ')
            self.word_buffer_signal.emit(self.word_buffer)
        elif key_down_signal == 'enter':
            self._word_buffer.append(' ')
            self.word_buffer_signal.emit(self.word_buffer)
        elif key_down_signal == 'tab':
            self._word_buffer.append(' ')
            self.word_buffer_signal.emit(self.word_buffer)
        elif key_down_signal == 'backspace':
            if self.word_buffer:
                self._backspace_pressed = True
                self.word_buffer.pop()
                self.word_buffer_signal.emit(self.word_buffer)

# TODO: review this
@ThreadSafeSingleton
class ShortcutSignalEmitter(QObject):

    shortcut_signal = pyqtSignal(dict)
    user = None

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        KeyboardStateSignalEmitter.instance().keyboard_state_signal.connect(
            self.on_keyboard_state_signal)

        self.shortcut_signal.connect(lambda ss:
            Logger.info('ShortcutSignalEmitter: Shortcut Event(%s)', ss))

    @pyqtSlot(dict)
    def on_keyboard_state_signal(self, keyboard_state_signal):
        for name, shortcut in self.user.shortcuts.items():
            if sorted(keyboard_state_signal.keys()) == sorted(shortcut):
                self.shortcut_signal.emit({name: shortcut})
                break

@ThreadSafeSingleton
class CompletionSignalEmitter(QObject):

    completion_signal = pyqtSignal(str)
    possible_completion_signal = pyqtSignal(str)

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

    @pyqtSlot(dict)
    def on_shortcut_signal(self, shortcut_signal):

        if not WordSignalEmitter.instance().current_word.strip(): return

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
                WordSignalEmitter.instance().current_word)
            return

        self.completion_signal.emit(self._possible_completion)

    @pyqtSlot(str)
    def on_current_word_signal(self, word_signal):

        if not word_signal.strip():
            self._possible_completion = ''
            self.possible_completion_signal.emit(self._possible_completion)
            return

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

        if not suggestions:
            self._possible_completion = ''
            self.possible_completion_signal.emit(self._possible_completion)
            return

        for suggestion in suggestions:
            if suggestion['text'] != word_signal:
                top_suggestion = suggestion['text']
                self._possible_completion = top_suggestion
                break

        self.possible_completion_signal.emit(self._possible_completion)

# TODO: clean up redundent code
@ThreadSafeSingleton
class CorrectionSignalEmitter(QObject):

    correction_signal = pyqtSignal(str)
    possible_correction_signal = pyqtSignal(str)
    user = None

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        WordSignalEmitter.instance().current_word_signal.connect(
            self.on_current_word_signal)

        WordSignalEmitter.instance().last_word_signal.connect(
            self.on_last_word_signal)

        self.correction_signal.connect(lambda cs:
            Logger.info(
                'CorrectionSignalEmitter: Correction Signal (%s)', cs))

    @pyqtSlot(str)
    def on_current_word_signal(self, current_word_signal):
        # check if last word is blank
        if not current_word_signal:
            self.possible_correction_signal.emit('')
            return

        if check_if_indexed(self.user, current_word_signal):
            Logger.info(
                'CorrectionSignalEmitter: Word Already Indexed (%s, %s)',
                current_word_signal, str(self.user.id))
            self.possible_correction_signal.emit('')
            return

        Logger.info(
            'CorrectionSignalEmitter: Word Not Found: (%s)',
            current_word_signal)

        # get suggestion for unknown word
        searcher = S(WordMappingType)
        suggestion_name = 'correction_suggestion'
        suggest_query = searcher.suggest(
            suggestion_name,
            current_word_signal,
            field='text')
        suggestions = suggest_query.suggestions()[suggestion_name][0]['options']

        if not suggestions:
            self.possible_correction_signal.emit('')
            return

        # correct last word if necessary
        top_suggestion = suggestions[0]['text']
        self.possible_correction_signal.emit(top_suggestion)

    @pyqtSlot(str)
    def on_last_word_signal(self, last_word_signal):
        # check if last word is blank
        if not last_word_signal: return

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

    snippet_signal = pyqtSignal(dict)
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

    @pyqtSlot(dict)
    def on_shortcut_signal(self, shortcut_signal):

        if not WordSignalEmitter.instance().current_word.strip(): return

        if not self.get_shortcut() in shortcut_signal:
            Logger.info(
                'SnippetSignalEmitter: Shortcut Not Recognized (%s)',
                shortcut_signal)
            return

        Logger.info(
            'SnippetSignalEmitter: Shortcut Recognized (%s)',
            shortcut_signal)

        snippet = str(WordSignalEmitter.instance().current_word)

        if not snippet in self.user.snippets:
            Logger.info(
                'SnippetSignalEmitter: Snippet Not Recognized (%s)',
                snippet)
            return

        self.snippet_signal.emit({snippet: self.user.snippets[snippet]})
