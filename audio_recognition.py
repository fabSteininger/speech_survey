#!/usr/bin/env python3
import json
import csv
import os
from recognition import *
from datetime import date
import traceback


#Folders with data, define for use case
textFilesFolder = os.path.join('TUDA-testdateien','JSON')
speechFilesFolder =os.path.join('TUDA-testdateien','Test')
resultsFolder =os.path.join('TUDA-testdateien','Results')
audioExtension=".wav"
textExtension=".json"

# Empty list to save results
results=[]

# Find all the audio files inside the given directory
speechFiles = [f for f in os.listdir(speechFilesFolder) if f.endswith(audioExtension)]

# read the corresponding text files to the speech files
def readText(Path):
    try:
        with open(Path, encoding="UTF-8") as file:
            data=json.load(file)
            text = data["cleaned_sentence"]  
            location = data["bundesland"]  
            gender = data["gender"]
            motherTongue= data["muttersprachler"]
            speakerId=data["speaker_id"]
            speakerDetails=(location,gender,motherTongue,speakerId)
        return text, speakerDetails
    except:
        return None

def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1
    return path

# load audio and translate speech to text 
for x in speechFiles:
    try:
        audio_read=readAudio(os.path.join(speechFilesFolder,x))
    except Exception:
        traceback.print_exc()
        print("can't read this file: "+ x )
        continue
    text_read=readText(os.path.join(textFilesFolder,x.split('_')[0]+textExtension))
    if(text_read!=None):
        #------------------------------------------------------------------
        # Speech Engine change here
        speechRecognition=wit(audio_read)
        wer=evaluation(text_read[0],speechRecognition)
        results.append(wer+text_read[1])
        print(x+" done...")
    else:
        print(x+" text file not existing")

# write filename (=date) and a unique number to avoid overwriting files
filename = str(date.today())
filename = filename+".csv"
filename= uniquify(os.path.join(resultsFolder,filename))


# write results into text file
with open(filename,'w',encoding="UTF-8",newline='') as file:
    writer = csv.writer(file)
    for row in results:
        writer.writerow(row)

print("Die Datei wurde unter "+os.path.join(resultsFolder,filename)+" gespeichert")