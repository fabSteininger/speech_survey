from threading import Thread
from queue import Queue
import subprocess
import speech_recognition as sr
from recognition import whisper_api
import time
from pynput.keyboard import Key, Controller

r = sr.Recognizer()
audio_queue = Queue()
keyboard = Controller()

def recognize_worker():
    # läuft in einem Hintergrund-Thread
    while True:
        audio = audio_queue.get()  
        if audio is None: break  
        recognized=whisper_api(audio)
        if recognized == "" or recognized.isspace():
            pass  # Falls "" oder " " als Ergebnis der Spracherkennung retour kommt sollte nichts passieren
        elif "Untertitel" in recognized:
        # Irgendwie Halluziniert die API etwas mit Untertitel der Amara.org-Community deshalb wird dieser Satz rausgefiltert
            pass
        elif "Vielen Dank für" in recognized:
        # Halluzination der API in allen Sprachen Vielen Dank fürs zusehen
            pass
        else:
            keyboard.type(recognized+' ')
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
        