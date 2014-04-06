class MetaSettings(type):

    @property
    def URLS(cls):
        return cls.URLS

    @classmethod
    def INDEX(cls):
        return cls.INDEX

    @property
    def MONGODB(cls):
        return cls.MONGODB

    @property
    def TITLE(cls):
        return cls.TITLE

    @property
    def DEFAULT_CORPUS(cls):
        return cls.DEFAULT_CORPUS

class Settings(object):

    __metaclass__ = MetaSettings

    URLS = ['localhost']
    INDEX = 'accipiokey'
    MONGODB = 'accipiokey'
    TITLE = 'Accipio Key'
    DEFAULT_CORPUS = 'data/words.txt'


