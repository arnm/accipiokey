from accipiokey import Settings
from accipiokey.mappings import *

from elasticutils import get_es
from elasticsearch.helpers import bulk

def index_str_list(client, index, doc_type, str_list, normalize_func=lambda s: s.lower().rstrip()):
    actions = []
    for id, string in enumerate(str_list):
        action = {'_id': id, 'text' : normalize_func(string)}
        actions.append(action)
    bulk(client, actions, index=index, doc_type=doc_type)

def init_index():
    es = get_es()

    if not es.indices.exists(Settings.INDEX):
        mappings_body = {}
        mappings_body.update(UserMappingType.get_mapping())
        mappings_body.update(StatSheetMappingType.get_mapping())
        mappings_body.update(WritingMappingType.get_mapping())
        mappings_body.update(WordMappingType.get_mapping())
        mappings= {}
        mappings['mappings'] = mappings_body

        es.indices.create(index=Settings.INDEX, body=mappings_body)
