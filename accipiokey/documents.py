from textblob import TextBlob

class Document(object):

    def __init__(self, schema):
        self._schema = schema
        self._id = schema['_id']

    @property
    def id(self):
        return self._id

    def __str__(self):
        return str(self._schema)

class User(Document):

    def __init__(self, schema):
        super().__init__(schema)
        self._username = schema['username']
        self._password = schema['password']

    def __repr__(self):
        pass

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

