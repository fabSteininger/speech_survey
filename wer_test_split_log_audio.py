import csv
import os
from recognition import *
from datetime import date
import traceback
import time
from pydub import AudioSegment
from pydub.silence import split_on_silence
from natsort import natsorted
import shutil

# Pfadangabe Datensatz
datasetPath = os.path.join('/home', 'fabian', 'Sprachdateien', 'commonvoice')
speechFilesFolder = os.path.join(datasetPath, 'audio')
textFilesFolder = os.path.join(datasetPath, 'text')
resultsFolder = os.path.join(datasetPath, 'result')
audioExtension = ".flac"
textExtension = ".txt"


# Minimale Länge von den Audiostücken
target_length = 45 * 1000 # 45 seconds

# Variablen
speechRecognition = ""
results = []


# Lesen einer .txt-Datei
def readText(path):
    with open(path, 'r') as file:
        file_contents = file.read()
    return file_contents

def split(filepath, folder_name,target_length):
    sound = AudioSegment.from_file(filepath, format="flac")
    chunks = split_on_silence(
        sound,
        min_silence_len = 500,
        silence_thresh = sound.dBFS - 16,
        keep_silence = True, # optional
    )

    output_chunks = [chunks[0]]
    for chunk in chunks[1:]:
        if len(output_chunks[-1]) < target_length:
            output_chunks[-1] += chunk
        else:
            output_chunks.append(chunk)
    for i, chunk in enumerate(output_chunks):
      chunk_filename = os.path.join(folder_name, f"chunk{i}.flac")
      chunk.export(chunk_filename, format="flac")

# Alle Audiodateien mit der definierten Dateiendung in einer Liste speichern
speechFiles = [f for f in os.listdir(speechFilesFolder) if f.endswith(audioExtension)]

# Für alle diese Dateien die Spracherkennung ausführen
#audio_read = readAudio("test.flac")
#whisper(audio_read)
for x in speechFiles:
    try:
        audio_path = os.path.join(speechFilesFolder, x)
        chunk_folder=os.path.join(speechFilesFolder,os.path.splitext(x)[0])
        print(chunk_folder)
        os.mkdir(chunk_folder)
        print(audio_path)
        split(audio_path,chunk_folder,target_length)
    except Exception:
        traceback.print_exc()
        print("Can't read this file:", x)
        continue

    filename = os.path.splitext(x)[0]
    text_path = os.path.join(textFilesFolder, filename + textExtension)
    text_read = readText(text_path)

    if text_read is not None:
        chunkFiles = natsorted([f for f in os.listdir(chunk_folder) if f.endswith(audioExtension)])
        print(chunkFiles)
        speechRecognition=""
        start_time = time.time()
        for y in chunkFiles:
          audio_read=readAudio(os.path.join(chunk_folder,y))
          chunk = microsoft(audio_read)
          print(chunk)
          speechRecognition = speechRecognition + chunk
        end_time = time.time()
        shutil.rmtree(chunk_folder)
        wer, ground_truth, truth_reduced, hypothesis, hypothesis_reduced = evaluation(text_read, speechRecognition)
        used_time = end_time - start_time
        results.append((filename, wer, ground_truth, truth_reduced, hypothesis, hypothesis_reduced, used_time))
        print(x, "done...")
    else:
        print(x, "text file does not exist")
    
# Ergebnisse in eine CSV-Datei schreiben
result_file = str(date.today())
result_file = os.path.join(resultsFolder, result_file+"_microsoft_Landtag" + ".csv")

with open(result_file, 'w', encoding="UTF-8", newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["filename", "wer", "ground_truth", "truthReduced", "hypothesis", "hypothesisReduced", "time"])
    writer.writerows(results)

print("Die Datei wurde unter", result_file, "gespeichert")