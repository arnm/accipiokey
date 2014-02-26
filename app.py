from accipiokey.indices import *
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[{"host": "localhost", "port": 9300}])
with open('data/words.txt') as data_file:
    index_str_list(client=es, index='accipiokey_index', doc_type='string_type', str_list=data_file.readlines())

response = es.get(index='accipiokey_index', doc_type='string_type' , id=1)
print('response', response)
print('source', response['_source'])

