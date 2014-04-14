
# TODO: fix this hack
def keycode_to_unicode(keycode): return keycode.replace('KEY_', '').lower()

# TODO: fix this hack
def unicode_to_keycode(unicode):
    if unicode == ' ':
        return 'KEY_' + 'space'.upper()
    return 'KEY_' + unicode.upper()

# TODO: fix this hack
def emulate_key_events(unicodes):
    for uni in unicodes:
        keycode = unicode_to_keycode(uni)
        with UInput() as uinput:
            exec('uinput.write(ecodes.EV_KEY, ecodes.' + keycode + ', 1)')
            exec('uinput.write(ecodes.EV_KEY, ecodes.' + keycode + ', 0)')
            uinput.syn()
