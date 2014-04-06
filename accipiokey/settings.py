
class Settings(object):

    @property
    def INDEX(self):
        return 'accipiokey-index'

    @property
    def MONGODB(self):
        return 'accipiokey'

    @property
    def TITLE(self):
        return 'Accipio Key'

    @property
    def DEFAULT_CORPUS(self):
        return 'data/words.txt'
