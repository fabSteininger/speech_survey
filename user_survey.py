from pynput import keyboard
#für Windows evtl.
#from pywinauto import keyboard as win_keyboard
from recognition import *
from notifypy import Notify
notification = Notify()

shortcut = False
stop =None

def on_activate():
    global shortcut 
    global stop
    if not shortcut:
        notification.title = "Spracherkennung gestartet"
        notification.message = "Es wird zugehört"
        notification.icon = "start.png"
        notification.send()
        stop = listenAudio()
        shortcut = True

    else:
        notification.title = "Spracherkennung gestoppt"
        notification.message = "Es wird nicht mehr zugehört"
        notification.icon = "stop.png"
        notification.send()
        shortcut = False
        stoplistenAudio(stop)
        stop=None

start_key = keyboard.HotKey(
    keyboard.HotKey.parse('<ctrl>+<alt>+l'),
    on_activate)

with keyboard.Listener(
        on_press=start_key.press,
        on_release=start_key.release
) as l:
    l.join()
