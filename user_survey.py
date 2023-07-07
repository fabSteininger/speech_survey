import subprocess
from pynput import keyboard
from notifypy import Notify
notification = Notify()

program_process = None  
shortcut = False

def start_program():
    print("started")
    global program_process # Variable um Subprozess zu starten und zu stoppen
    program_process = subprocess.Popen(['python', 'user_survey_thread.py'])  # Starten vom Subprozess

def stop_program():
    global program_process
    if program_process:
        program_process.terminate() # Subprozess stoppen

def on_activate():
    global shortcut 
    if not shortcut:
        notification.title = "Spracherkennung gestartet"
        notification.message = "Es wird zugehört"
        notification.icon = "start.png"
        notification.send()
        start_program() # Starten der Spracherkennung (Subprozess)
        shortcut = True #Zustandsspeicher ob die Spracherkennung aktiviert wurde
    else:
        notification.title = "Spracherkennung gestoppt"
        notification.message = "Es wird nicht mehr zugehört"
        notification.icon = "stop.png"
        notification.send()
        shortcut = False
        stop_program() # Stoppen der Spracherkennung (Subprozess)

start_key = keyboard.HotKey(
    keyboard.HotKey.parse('<ctrl>+<alt>+l'),
    on_activate)

with keyboard.Listener(
        on_press=start_key.press,
        on_release=start_key.release
) as l:
    l.join() #siehe https://pynput.readthedocs.io/en/latest/keyboard.html
