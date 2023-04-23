import speech_recognition as sr
import jiwer
import os
import keys
import sounddevice #mute the warnings of alsa in pyaudio

srImplemented=["sphinx", "google", "microsoft", "ibm", "vosk", "wit", "amazon", "whisper"]

r = sr.Recognizer()

def readAudio(Path):
    with sr.AudioFile(Path) as source:
        audio = r.record(source)  # read the entire audio file  
    return audio 

def listenAudio(microphoneIndex=2):
    with sr.Microphone(microphoneIndex) as source:
        r.adjust_for_ambient_noise(source)  
        print("Say something!")
        audio = r.listen(source)
    return audio

def evaluation(ground_truth: str, hypothesis: str):
    # to lower and remove punctuation the rest is by default for calculating WER efficient
    transformation = jiwer.Compose(
        [
            jiwer.ToLowerCase(), 
            jiwer.RemovePunctuation(),
            # jiwer default to get into the right format for calculating
            jiwer.RemoveMultipleSpaces(),
            jiwer.Strip(),
            jiwer.ReduceToListOfListOfWords()
        ]
    )
    # use the jiwer compose method to make the same transformations than jiwer
    truthReduced=' '.join(jiwer.Compose.__call__(transformation,text=ground_truth)[0])
    hypothesisReduced=' '.join(jiwer.Compose.__call__(transformation,text=hypothesis)[0])
    wer = jiwer.wer(ground_truth, hypothesis,truth_transform=transformation, hypothesis_transform=transformation)
    return wer, ground_truth, truthReduced, hypothesis, hypothesisReduced

def sphinx(audio):
    recogniced=""
    try:
        recogniced = r.recognize_sphinx(audio, language="de-DE")
        print("sphinx")
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    return recogniced

def google(audio):
    recogniced=""
    try:
        recogniced=r.recognize_google(audio, language="de-AT")[0]
        print("google")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))   
    return recogniced

def wit(audio):
    recogniced=""
    try:
        recogniced = r.recognize_wit(audio, key=keys.WIT_AI_KEY)
        print("wit")
    except sr.UnknownValueError:
        print("Wit could not understand audio")
    except sr.RequestError as e:
        print("Wit error; {0}".format(e))
    return recogniced

def ibm(audio):
    recogniced=""
    try:
        recogniced=r.recognize_ibm(audio, key=keys.IBM_KEY,instance=keys.IBM_Instance, model="de-DE_NarrowbandModel")[0]
        print("ibm")
    except sr.UnknownValueError:
        print("IBM Speech to Text could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from IBM Speech to Text service; {0}".format(e))
    return recogniced

def vosk(audio):
    recogniced=""
    try:
        recogniced = r.recognize_vosk(audio, modelPath="model")
        print("vosk")
    except sr.UnknownValueError:
        print("Vosk could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Vosk service; {0}".format(e))
    return recogniced

def microsoft(audio):
    recogniced=""
# recognize speech using Microsoft Azure Speech
     # Microsoft Speech API keys 32-character lowercase hexadecimal strings
    try:
        recogniced=r.recognize_azure(audio, key=keys.AZURE_SPEECH_KEY,language="de-AT", location="westeurope")[0]
        print("microsoft")
    except sr.UnknownValueError:
        print("Microsoft Azure Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Microsoft Azure Speech service; {0}".format(e))
    return recogniced

def whisper(audio):
    recogniced=""
    try:
        recogniced=r.recognize_whisper(audio,model="small", language="german")
        print("whisper")
    except sr.UnknownValueError:
        print("Whisper could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper service; {0}".format(e))
    return recogniced

def amazon(audio):
    recogniced=""
    try:
        recogniced=r.recognize_amazon(audio,region="eu-west-1")
        print("Amazon")
    except sr.UnknownValueError:
        print("Amazon could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Amazon service; {0}".format(e))
    return recogniced  
