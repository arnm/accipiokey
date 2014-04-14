from mongoengine import *


class User(Document):
    username = StringField(required=True, min_length=4, max_length=30)
    password = StringField(required=True, min_length=4, max_length=30)
    shortcuts = DictField()
    snippets = DictField()

class StatSheet(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    words_corrected = IntField(min_value=0)
    words_generated = IntField(min_value=0)
    words_completed = IntField(min_value=0)
    keystrokes_saved = IntField(min_value=0)

class Writing(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    title = StringField(required=True, max_length=120)
    content = StringField(required=True)
