from accipiokey import settings
from accipiokey.mappings import *

from elasticutils import get_es
from elasticsearch.helpers import bulk

def init_index():
    es = get_es()

    if not es.indices.exists(settings.INDEX):
        # create index
        es.indices.create(settings.INDEX)

        # put mappings
        es.indices.put_mapping(
            index=settings.INDEX, doc_type=UserMappingType.get_mapping_type_name(), body=UserMappingType.get_mapping())
        es.indices.put_mapping(
            index=settings.INDEX, doc_type=StatSheetMappingType.get_mapping_type_name(), body=StatSheetMappingType.get_mapping())
        es.indices.put_mapping(
            index=settings.INDEX, doc_type=WritingMappingType.get_mapping_type_name(), body=WritingMappingType.get_mapping())
        es.indices.put_mapping(
            index=settings.INDEX, doc_type=WordMappingType.get_mapping_type_name(), body=WordMappingType.get_mapping())

def index_new_words(user_dict, words, normalize_func=lambda s: s.lower().rstrip()):
    actions = []
    for text in words:
        action = { '_parent': user_dict['_id'], 'text' : normalize_func(text)}
        actions.append(action)
    bulk(client=get_es(), actions=actions, index=WordMappingType.get_index(), doc_type=WordMappingType.get_mapping_type_name())

def increase_word_boost(user_dict, word):
    pass
