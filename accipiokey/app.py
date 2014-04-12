from accipiokey.apputils import *
from accipiokey.dispatchers import *
from accipiokey.documents import *
from accipiokey.esutils import index_new_words
from accipiokey.handlers import *
from accipiokey.mappings import *
from accipiokey.modals import FileModal
from accipiokey.widgets import *
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.logger import Logger
from textblob import TextBlob
from mongoengine.errors import ValidationError
import mimetypes, os, threading


class AccipioKeyApp(App):
    title = 'Accipio Key'
    LOGIN_SCREEN, REGISTER_SCREEN, HOME_SCREEN = [str(i) for i in range(3)]

    def __init__(self, **kwargs):
        super(AccipioKeyApp, self).__init__(**kwargs)
        self._user = None
        self._sm = ScreenManager()

        WordEventDispatcher.instance().bind(
            indexed_word_event=self._on_indexed_word_event)

        CompletionEventDispatcher.instance().bind(
            completion_event=self._on_completion_event)

        CorrectionEventDispatcher.instance().bind(
            correction_event=self._on_correction_event)

        SnippetEventDispatcher.instance().bind(
            snippet_event=self._on_snippet_event)

    @property
    def user(self):
        return self._user

    @property
    def is_logged_in(self):
        return True if self._user else False

    def build(self):
        self._sm.add_widget(LoginScreen(name=self.LOGIN_SCREEN))
        self._sm.add_widget(RegisterScreen(name=self.REGISTER_SCREEN))
        self._sm.add_widget(HomeScreen(name=self.HOME_SCREEN))
        return self._sm

    def login(self, username, password):
        # check if someone is already logged in
        if self.is_logged_in:
            return False

        # check if user exists
        users = User.objects(username=username, password=password)
        if not users.count():
            return False

        self._user = users[0]
        KeyboardEventDispatcher.instance().poll_forever()
        self._sm.current = self.HOME_SCREEN
        return True

    def logout(self):
        if self.is_logged_in:
            KeyboardEventDispatcher.instance().stop()
            self._user = None
        return True

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
                        snippets={'lol': 'laugh out loud'}
                    ).save()
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

    # TODO: boost each indexed word
    def _on_indexed_word_event(self, instance, indexed_word_event):
        pass

    # TODO: implement method
    def _on_completion_event(self, instance, completion_event):
        KeyboardEventDispatcher.instance().stop()
        KeyboardEventDispatcher.instance().poll_forever()

    # TODO: incorporate user analytics
    def _on_correction_event(self, instance, correction_event):
        KeyboardEventDispatcher.instance().stop()

        wed = WordEventDispatcher.instance()

        Logger.debug(
            'CorrectionEventHandler: Original Word Buffer(%s)',
            wed.word_buffer)

        num_deletions = len(wed.last_word_event) + 1

        Logger.debug(
            'CorrectionEventHandler: Deletions To Be Made (%d)',
            num_deletions)

        # remove incorrect word from buffer
        for _ in range(num_deletions): del wed.word_buffer[-1]
        # delete external app word
        emulate_key_events(['backspace' for _ in range(num_deletions)])

        # add space to corrected word b/c this is invoked after new words
        correction = correction_event + ' '

        Logger.info(
            'CorrectionEventHandler: Correction To Be Made (%s)',
            list(correction))

        # append new word to word buffer
        for character in correction: wed.word_buffer.append(character)

        # simulate corrected word keys in external app
        emulate_key_events([character for character in correction])

        Logger.debug(
            'CorrectionEventHandler: Corrected Word Buffer(%s)',
            wed.word_buffer)

        Logger.info(
            'CorrectionEventHandler: Last Word (%s) Current Word (%s)',
            wed.last_word_event,
            wed.word_event)

        KeyboardEventDispatcher.instance().poll_forever()

    def _on_snippet_event(self, instance, snippet_event):
        KeyboardEventDispatcher.instance().stop()

        wed = WordEventDispatcher.instance()

        Logger.debug(
            'SnippetEventHandler: Original Word Buffer(%s)',
            wed.word_buffer)

        num_deletions = len(wed.word_event)

        Logger.debug(
            'SnippetEventHandler: Deletions To Be Made (%d)',
            num_deletions)

        # remove incorrect word from buffer
        for _ in range(num_deletions): del wed.word_buffer[-1]
        # delete external app word
        emulate_key_events(['backspace' for _ in range(num_deletions)])

        # add space to corrected word b/c this is invoked after new words
        correction = snippet_event.itervalues().next()

        Logger.info(
            'SnippetEventHandler: Correction To Be Made (%s)',
            list(correction))

        # append new word to word buffer
        for character in correction: wed.word_buffer.append(character)

        # simulate corrected word keys in external app
        emulate_key_events([character for character in correction])

        Logger.debug(
            'SnippetEventHandler: Corrected Word Buffer(%s)',
            wed.word_buffer)

        Logger.info(
            'SnippetEventHandler: Last Word (%s) Current Word (%s)',
            wed.last_word_event,
            wed.word_event)

        KeyboardEventDispatcher.instance().poll_forever()

    def add_writing(self, path):
        if not self.is_logged_in:
            return False

        if not mimetypes.guess_type(path)[0] == 'text/plain':
            return False

        with open(path, 'r') as f:
            title = os.path.splitext(os.path.basename(path))
            content = f.read()
            writing = Writing(title=title, content=content)
            writing.save()
            self._process_writing(writing)

        return True

    def _process_writing(self, writing):
        pass

class LoginScreen(Screen):

    username = StringProperty()
    password = StringProperty()

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self._app = AccipioKeyApp.get_running_app()

    def login(self):
        if not self._app.login(self.username, self.password):
            show_message(
                'Login Failed',
                'Invalid credentials, please try again.')

        self.ids.ti_username.text = ''
        self.ids.ti_password.text = ''

class RegisterScreen(Screen):

    username = StringProperty()
    password1 = StringProperty()
    password2 = StringProperty()

    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self._app = AccipioKeyApp.get_running_app()

    def clear(self):
        self.ids.ti_username.text = ''
        self.ids.ti_password1.text = ''
        self.ids.ti_password2.text = ''

    def finish(self):
        self.clear()
        self.manager.current = self._app.LOGIN_SCREEN

    def register(self):
        # check if username field is empty
        if not self.username:
            show_message("Empty Field", "Please enter in a username.")
            return

        # check if either password field is empty
        if not self.password1 or not self.password2:
            show_message('Empty Field', 'Please enter matching passwords.')
            return

        # check if passwords don't match
        if not self.password1 == self.password2:
            show_message(
                'Password Mismatch',
                'Please enter matching passwords.')
            return

        # check if registration failed
        if not self._app.register(self.username, self.password1):
            show_message(
                'Registration Failed',
                'Please choose a different username.')
            return

        self.finish()

class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self._app = AccipioKeyApp.get_running_app()

    def dismiss_file_modal(self):
        self._file_modal.dismiss()

    def show_file_dialog(self):
        self._file_modal = FileModal(
                                title='Load Corpus',
                                load=self.load,
                                cancel=self.dismiss_file_modal)
        self._file_modal.open()

    def load(self, selections):
        self.dismiss_file_modal();

        invalid_selections = []
        for selection in selections:
            if not self._app.add_corpus(selection):
                invalid_selections.append(selection)

        if not selections:
            show_message('Invalid Corpora', str(invalid_selections))
