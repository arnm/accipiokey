from accipiokey.core import settings
from accipiokey.core.mappings import *

from elasticutils import get_es
from elasticsearch.helpers import bulk

def init_index():
    es = get_es()

    if not es.indices.exists(settings.INDEX):
        # create index
        es.indices.create(settings.INDEX)

        es.indices.put_mapping(
            index=settings.INDEX,
            doc_type=WordMappingType.get_mapping_type_name(),
            body=WordMappingType.get_mapping())

def index_new_words(user, words, normalize_func=lambda s: s.lower().rstrip()):
    actions = []
    for text in words:
        action = { 'user': str(user.id), 'text' : normalize_func(text)}
        actions.append(action)
    bulk(
        client=get_es(),
        actions=actions,
        index=WordMappingType.get_index(),
        doc_type=WordMappingType.get_mapping_type_name())
