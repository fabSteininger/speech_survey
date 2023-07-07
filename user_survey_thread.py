from threading import Thread
from queue import Queue
import subprocess
import speech_recognition as sr
from recognition import wit
import time

r = sr.Recognizer()
audio_queue = Queue()

def recognize_worker():
    # läuft in einem Hintergrund-Thread
    while True:
        audio = audio_queue.get()  
        if audio is None: break  
        recognized=wit(audio)
        if recognized == "" or recognized.isspace():
            pass  # Falls "" oder " " als Ergebnis der Spracherkennung retour kommt sollte nichts passieren
        else:
            subprocess.run(["xdotool", "type", recognized+' ']) # Ansonsten erkannter Text + Leerzeichen 
            print("Output:" + recognized)

        audio_queue.task_done()


# Einen neuen Thread um die Spracherkennung auszuführen. Das Hauptprogramm verarbeitet währenddessen die eingehenden Mikrofondaten

recognize_thread = Thread(target=recognize_worker)
recognize_thread.daemon = True
recognize_thread.start()
subprocess.run(["setxkbmap", "de"]) #Sichergehen ob richtiges Tastaturlayout eingestellt ist

with sr.Microphone(sample_rate=16000) as source:
    r.adjust_for_ambient_noise(source)  # Für Umgebungsgeräusche kalibiereren
    while True:  # Entstehende Daten dem Thread der Spracherkennung hinzufügen
        audio_queue.put(r.listen(source))
        