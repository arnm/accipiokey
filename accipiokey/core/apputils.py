from accipiokey.core.mappings import WordMappingType
from elasticutils import S
from evdev import ecodes, UInput

# TODO: fix this hack
def keycode_to_unicode(keycode): return keycode.replace('KEY_', '').lower()

# TODO: fix this hack
def unicode_to_keycode(unicode):
    if unicode == ' ':
        return 'KEY_' + 'space'.upper()
    return 'KEY_' + unicode.upper()

# TODO: fix this hack
# TODO: could be more efficient (UInput could remain open)
def emulate_key_events(unicodes):
    with UInput() as uinput:
        for uni in unicodes:
            keycode = unicode_to_keycode(uni)
            exec('uinput.write(ecodes.EV_KEY, ecodes.' + keycode + ', 1)')
            exec('uinput.write(ecodes.EV_KEY, ecodes.' + keycode + ', 0)')
            uinput.syn()

def check_if_indexed(user, word):
    searcher = S(WordMappingType)
    word_search_result = searcher.query(
        user__term=str(user.id),
        text__term=str(word),
        must=True)

    # if word is indexed there should only be one instance of that word
    if word_search_result.count(): return True
    return False
