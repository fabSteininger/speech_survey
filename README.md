# Installation
Tested with python 3.10.11  

Following packages are needed on Ubuntu 23.10 and additionally a programm that uses xwayland like the browsers firefox (tested on version 115) and chrome (tested on version 114)
```unix
sudo apt install portaudio19-dev
```
It is recommended to use a virtual environment  
```python
python -m venv speechRecognition
source speechRecognition/bin/activate
```
Install the requirements.txt
```python
pip install -r requirements.txt
```
# Usage
For the several speech services an authentification is needed therefore create a keys.py file  
```
WIT_AI_KEY = "YOUR_KEY"
IBM_KEY = "YOUR_KEY"
IBM_Instance = "YOUR_KEY"
AZURE_SPEECH_KEY = "YOUR_KEY
```
For the Google Cloud Speech-to-Text Service also credentials are needed - create the json credentals under IAM & Admin / Service Accounts
Place them in the folder of the user_survey.py and wer_test.py with the file name "credentials_google.json"

For the usage of AWS authenticate with: 
```
aws configure
```
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