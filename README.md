# speech_survey
Files and Programms to evaluate actual speech-recognition engines

## Requirements
* Python 3.10 or higher
* Virtual Environment:
    * `pip install virtualenv`
    * `virtualenv speech_survey`
    * `masterarbeit\Scripts\activate`
* Speech Recognition Library: https://github.com/fabSteininger/speech_recognition 
    * **this has to be built manually, use the following commands:**
    * `pip install --upgrade setuptools`
    * `python setup.py install`
* All the other dependencies can be installed with the requirements.txt inside the virtual environment
    * `pip install -r requirements.txt`

## Configuration of the speech-recognition services
### Microsoft
For the usage an Azure-Account is required. Inside the Azure Portal a Speech-Service has to be generated.
With the Information of the Speech-Service the API can be connected, just enter the missing key inside the recognition.py
r.recognize_azure(audio, key=AZURE_SPEECH_KEY,language="de-AT", location="westeurope")[
### Wit.ai
### IBM 
### Vosk
### Sphinx
### Coqui