import speech_recognition as sr
import jiwer
import os
import keys
import sounddevice #Stummschalten der Warnungen von alsa in pyaudio
from text_to_num import alpha2digit
import subprocess

srImplemented=["sphinx", "google", "microsoft", "ibm", "vosk", "wit", "amazon", "whisper"]

r = sr.Recognizer()


def readAudio(Path):
    with sr.AudioFile(Path) as source:
        audio = r.record(source)  
    return audio 

def listenAudio():
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)  
    stop_listening = r.listen_in_background(m, writer)
    # Layout Deutsch
    subprocess.run(["setxkbmap", "de"])
    return stop_listening

def stoplistenAudio(stop_listening):
    stop_listening(wait_for_stop=True)

def writer(recognizer,audio):
    recognized= google(audio)+" "
    if recognized !=" ":
        print(recognized)
        subprocess.run(["xdotool", "type", recognized])
  
def del_umlaute(text: str) -> str:
    """ Umlaute umwandeln 
    ä -> ae, Ä -> Ae...
    ü -> ue, Ü -> Ue...
    ö -> oe, Ö -> Oe...
    ß -> ss
    """
    vowel_char_map = {
        ord('ä'): 'ae', ord('ü'): 'ue', ord('ö'): 'oe', ord('ß'): 'ss',
        ord('Ä'): 'Ae', ord('Ü'): 'Ue', ord('Ö'): 'Oe'
    }
    return text.translate(vowel_char_map)

def evaluation(ground_truth: str, hypothesis: str):
    # Satzzeichen entfernen und alles Kleinschreiben
    truthReduced=del_umlaute(ground_truth)
    hypothesisReduced=del_umlaute(hypothesis)
    try:
        truthReduced=alpha2digit(truthReduced,"de",ordinal_threshold=0)
        hypothesisReduced=alpha2digit(hypothesisReduced,"de",ordinal_threshold=0)
    except:
        print("alpha2digit has some error")

    transformation = jiwer.Compose(
        [
            jiwer.ToLowerCase(), 
            jiwer.RemovePunctuation(),
            jiwer.RemoveKaldiNonWords(),
            # jiwer Standard
            jiwer.RemoveMultipleSpaces(),
            jiwer.Strip(),
            jiwer.ReduceToListOfListOfWords()
        ]
    )
    
    truthReduced=' '.join(jiwer.Compose.__call__(transformation,text=truthReduced)[0])
    hypothesisReduced=' '.join(jiwer.Compose.__call__(transformation,text=hypothesisReduced)[0])

    wer = jiwer.wer(truthReduced, hypothesisReduced)
    return wer, ground_truth, truthReduced, hypothesis, hypothesisReduced

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

def google_cloud(audio):
    recogniced=""
    try:
        recogniced=r.recognize_google_cloud(audio, credentials_json="credentials_google.json",language="de-DE")
        print("google")
    except sr.UnknownValueError:
        print("Google Cloud Speech API could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech API service; {0}".format(e))   
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
        recogniced=r.recognize_ibm(audio, key=keys.IBM_KEY,instance=keys.IBM_Instance, model="de-DE_Multimedia")[0]
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
        recogniced=r.recognize_whisper(audio,model="large-v2", language="german")
        print("whisper")
    except sr.UnknownValueError:
        print("Whisper could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper service; {0}".format(e))
    return recogniced

def whisper_api(audio):
    recogniced=""
    try:
        recogniced=r.recognize_whisper_api(audio,key=keys.OPEN_AI)
        print(recogniced)
        print("whisper")
    except sr.UnknownValueError:
        print("Whisper could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper service; {0}".format(e))
    return recogniced   

def amazon(audio):
    recogniced=""
    try:
        recogniced=r.recognize_amazon(audio,bucket_name="speechfabi")
        print("Amazon")
    except sr.UnknownValueError:
        print("Amazon could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Amazon service; {0}".format(e))
    return recogniced  
