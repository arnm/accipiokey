from accipiokey.core.apputils import emulate_key_events
from accipiokey.core.documents import *
from accipiokey.core.emitters import *
from accipiokey.gui.windows import *
from mongoengine.errors import ValidationError
from PySide.QtCore import Slot
from PySide.QtGui import QApplication
from singleton.singleton import ThreadSafeSingleton
from textblob import TextBlob
import mimetypes, os, threading

@ThreadSafeSingleton
class AccipioKeyApp(QObject):

    @property
    def user(self):
        return self._user

    @property
    def is_logged_in(self):
        return True if self._user else False

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        # private members
        self._user = None

        # Handle Emitters
        WordSignalEmitter.instance().indexed_word_signal.connect(
            self._on_indexed_word_signal)

        CorrectionSignalEmitter.instance().correction_signal.connect(
            self._on_correction_signal)

        CompletionSignalEmitter.instance()
        CompletionSignalEmitter.instance().completion_signal.connect(
            self._on_completion_signal)

        SnippetSignalEmitter.instance().snippet_signal.connect(
            self._on_snippet_signal)

    def _init_emitters(self):
        WordSignalEmitter.instance().user = self.user
        ShortcutSignalEmitter.instance().user = self.user
        CorrectionSignalEmitter.instance().user = self.user
        SnippetSignalEmitter.instance().user = self.user

    def register(self, username, password):
        # check if user exists with that username
        if User.objects(username=username).count():
            return False

        # setup default user in DB
        try:
            user = User(
                username=username,
                password=password,
                shortcuts={
                    'completion': ['KEY_LEFTALT'],
                    'snippet': ['KEY_RIGHTALT']
                },
                snippets={'lol': 'laugh out loud'}).save()
        except ValidationError:
            return False

        # index default words for new user
        with open(settings.DEFAULT_CORPUS) as corpus:
            thread = threading.Thread(
                target=index_new_words,
                args=(user, corpus.readlines(),))
            thread.daemon = True
            thread.start()
        return True

    def login(self, username, password):
        # check if someone is already logged in
        if self.is_logged_in:
            Logger.debug(
                'AccipioKeyApp: Already Logged In (%s)', self.user.username)
            return False

        # check if user exists
        users = User.objects(username=username, password=password)
        if not users.count():
            Logger.debug('AccipioKeyApp: User Not Registered (%s)', username)
            return False

        self._user = users[0]
        Logger.debug('AccipioKeyApp: Logging In (%s)', self.user.username)
        return True

    def start(self):
        if not self.is_logged_in:
            Logger.debug('AccipioKeyApp: Not Logged In')
            return

        if KeySignalEmitter.instance().running:
            Logger.debug('AccipioKeyApp: Already Running')
            return

        Logger.debug('AccipioKeyApp: Starting')
        self._init_emitters()
        KeySignalEmitter.instance().poll_forever()

    # TODO: this doesn't really stop recording of keys
    def stop(self):
        if not self.is_logged_in:
            Logger.debug('AccipioKeyApp: Not Logged In')
            return

        if not KeySignalEmitter.instance().running:
            Logger.debug('AccipioKeyApp: Already Stopped')
            return

        Logger.debug('AccipioKeyApp: Stopping')
        KeySignalEmitter.instance().stop()

    def logout(self):
        if not self.is_logged_in:
            Logger.debug('AccipioKeyApp: Not Logged In')
            return

        Logger.debug('AccipioKeyApp: Logging Out (%s)', self.user.username)
        KeySignalEmitter.instance().stop()
        self._user = None

    def add_writing(self, path):
        if not self.is_logged_in: return False
        if not mimetypes.guess_type(path)[0] == 'text/plain': return False

        with open(path, 'r') as f:
            title = os.path.splitext(os.path.basename(path))
            content = f.read()
            writing = Writing(title=title, content=content)
            writing.save()
            self._process_writing(writing)
        return True

    # TODO: implement
    def _process_writing(self, writing):
        pass

    # TODO: implement
    @Slot(str)
    def _on_indexed_word_signal(self, indexed_word_signal):
        Logger.debug('IndexedWordSignalHandler: (%s)', indexed_word_signal)

    # TODO: incorporate user analytics
    @Slot(str)
    def _on_correction_signal(self, correction_signal):
        KeySignalEmitter.instance().stop()

        wed = WordSignalEmitter.instance()

        # Logger.debug(
        #     'CorrectionSEmitter: Original Word Buffer(%s)',
        #     wed.word_buffer)

        num_deletions = len(wed.last_word) + 1

        Logger.debug(
            'CorrectionSEmitter: Deletions To Be Made (%d)',
            num_deletions)

        # remove incorrect word from buffer
        for _ in range(num_deletions): del wed.word_buffer[-1]
        # delete external app word
        emulate_key_events(['backspace' for _ in range(num_deletions)])

        # add space to corrected word b/c this is invoked after new words
        correction = correction_signal + ' '

        Logger.info(
            'CorrectionSEmitter: Correction To Be Made (%s)',
            list(correction))

        # append new word to word buffer
        for character in correction: wed.word_buffer.append(character)

        # simulate corrected word keys in external app
        emulate_key_events([character for character in correction])

        # Logger.debug(
        #     'CorrectionSEmitter: Corrected Word Buffer(%s)',
        #     wed.word_buffer)

        Logger.info(
            'CorrectionSEmitter: Last Word (%s) Current Word (%s)',
            wed.last_word,
            wed.current_word)

        KeySignalEmitter.instance().poll_forever()

    @Slot(str)
    def _on_completion_signal(self, completion_signal):
        KeySignalEmitter.instance().stop()

        wed = WordSignalEmitter.instance()

        # Logger.debug(
        #     'CompletionSignalHandler: Original Word Buffer(%s)',
        #     wed.word_buffer)

        # get remaining string of completion
        postfix = completion_signal[len(wed.current_word):]

        Logger.debug('CompletionSignalHandler: Postfix (%s)', postfix)

        # append postfix to word buffer
        for character in postfix: wed.word_buffer.append(character)

        # simulate postfix keys in external app
        emulate_key_events([character for character in postfix])

        # Logger.debug(
        #     'CompletionSignalHandler: Corrected Word Buffer(%s)',
        #     wed.word_buffer)

        Logger.info(
            'CompletionSignalHandler: Last Word (%s) Current Word (%s)',
            wed.last_word,
            wed.current_word)

        KeySignalEmitter.instance().poll_forever()

    # TODO: incorporate analytics
    @Slot(dict)
    def _on_snippet_signal(self, snippet_signal):
        KeySignalEmitter.instance().stop()

        wed = WordSignalEmitter.instance()

        # Logger.debug(
        #     'SnippetSignalHandler: Original Word Buffer(%s)',
        #     wed.word_buffer)

        num_deletions = len(wed.current_word)

        Logger.debug(
            'SnippetSignalHandler: Deletions To Be Made (%d)',
            num_deletions)

        # remove incorrect word from buffer
        for _ in range(num_deletions): del wed.word_buffer[-1]
        # delete external app word
        emulate_key_events(['backspace' for _ in range(num_deletions)])

        # add space to corrected word b/c this is invoked after new words
        correction = snippet_signal.itervalues().next()

        Logger.info(
            'SnippetSignalHandler: Correction To Be Made (%s)',
            list(correction))

        # append new word to word buffer
        for character in correction: wed.word_buffer.append(character)

        # simulate corrected word keys in external app
        emulate_key_events([character for character in correction])

        # Logger.debug(
        #     'SnippetSignalHandler: Corrected Word Buffer(%s)',
        #     wed.word_buffer)

        Logger.info(
            'SnippetSignalHandler: Last Word (%s) Current Word (%s)',
            wed.last_word,
            wed.current_word)

        KeySignalEmitter.instance().poll_forever()

class AccipioKeyAppController(QApplication):

    def __init__(self, argv):
        super(AccipioKeyAppController, self).__init__(argv)
        self._app = AccipioKeyApp.instance()

        self._user_window = UserWindow()
        self._user_window.ui.actionStart.triggered.connect(self._on_app_start)
        self._user_window.ui.actionStop.triggered.connect(self._on_app_stop)
        self._user_window.ui.actionLogout.triggered.connect(self._on_app_logout)

    def exec_(self):
        self._run()
        super(AccipioKeyAppController, self).exec_()

    def _run(self):
        login_window = LoginWindow()

        @Slot(dict)
        def on_login_signal(credentials):
            if self._app.login(credentials['username'],credentials['password']):
                login_window.close()
                self._user_window.setWindowTitle(self._app.user.username)
                self._user_window.show()

        @Slot()
        def on_register_signal():
            register_window = RegisterWindow(login_window)

            @Slot(dict)
            def on_register_signal(credentials):
                if self._app.register(
                    credentials['username'], credentials['password']):
                    register_window.close()

            @Slot()
            def on_cancel_signal():
                register_window.close()

            register_window.register_signal.connect(on_register_signal)
            register_window.show()

        login_window.login_signal.connect(on_login_signal)
        login_window.register_signal.connect(on_register_signal)
        login_window.show()

    def _on_app_start(self):
        self._app.start()

    def _on_app_stop(self):
        self._app.stop()

    def _on_app_logout(self):
        self._app.logout()
        self._user_window.close()
        self._run()
