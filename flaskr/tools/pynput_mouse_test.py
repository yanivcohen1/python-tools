from pynput import keyboard
from pynput.keyboard import Key, Controller
from pyautogui import press, typewrite #, hotkey
from pynput.mouse import Button
from pynput import mouse
from pynput.mouse import Controller as MController
import pyperclip

class MyException(Exception): pass

def on_click(x, y, button, pressed):
    print('click', button, pressed, x, y)
    # if button == mouse.Button.left:
    #     raise MyException(button)

def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))

# Collect events until released
with mouse.Listener(
        on_click=on_click,
        on_move=on_move,
        on_scroll=on_scroll) as listener:
    try:
        listener.join()
    except MyException as e:
        print('{0} was clicked'.format(e.args[0]))
