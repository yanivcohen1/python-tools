from pynput import keyboard
from pynput.keyboard import Key, Controller
import time

keyboard2 = Controller()

def on_activate():
    print('Global hotkey activated!')
    time.sleep(1)
    keyboard2.type('Hello World')
    keyboard2.press(Key.enter)

def for_canonical(f):
    return lambda k: f(l.canonical(k))

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<ctrl>+<alt>+h'),
    on_activate)
with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as l:
    l.join()
