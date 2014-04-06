from mongoengine import *


class User(Document):
    username = StringField(required=True, min_length=4, max_length=30)
    password = StringField(required=True, min_length=4, max_length=30)

class StatSheet(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    words_corrected = IntField()
    words_generated = IntField()
    words_completed = IntField()
    keystrokes_saved = IntField()

class Writing(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    title = StringField(required=True, max_length=120)
    content = StringField(required=True)
