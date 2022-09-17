#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class
from recognition import *
import pywebio.input as webin
import pywebio.output as webout
import pandas as pd
import os
import random

#Folders with data, define for use case
sentencesFile = os.path.join('survey','sentences','sentences.csv')
# List for saving the results
results=[]
xSR=0

# switch between the different speech recognition engines
def useSR(speechRecognition, audio):
    print(speechRecognition)
    if speechRecognition=="sphinx":
        recogniced=vosk(audio)
    elif speechRecognition=="coqui":
        recogniced=coqui(audio)
    elif speechRecognition=="google":
        recogniced=google(audio)
    elif speechRecognition=="microsoft":
        recogniced=microsoft(audio)
    elif speechRecognition=="ibm":
        recogniced=ibm(audio)
    elif speechRecognition=="vosk":
        recogniced=vosk(audio)
    elif speechRecognition=="wit":
        recogniced=wit(audio)
    return recogniced
   
def listen(speechEngine, sentence):
    input='Mir ist ein Fehler passiert, bitte wiederholen'
    while input == 'Mir ist ein Fehler passiert, bitte wiederholen':
        webout.put_markdown("# "+sentence)
        audio=listenAudio(microphoneIndex=2)
        recogniced=useSR(speechEngine,audio)
        webout.put_markdown("# "+recogniced)
        input=webin.radio("Wie gut findest du die Ausgabe der Spracherkennung: ", options=['Sehr gut', 'Gut', 'Mittelmäßig', 'Schlecht', 'Grausam','Mir ist ein Fehler passiert, bitte wiederholen'])
        webout.clear()
    return (audio, input)

def randomizeSR(index):
    indexrest=divmod(index,len(srImplemented))[1]
    if indexrest==0:
        random.shuffle(srImplemented)
    return srImplemented[indexrest]

# read csv sentences
data = pd.read_csv(sentencesFile, sep=";")

#converting column data to list
sorter=data['#'].tolist()
sentence=data['sentence'].tolist()

random.shuffle(sorter)
print(sorter)
# Uncomment to find microphone that should be used
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

info = webin.input_group("Daten über dich",[
  webin.select('Alter',options=['11-20','21-30', '31-40','41-50','51-60','61-70', '71-80','81-90','91-100'], name='age'),
  webin.select("Geschlecht", options=['Weiblich', 'Männlich', 'Divers'], name='gender'),
  webin.input("Aus welchen Bundesland kommst Du?",name='bundesland'),
  webin.select("Ist Deutsch deine Muttersprache?",options=['Ja', 'Nein'],name='muttersprache')
])

for i in sorter:
    speechEngine=randomizeSR(xSR)
    res=listen(speechEngine,sentence[i])
    print(res[1])
    xSR=xSR+1

webout.put_markdown('# Vielen Dank!')
webout.put_image('https://c.tenor.com/CwQVw9XUhwwAAAAC/smooch-blow-kiss.gif')  # internet image 


