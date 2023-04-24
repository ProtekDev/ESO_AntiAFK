from datetime import datetime, time
import random
import time
import threading
import os
from pynput.mouse import Listener as MouseListener, Controller as MouseController, Button
from pynput.keyboard import Listener as KeyboardListener, KeyCode, Controller as KeyboardController
import psutil
from pywinauto import Application

# https://pypi.org/project/pynput/
last_input = datetime.now()
ingame_key = KeyCode(char=".")
process_name = "eso64"

print_debug = True
mouse = MouseController()
keyboard = KeyboardController()


def check_process():
    for process in psutil.process_iter():
        try:
            if process_name.lower() in process.name().lower():
                return True
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    else:
        return False


def process_to_foreground():
    proc_alive = check_process()
    if proc_alive:
        app = Application().connect(path=process_name)
        app.top_window().set_focus()
    else:
        print("Process is not alive")


def worker():
    global last_input
    while True:
        proc_alive = check_process()
        if proc_alive:
            datetime_diff = datetime.now() - last_input
            if datetime_diff.seconds >= 5*60:
                process_to_foreground()
                time.sleep(0.3)
                print("Detected Inactivity -> prevent disconnect")
                keyboard.press(ingame_key)
                time.sleep(0.1)
                keyboard.release(ingame_key)
                last_input = datetime.now()
            else:
                os.system('cls')
                print(f"last input: {last_input}")
        else:
            print("Process not alive ! Macro waiting")

        time.sleep(random.uniform(50, 59))


def keyboard_on_press(key):
    global last_input
    last_input = datetime.now()


def mouse_on_click(x, y, button, pressed):
    global last_input
    last_input = datetime.now()


def mouse_on_move(x, y):
    global last_input
    last_input = datetime.now()


os.system("title ESO - Anti AFK Helper")
print(f"ESO - Anti AFK Helper")
print(f"This will automatically press any Key (open Backpack), to prevent AFK Kick.")
print("When no Keyboard or Mouseinput was recognitioned for longer than 5 Minutes !")

worker_thread = threading.Thread(target=worker)
worker_thread.start()

keyboard_on_press_listener = KeyboardListener(on_press=keyboard_on_press)
mouse_click_listener = MouseListener(on_click=mouse_on_click)
mouse_on_move_listener = MouseListener(on_move=mouse_on_move)

keyboard_on_press_listener.start()
mouse_click_listener.start()
mouse_on_move_listener.start()

keyboard_on_press_listener.join()
mouse_click_listener.join()
mouse_on_move_listener.join()
