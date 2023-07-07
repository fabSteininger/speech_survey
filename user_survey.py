import subprocess
from pynput import keyboard
from notifypy import Notify
notification = Notify()

program_process = None  # Global variable to store the program process
shortcut = False

def start_program():
    print("started")
    global program_process
    program_process = subprocess.Popen(['python', 'user_survey_thread.py'])  # Replace with the actual name of your Python program file

def stop_program():
    global program_process
    if program_process:
        program_process.terminate()

def on_activate():
    global shortcut 
    if not shortcut:
        notification.title = "Spracherkennung gestartet"
        notification.message = "Es wird zugehört"
        notification.icon = "start.png"
        notification.send()
        start_program()
        shortcut = True
    else:
        notification.title = "Spracherkennung gestoppt"
        notification.message = "Es wird nicht mehr zugehört"
        notification.icon = "stop.png"
        notification.send()
        shortcut = False
        stop_program()

start_key = keyboard.HotKey(
    keyboard.HotKey.parse('<ctrl>+<alt>+l'),
    on_activate)

with keyboard.Listener(
        on_press=start_key.press,
        on_release=start_key.release
) as l:
    l.join()
