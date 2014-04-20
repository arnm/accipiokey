from accipiokey.core import settings
from accipiokey.core.mappings import *
from accipiokey.core.logger import Logger
from elasticsearch.helpers import bulk
from elasticutils import get_es, S

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
        text = normalize_func(text)
        action = { 'user': str(user.id), 'text' : { 'input': text, 'output': text, 'weight': 1} }
        actions.append(action)

    bulk(
        client=get_es(),
        actions=actions,
        index=WordMappingType.get_index(),
        doc_type=WordMappingType.get_mapping_type_name())

# TODO: not necessary, refactor out of code, use get_word instead
def check_if_indexed(user, word):
    if get_word(user, word): return True
    return False

# TODO: scan code to check if execute should be called on all queries
def get_word(user, word):
    searcher = S(WordMappingType)
    word_query = searcher.query(
        user__term=str(user.id),
        text__term=str(word),
        must=True).execute()
    if word_query.results:
        return word_query.results[0]
    return None

# TODO: add error handling
def increment_word_weight(user, word):
    indexed_word = get_word(user, word)
    weight = indexed_word['_source']['text']['weight']
    weight += 1

    Logger.info('Incremented Weight: (%s) (%d)' % (word, weight))

    es = get_es()
    es.index(index=WordMappingType.get_index(),
        doc_type=WordMappingType.get_mapping_type_name(),
        id=indexed_word['_id'],
        refresh=True,
        body={
            'user': str(user.id),
            'text': {
                'input': word,
                'output': word,
                'weight': weight
            }
        })



