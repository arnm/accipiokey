from mongoengine import *


class User(Document):
    username = StringField(required=True, min_length=4, max_length=30)
    password = StringField(required=True, min_length=4, max_length=30)

class Writing(EmbeddedDocument):
    title = StringField(required=True, min_length=1, max_length=120)
    text = StringField()

class Corpus(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    writings = ListField(EmbeddedDocumentField(Writing))

class Stats(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    words_corrected = IntField()
    words_generated = IntField()
    words_completed = IntField()
    keystrokes_saved = IntField()

