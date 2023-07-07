from threading import Thread
from queue import Queue
import subprocess
import speech_recognition as sr
from recognition import google

r = sr.Recognizer()
audio_queue = Queue()

def recognize_worker():
    # läuft in einem Hintergrund-Thread
    while True:
        audio = audio_queue.get()  # retrieve the next audio processing job from the main thread
        if audio is None: break  # stop processing if the main thread is done
        try:
            recognized=google(audio)
            if recognized == "" or recognized.isspace():
                pass  # Do nothing
            else:
                subprocess.run(["xdotool", "type", recognized+' '])
                print("Google Speech Recognition thinks you said:" + recognized)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        audio_queue.task_done()  # mark the audio processing job as completed in the queue


# Einen neuen Thread um die Spracherkennung auszuführen. Das Hauptprogramm verarbeitet währenddessen die eingehenden Mikrofondaten
recognize_thread = Thread(target=recognize_worker)
recognize_thread.daemon = True
recognize_thread.start()
subprocess.run(["setxkbmap", "de"])

with sr.Microphone() as source:
    while True:  # Entstehende Daten dem Thread der Spracherkennung hinzufügen
        audio_queue.put(r.listen(source))