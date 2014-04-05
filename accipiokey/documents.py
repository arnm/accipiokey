from mongoengine import *


class User(Document):
    username = StringField(required=True, max_length=30)
    password = StringField(required=True, max_length=30)

class Writing(EmbeddedDocument):
    title = StringField(max_length=120, required=True)
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

