from accipiokey import Settings
from accipiokey import AccipioKeyApp

from mongoengine import connect
from elasticsearch import Elasticsearch

def init_es():
    es = Elasticsearch()

    if not es.indices.exists(Settings.INDEX):
        pass

if __name__ == '__main__':
    init_es()
    connect('accipiokey')
    AccipioKeyApp().run()
