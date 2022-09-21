#!/usr/bin/env python3
import json
import csv
import os
from recognition import *

#Folders with data, define for use case
textFilesFolder = os.path.join('TUDA-testdateien','JSON')
speechFilesFolder =os.path.join('TUDA-testdateien','Yamaha')
resultsFolder =os.path.join('TUDA-testdateien','Results')
audioExtension=".wav"
textExtension=".json"

# Find all the audio files inside the given directory
speechFiles = [f for f in os.listdir(speechFilesFolder) if f.endswith(audioExtension)]


# load audio and translate speech to text 
for x in speechFiles:
    try:
        audio_read=readAudio(os.path.join(speechFilesFolder,x))
    except:
        print (x+"file seems to be corrupted")
        continue