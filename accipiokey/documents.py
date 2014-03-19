from textblob import TextBlob

class User(object):

    def __init__(self, schema):
        self._schema = schema
        self._id = schema['_id']
        self._username = schema['username']
        self._password = schema['password']

    @property
    def username(self):
        return self._username

    @property
    def id(self):
        return self._id

    @property
    def password(self):
        return self._password

class Corpus(object):

    def __init__(self, schema):
        self._schema = schema
        self._user = schema['user']
        self._corpus = schema['corpus']
        self._blob = TextBlob(self._corpus)

    @property
    def user(self):
        return self._user

    @property
    def corpus(self):
        return self._corpus

    @property
    def blob(self):
        return self._blob
