
from accipiokey.utils import *
from accipiokey.dispatchers import WordEventDispatcher

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
        instance.wordEventDispatcher.word_buffer = word_buffer[:backspace_count-1]
        if not instance.wordEventDispatcher.word_buffer[-1] == ' ':
            instance.wordEventDispatcher.word_buffer.append(' ')
        [instance.wordEventDispatcher.word_buffer.append(key_event) for key_event in key_events]

def shortcut_event_handler(instance, shortcut_event):
    snippets = {'lol':'laugh out loud', 'brb':'be right back', 'tbh':'to be honest'}
    wed = WordEventDispatcher.instance()

    if wed.word_event in list(snippets.keys()):
        word_buffer = wed.word_buffer
        index = find_second_to_last(word_buffer, ' ')

        if not index:
            backspace_count = len(wed.word_event)
            emulate_key_events(['backspace' for i in range(backspace_count)])
            key_events = list(snippets[wed.word_event])
            key_events.append(' ')
            print('Emulating: ', key_events)
            emulate_key_events(key_events)
            wed.word_buffer = key_events
        else:
            backspace_count = len(wed.word_event)
            emulate_key_events(['backspace' for i in range(backspace_count)])
            key_events = list(snippets[wed.word_event])
            key_events.append(' ')
            print('Emulating: ', key_events)
            emulate_key_events(key_events)
            wed.word_buffer = word_buffer[:backspace_count-1]
            if not wed.word_buffer[-1] == ' ':
                wed.word_buffer.append(' ')
            [wed.word_buffer.append(key_event) for key_event in key_events]
