from configparser import ConfigParser
from pathlib import Path
import json
import torch
path = Path(__file__).absolute().parent
CONFIG_FILE = f"{path}\Assets\Data\Config.ini"
config = ConfigParser()
config.read(CONFIG_FILE)

with open(f'{path}\Assets\Data\intents.json', 'r') as json_file:
    intents = json.load(json_file)

with open(f'{path}\Assets\Data\Settings.json', 'r') as json_file:
    settings = json.load(json_file)

class Djson:
    def content():
        with open(f'{path}\Assets\Data\Settings.json', 'r') as json_file:
            content = json.load(json_file)
            return content
    
    def save_to_file(content,indent: int = 3):
        with open(f'{path}\Assets\Data\Settings.json', 'w') as json_file:
            json.dump(content,json_file,indent=indent)

class Saved_Apps:
    AllDict = config.items("APPS",True,None)
    Apps = config.options("APPS")
    Options = ([config["APPS"][App] for App in Apps])

class Settings:
    settings = settings["settings"]

class voice_properties:
    GTTS_settings = settings["voice_properties"]["GTTS_settings"]
    PYTTSX3_settings = settings["voice_properties"]["PYTTSX3_settings"]

class sys_data:
    input_devices = settings["sys_data"]["input_devices"]
    output_devices = settings["sys_data"]["output_devices"]

class Notifications:
    Starting = [Value for Value in settings["sys_notifications"] if Value["OptionDest"] == "Starting"][0]
    PreListening = [Value for Value in settings["sys_notifications"] if Value["OptionDest"] == "PreListening"][0]
    NotUnderstand = [Value for Value in settings["sys_notifications"] if Value["OptionDest"] == "NotUnderstand"][0]
    RunningTime = [Value for Value in settings["sys_notifications"] if Value["OptionDest"] == "RunningTime"][0]


class AlphabetV2:
    Intents = intents
    Allintents = intents["intents"]
    Allpatterns = [i["patterns"] for i in Allintents]
    LenIntents = len(intents)
    Lenpatterns = len(Allpatterns)
    Caller = intents["Types of Callers"]["Callers"]
    CustomCallers = intents["Types of Callers"]["Custom Callers"]
    AllCallers = Caller + CustomCallers

    #----------------------------------------------------------------

    DATA_FILE =f"{path}\Assets\Data\data.pth"
    data = torch.load(DATA_FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]
