from accipiokey.core.apputils import emulate_key_events
from accipiokey.core.documents import *
from accipiokey.core.emitters import *
from accipiokey.core.esutils import index_new_words
from accipiokey.gui.windows import *
from mongoengine.errors import ValidationError
from os.path import commonprefix
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication
from singleton.singleton import ThreadSafeSingleton
from textblob import TextBlob
import mimetypes, os, threading

@ThreadSafeSingleton
class AccipioKeyApp(QObject):

    user_statsheet_updated = pyqtSignal()

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
        self._statsheet = None

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
            Logger.info('AccipioKeyApp: User Name Taken (%s)', username)
            return False

        Logger.info('AccipioKeyApp: Registering (%s)', username)
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
            # check documents for specify error
            Logger.debug('AccipioKeyApp: Registration Validation Error')
            return False

        # create new user statsheet
        statsheet = StatSheet(user=user)
        statsheet.words_completed = 0
        statsheet.words_corrected = 0
        statsheet.snippets_used = 0
        statsheet.keystrokes_saved = 0
        statsheet.save()

        Logger.debug('AccipioKeyApp: Indexing Default Words for User (%s)', user.username)
        # index default words for new user
        with open(settings.DEFAULT_CORPUS) as corpus:
            thread = threading.Thread(
                target=index_new_words,
                args=(user, corpus.readlines(),))
            thread.daemon = True
            thread.start()
        Logger.info('AccipioKeyApp: User Registered (%s)', user.username)
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
        self._statsheet = StatSheet.objects(user=self._user)[0]
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
        KeySignalEmitter.instance().run()

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
        self._statsheet = None

    def add_writing(self, path):
        if not self.is_logged_in: return False
        if not mimetypes.guess_type(path)[0] == 'text/plain': return False

        with open(path, 'r') as f:
            title = os.path.splitext(os.path.basename(path))
            content = f.read()
            writing = Writing(user=self._user, title=title, content=content)
            writing.save()
            self._process_writing(writing)
        return True

    # TODO: implement
    def _process_writing(self, writing):
        pass

    # TODO: implement
    @pyqtSlot(str)
    def _on_indexed_word_signal(self, indexed_word_signal):
        Logger.debug('IndexedWordSignalHandler: (%s)', indexed_word_signal)

    # TODO: incorporate user analytics
    @pyqtSlot(str)
    def _on_correction_signal(self, correction_signal):
        KeySignalEmitter.instance().pause()

        wse = WordSignalEmitter.instance()

        # Logger.debug(
        #     'CorrectionSEmitter: Original Word Buffer(%s)',
        #     wse.word_buffer)

        prefix = commonprefix([correction_signal, wse.last_word])

        Logger.debug(
            'CorrectionSEmitter: Common Prefix (%s)',
            prefix)

        num_deletions = (len(wse.last_word) - len(prefix)) + 1

        Logger.debug(
            'CorrectionSEmitter: Deletions To Be Made (%d)',
            num_deletions)

        postfix = correction_signal[len(prefix):]

        # remove incorrect word from buffer
        for _ in range(num_deletions): del wse.word_buffer[-1]
        # delete external app word
        emulate_key_events(['backspace' for _ in range(num_deletions)])

        # add space to corrected word b/c this is invoked after new words
        completion = postfix + ' '

        Logger.info(
            'CorrectionSEmitter: Correction To Be Made (%s)',
            list(completion))

        # append new word to word buffer
        for character in completion: wse.word_buffer.append(character)

        # simulate corrected word keys in external app
        emulate_key_events([character for character in completion])

        # Logger.debug(
        #     'CorrectionSEmitter: Corrected Word Buffer(%s)',
        #     wse.word_buffer)

        # update statsheet
        self._statsheet.words_corrected += 1
        self._statsheet.keystrokes_saved += (num_deletions + len(postfix))
        self._statsheet.save()
        self.user_statsheet_updated.emit()

        KeySignalEmitter.instance().run()

        WordSignalEmitter.instance().update()
        Logger.info(
            'CorrectionSEmitter: Last Word (%s) Current Word (%s)',
            wse.last_word,
            wse.current_word)

    @pyqtSlot(str)
    def _on_completion_signal(self, completion_signal):
        KeySignalEmitter.instance().pause()

        wse = WordSignalEmitter.instance()

        # Logger.debug(
        #     'CompletionSignalHandler: Original Word Buffer(%s)',
        #     wse.word_buffer)

        # get remaining string of completion
        postfix = completion_signal[len(wse.current_word):] + ' '

        if not postfix.strip():
            KeySignalEmitter.instance().run()
            return

        Logger.debug('CompletionSignalHandler: Postfix (%s)', postfix)

        # append postfix to word buffer
        for character in postfix: wse.word_buffer.append(character)

        # simulate postfix keys in external app
        emulate_key_events([character for character in postfix])

        # Logger.debug(
        #     'CompletionSignalHandler: Corrected Word Buffer(%s)',
        #     wse.word_buffer)

        # update statsheet
        self._statsheet.words_completed += 1
        self._statsheet.keystrokes_saved += len(postfix)
        self._statsheet.save()
        self.user_statsheet_updated.emit()

        KeySignalEmitter.instance().run()

        WordSignalEmitter.instance().update()
        Logger.info(
            'CompletionSignalHandler: Last Word (%s) Current Word (%s)',
            wse.last_word,
            wse.current_word)

    # TODO: bug when pressed consecutively (WordSignalEmitter bug)
    @pyqtSlot(dict)
    def _on_snippet_signal(self, snippet_signal):
        KeySignalEmitter.instance().pause()

        wse = WordSignalEmitter.instance()
        # Logger.debug(
        #     'SnippetSignalHandler: Original Word Buffer(%s)',
        #     wse.word_buffer)

        num_deletions = len(wse.current_word)

        Logger.debug(
            'SnippetSignalHandler: Deletions To Be Made (%d)',
            num_deletions)

        # remove incorrect word from buffer
        for _ in range(num_deletions): del wse.word_buffer[-1]
        # delete external app word
        emulate_key_events(['backspace' for _ in range(num_deletions)])

        # add space to corrected word b/c this is invoked after new words
        correction = snippet_signal.itervalues().next() + ' '

        Logger.info(
            'SnippetSignalHandler: Correction To Be Made (%s)',
            list(correction))

        # append new word to word buffer
        for character in correction: wse.word_buffer.append(character)

        # simulate corrected word keys in external app
        emulate_key_events([character for character in correction])

        # Logger.debug(
        #     'SnippetSignalHandler: Corrected Word Buffer(%s)',
        #     wse.word_buffer)

        self._statsheet.snippets_used += 1
        self._statsheet.keystrokes_saved += (len(correction) - num_deletions)
        self._statsheet.save()
        self.user_statsheet_updated.emit()

        KeySignalEmitter.instance().run()

        WordSignalEmitter.instance().update()
        Logger.info(
            'SnippetSignalHandler: Last Word (%s) Current Word (%s)',
            wse.last_word,
            wse.current_word)

class AccipioKeyAppController(QApplication):

    def __init__(self, argv):
        super(AccipioKeyAppController, self).__init__(argv)

        # members
        self._app = AccipioKeyApp.instance()
        self._user_window = None

        self._app.user_statsheet_updated.connect(self._on_user_statsheet_updated)

    def exec_(self):
        self._run()
        super(AccipioKeyAppController, self).exec_()

    def _run(self):
        login_window = LoginWindow()

        @pyqtSlot(dict)
        def on_login_signal(credentials):
            if not self._app.login(credentials['username'],credentials['password']):
                login_window.ui.statusbar.showMessage('Invalid credentials', 3000)
                return
            login_window.close()
            self._init_user_window()

        @pyqtSlot()
        def on_register_signal():
            register_window = RegisterWindow(login_window)

            @pyqtSlot(dict)
            def on_register_signal(credentials):
                if not self._app.register(credentials['username'], credentials['password']):
                    register_window.ui.statusbar.showMessage('Invalid fields', 3000)
                    return
                register_window.close()

            @pyqtSlot()
            def on_cancel_signal():
                register_window.close()

            register_window.register_signal.connect(on_register_signal)
            register_window.cancel_signal.connect(on_cancel_signal)
            register_window.show()

        login_window.login_signal.connect(on_login_signal)
        login_window.register_signal.connect(on_register_signal)
        login_window.show()

    @pyqtSlot()
    def _on_user_statsheet_updated(self):
        self._user_window.update_stats_model()

    def _init_user_window(self):
        self._user_window = UserWindow(self._app.user)

        # signals
        self._user_window.ui.app_state_toggle_btn.toggled.connect(
            self._on_app_state_toggle_btn_toggle)
        self._user_window.ui.actionLogout.triggered.connect(self._on_app_logout)

        self._user_window.show()

    @pyqtSlot(int)
    def _on_app_state_toggle_btn_toggle(self, checked):

        if not checked:
            self._app.stop()
            self._user_window.notification_window.close()
            return

        self._app.start()
        self._user_window.notification_window.show()

    def _on_app_logout(self):
        self._app.logout()
        self._user_window.close()
        self._user_window = None
        self._run()
