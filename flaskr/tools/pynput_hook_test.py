from pynput import keyboard
from pynput.keyboard import Key, Controller
from pyautogui import press, typewrite #, hotkey
from pynput.mouse import Button
from pynput import mouse
from pynput.mouse import Controller as MController
import pyperclip

keyboard_c = Controller()
mouse_c = MController()

def on_activate():
    print(f'The current pointer position is {mouse_c.position}')
    clipbord = pyperclip.paste()
    typewrite(clipbord)
    # keyboard_c.type('HellOo1 World')

def for_canonical(f):
    return lambda k: f(l.canonical(k))

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<F8>'),
    on_activate)
with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as l:
    l.join()
