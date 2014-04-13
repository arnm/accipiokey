from accipiokey.app import AccipioKeyApp
from accipiokey import settings
from accipiokey.esutils import init_index
from mongoengine import connect

connect(settings.DB)
init_index()
