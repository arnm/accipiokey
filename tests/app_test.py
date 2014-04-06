import random
import string

from accipiokey.app import AccipioKeyApp
from accipiokey.documents import User

from nose.tools import eq_, assert_true, assert_false

def gen_id(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class TestAccipioKeyApp():

    @classmethod
    def setup_class(cls):
        # instantiate db connection
        from mongoengine import connect
        cls.db_name = 'accipiokey_test'
        cls.db = connect(cls.db_name)

    @classmethod
    def teardown_class(cls):
        pass

    def setup(self):
        # create test user
        self.user = User(username='test', password='user')
        self.user.save()

        # create test app
        self.app = AccipioKeyApp()

    def teardown(self):
        # start next test with clean db
        self.db.drop_database(self.db_name)

    def correct_login_credentials_test(self):
        # check there is no user currently logged in
        assert_false(self.app.is_logged_in)
        assert_false(self.app.user)

        # check for successful login
        assert_true(self.app.login(self.user.username, self.user.password))
        eq_(self.app.user.username, self.user.username)
        eq_(self.app.user.password, self.user.password)

    def incorrect_login_credentials_test(self):
        # check there is no user currently logged in
        assert_false(self.app.is_logged_in)
        assert_false(self.app.user)

        # check for unsuccessful login
        username = gen_id()
        password = gen_id()
        assert_false(self.app.login(username, password))

    def register_new_user_test(self):
        username = gen_id()
        password = gen_id()

        # check that user is not already in db
        users = User.objects(username=username)
        eq_(users.count(), 0)

        # check user was added after registration
        assert_true(self.app.register(username, password))
        users = User.objects(username=username)
        eq_(users.count(), 1)
        user = users[0]
        eq_(user.username, username)
        eq_(user.password, password)

    def taken_username_register_test(self):
        assert_false(self.app.register(self.user.username, gen_id))

