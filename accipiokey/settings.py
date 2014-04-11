import yaml

URLS = ['localhost']
INDEX = 'accipiokey'
DB = 'accipiokey'
TITLE = 'Accipio Key'
DEFAULT_CORPUS = 'data/words.txt'
USER_SETTINGS = {}
HANDLE_EVENTS = False

def load_user_settings():
    with open('settings.yaml', 'r') as settings_handle:
        global USER_SETTINGS
        USER_SETTINGS = yaml.safe_load(settings_handle)


