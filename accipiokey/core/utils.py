from accipiokey.core import settings
from accipiokey.core.mappings import *
from accipiokey.core.logger import Logger
from elasticsearch.helpers import bulk
from elasticutils import get_es, S
from evdev import ecodes, UInput
from textblob import TextBlob

# TODO: fix this hack
def keycode_to_unicode(keycode): return keycode.replace('KEY_', '').lower()

# TODO: fix this hack
def unicode_to_keycode(unicode):
    if unicode == ' ':
        return 'KEY_' + 'space'.upper()
    if unicode == 'Alt':
        return 'KEY_LEFTALT'
    if unicode == 'Ctrl':
        return 'KEY_LEFTCTRL'
    return 'KEY_' + unicode.upper()

# TODO: could be more efficient (UInput could remain open)
def emulate_key_events(unicodes):
    with UInput() as uinput:
        for uni in unicodes:
            keycode = unicode_to_keycode(uni)
            exec('uinput.write(ecodes.EV_KEY, ecodes.' + keycode + ', 1)')
            exec('uinput.write(ecodes.EV_KEY, ecodes.' + keycode + ', 0)')
            uinput.syn()

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
    for text in map(normalize_func, words):
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

# TODO: could be more efficient
def process_writing(writing, normalize_func=lambda s: s.lower().rstrip()):
    content = TextBlob(writing.content)
    unindexed_words = []

    for word in map(normalize_func, content.words):
        if get_word(writing.user, word):
            increment_word_weight(writing.user, word)
        else:
            Logger.info('Writing Processor: Word Not Indexed (%s)', word)
            if word not in unindexed_words:
                unindexed_words.append(word)
            else:
                Logger.info('Writing Processor: Indexing (%s)', unindexed_words)
                index_new_words(writing.user, unindexed_words)
                del unindexed_words[:]

    if unindexed_words:
        Logger.info('Writing Processor: Indexing (%s)', unindexed_words)
        index_new_words(writing.user, unindexed_words)

