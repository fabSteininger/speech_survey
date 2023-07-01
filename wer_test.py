import csv
import os
from recognition import *
from datetime import date
import traceback
import time

# Pfadangabe Datensatz
datasetPath = os.path.join('/home', 'fabian', 'Sprachdateien', 'test')
speechFilesFolder = os.path.join(datasetPath, 'audio')
textFilesFolder = os.path.join(datasetPath, 'text')
resultsFolder = os.path.join(datasetPath, 'result')
audioExtension = ".flac"
textExtension = ".txt"

# Variablen
speechRecognition = ""
results = []


# Lesen einer .txt-Datei
def readText(path):
    with open(path, 'r') as file:
        file_contents = file.read()
    return file_contents


# Alle Audiodateien mit der definierten Dateiendung in einer Liste speichern
speechFiles = [f for f in os.listdir(speechFilesFolder) if f.endswith(audioExtension)]
# Für alle diese Dateien die Spracherkennung ausführen
for x in speechFiles:
    try:
        audio_path = os.path.join(speechFilesFolder, x)
        audio_read = readAudio(audio_path)
    except Exception:
        traceback.print_exc()
        print("Can't read this file:", x)
        continue

    filename = os.path.splitext(x)[0]
    text_path = os.path.join(textFilesFolder, filename + textExtension)
    text_read = readText(text_path)

    if text_read is not None:
        start_time = time.time()
        speechRecognition = whisper_api(audio_read)
        end_time = time.time()

        wer, ground_truth, truth_reduced, hypothesis, hypothesis_reduced = evaluation(text_read, speechRecognition)
        used_time = end_time - start_time
        results.append((filename, wer, ground_truth, truth_reduced, hypothesis, hypothesis_reduced, used_time))
        print(x, "done...")
    else:
        print(x, "text file does not exist")

# Ergebnisse in eine CSV-Datei schreiben
result_file = str(date.today())
result_file = os.path.join(resultsFolder, result_file+"_whisper" + ".csv")

with open(result_file, 'w', encoding="UTF-8", newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["filename", "wer", "ground_truth", "truthReduced", "hypothesis", "hypothesisReduced", "time"])
    writer.writerows(results)

print("Die Datei wurde unter", result_file, "gespeichert")
