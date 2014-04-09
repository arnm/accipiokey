import yaml

URLS = ['localhost']
INDEX = 'accipiokey'
TITLE = 'Accipio Key'
DEFAULT_CORPUS = 'data/words.txt'
USER_SETTINGS = {}

def load_user_settings():
    with open('settings.yaml', 'r') as settings_handle:
        USER_SETTINGS = yaml.safe_load(settings_handle)


