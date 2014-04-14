from accipiokey.core.app import AccipioKeyAppController, AccipioKeyApp
from accipiokey.core import settings
from accipiokey.core.esutils import init_index
from mongoengine import connect

connect(settings.DB)
init_index()
