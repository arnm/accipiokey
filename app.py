from accipiokey.helpers import *
from elasticsearch import Elasticsearch

INDEX = 'accipiokey'
TYPE = 'word'

es = Elasticsearch()

if not es.indices.exists(INDEX):
    es.indices.create(index=INDEX, body=
        {
            'settings': { 'index': { 'number_of_shards': 1, 'number_of_replicas': 0 } }
        }
    )
    mapping = {
            'properties': {
                'text': {
                    'type': 'completion',
                    'index_analyzer': 'simple',
                    'search_analyzer': 'simple',
                    'payloads': True
                }
            }
        }

    es.indices.put_mapping(index=INDEX, doc_type=TYPE, body=mapping)

    with open('data/words.txt') as data_file:
        index_str_list(client=es, index=INDEX, doc_type=TYPE, str_list=data_file.readlines())

map_res = es.indices.get_field_mapping(field='text', index=INDEX, doc_type=TYPE)
# print(map_res)

search = es.search(index=INDEX, doc_type=TYPE, body=
    {
        "query": {
            "term": { "text" : "town"}
        }
    })

# print('search', search)

term = es.suggest(index=INDEX, body=
    {
        "termSuggestion": {
            "text": 'trtle',
            "term": {
                "field": "text"
            }
        }
    })

print('term: ', term)

completion = es.suggest(index=INDEX, body=
    {
        "competionSuggestion": {
            "text": "trtle",
            "completion": {
                "field": "text"
            }
        }
    })
print('completion:', completion)
