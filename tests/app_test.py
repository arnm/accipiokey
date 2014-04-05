from accipiokey.app import AccipioKeyApp

from nose.tools import eq_

class TestAccipioKeyApp():

    @classmethod
    def setup_class(cls):
        from mongoengine import connect
        cls.db_name = 'accipiokey_test'
        cls.db = connect(cls.db_name)

    @classmethod
    def teardown_class(cls):
        cls.db.drop_database(cls.db_name)

    def setup(self):
        self.username = 'anunez'
        self.password = 'pass'
        self.app = AccipioKeyApp()

    def teardown(self):
        pass

    def login_test(self):
        eq_(self.app.user, None)
        self.app.login(self.username, self.password)
        eq_(self.app.user.username, self.username)
        eq_(self.app.user.password, self.password)

    def register_test(self):
        self.app.register()

