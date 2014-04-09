from accipiokey.app import AccipioKeyApp
from accipiokey import settings
from accipiokey.esutils import init_index


settings.load_user_settings()
init_index()
