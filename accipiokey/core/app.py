from accipiokey.core.documents import *
from accipiokey.core.emitters import *
from accipiokey.gui.windows import *
from mongoengine.errors import ValidationError
from PySide.QtGui import QApplication
from textblob import TextBlob
import mimetypes, os, threading
from singleton.singleton import ThreadSafeSingleton

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

        # Init Emitters
        WordSignalEmitter.instance()
        CorrectionSignalEmitter.instance()
        CompletionSignalEmitter.instance()
        ShortcutSignalEmitter.instance().app = self
        SnippetSignalEmitter.instance().app = self

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
            return False

        # check if user exists
        users = User.objects(username=username, password=password)
        if not users.count():
            return False

        self._user = users[0]
        KeySignalEmitter.instance().poll_forever()
        return True

    def logout(self):
        if self.is_logged_in:
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

    def _process_writing(self, writing):
        pass


class AccipioKeyAppController(QApplication):

    def __init__(self, argv):
        super(AccipioKeyAppController, self).__init__(argv)
        self._app = AccipioKeyApp.instance()

    def _run(self):
        login_window = LoginWindow()

        @Slot(dict)
        def on_login_signal(credentials):
            self._app.login(credentials['username'], credentials['password'])

        @Slot()
        def on_register_signal():
            register_window = RegisterWindow(login_window)

            @Slot(dict)
            def on_register_signal(credentials):
                if self._app.register(credentials['username'], credentials['password']):
                    register_window.close()

            @Slot()
            def on_cancel_signal():
                register_window.close()

            register_window.register_signal.connect(on_register_signal)
            register_window.show()

        login_window.login_signal.connect(on_login_signal)
        login_window.register_signal.connect(on_register_signal)
        login_window.show()

    def exec_(self):
        self._run()
        super(AccipioKeyAppController, self).exec_()
