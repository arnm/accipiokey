
from accipiokey.utils import *

def correction_event_handler(instance, correction_event):
    word_buffer = instance.wordEventDispatcher.word_buffer
    index = find_second_to_last(word_buffer, ' ')

    if not index:
        backspace_count = len(word_buffer)
        emulate_key_events(['backspace' for i in range(backspace_count)])
        key_events = list(correction_event)
        key_events.append(' ')
        print('Emulating: ', key_events)
        emulate_key_events(key_events)
        instance.wordEventDispatcher.word_buffer = key_events
    else:
        backspace_count = len(word_buffer[index+1:])
        emulate_key_events(['backspace' for i in range(backspace_count)])
        key_events = list(correction_event)
        key_events.append(' ')
        print('Emulating: ', key_events)
        emulate_key_events(key_events)
        instance.wordEventDispatcher.word_buffer = word_buffer[:backspace_count-1] + key_events
        print(instance.wordEventDispatcher.word_buffer)
