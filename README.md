# Installation
tested with python 3.10.11
It is recommended to use a virtual environment
pip install -r requirements.txt

# Usage
For the several speech services an authentification is needed therefore create a keys.py file
WIT_AI_KEY = "YOUR_KEY"
IBM_KEY = "YOUR_KEY"
IBM_Instance = "YOUR_KEY"
AZURE_SPEECH_KEY = "YOUR_KEY"

### user_survey.py
select used speech recognition, in this case it is vosk, because it is an offline speech recognition download a model first and place it in a new folder "model" (default setting)
```python
def writer(recognizer,audio):
    recognized= vosk(audio)+" "
    if recognized !=" ":
        print(recognized)
        subprocess.run(["xdotool", "type", recognized])
```

### wer_test
Safe the audio files in the .flac format and the corresponding text as .txt. The filename of the .flac and the .txt shall be the same. 
all the results are saved into the results folder
```python
datasetPath = os.path.join('/home', 'path', 'Sprachdateien', 'test')
speechFilesFolder = os.path.join(datasetPath, 'audio')
textFilesFolder = os.path.join(datasetPath, 'text')
resultsFolder = os.path.join(datasetPath, 'result')
```