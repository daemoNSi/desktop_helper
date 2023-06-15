import time
import keyboard
import pyperclip
from WordsToDocs import insert_to_doc, jisho_search, lookup_word


while True:
    try:
        add_word = pyperclip.paste()
        if keyboard.is_pressed('ctrl+b'):
            jisho_search(add_word)
            time.sleep(1)
        elif keyboard.is_pressed('ctrl+q'):
            insert_to_doc(add_word)
            time.sleep(1)
        # elif keyboard.is_pressed('ctrl+i'):
        #     duplicate_check(add_word)
        #     time.sleep
        elif keyboard.is_pressed('ctrl+k'):
            lookup_word()
            time.sleep(1)
    except:
        break
