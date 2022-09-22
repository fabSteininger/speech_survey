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
The keys for the services are placed inside a keys.py file, therefore creating this file is mandatory.
```
WIT_AI_KEY = "Your Wit.ai key"
IBM_KEY = "Your IBM Key"
IBM_Instance = "Your IBM Instance"
AZURE_SPEECH_KEY = "Your Azure Key" 
```
### Microsoft
For the usage an Azure-Account is required.\
Inside the Azure Portal a Speech-Service has to be generated.\
With the Information of the Speech-Service the API can be connected, just enter the missing key inside the keys.py file\
`r.recognize_azure(audio, key=AZURE_SPEECH_KEY,language="de-AT", location="westeurope")`
### Wit.ai
For the usage an Facebook account is mandatory.\
Create a new app to get the API Key.
### IBM 
For the usage of the IBM service an account is required. The account usually needs a credit card, by the usage of the official course licenses in the MOOC platforms, the usage without any credit card is possible.
### Vosk
The installation of Vosk is done with the requirements. The model can be downloaded from the webpage of the project [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)
### Sphinx
The Sphinx model should already be available through the installation of the Speech Recognition Library: https://github.com/fabSteininger/speech_recognition 
otherwise the model can be downloaded from: https://sourceforge.net/projects/cmusphinx/
### Coqui
The [following model](https://coqui.ai/german/AASHISHAG/v0.9.0) was tested, but it should be possible to use every deepspeech model with a tflite file.
Place the model file inside the specified path:
`r.recognize_coqui(audio, language="de-DE",model_base_dir=os.path.join("coqui-data"))`
# Output
Following header in the csv is used 
|   wer   |   ground_truth   |   truthReduced   |   hypothesis   |   hypothesisReduced   |   location   |   gender   |   mother tongue   |   speaker ID   |
| ------- |:----------------:| ----------------:| --------------:| ---------------------:| ------------:| ----------:| -----------------:| --------------:|
|   word error rate   |   text that was read   |   text without case sensitivity,...  |   recognized text   |   recongnized text without case sensitivity,....  |   home region of the speaker   |   gender   |   mother tongue   |   UUID of speaker   |