from datastructures import Djson, AlphabetV2, path
import speech_recognition as sr
from speech_recognition import Microphone, Recognizer
from time import sleep
from datetime import datetime

#Instance = Listen_in_Background(Question="Cosa posso fare per te?",device_index=Device_Index)

#sleep(10)
#Input = Stop_Listener(Instance)
#print(Input)

def get_device_index(device_name: str):
    Devices = [(index, name) for index, name in enumerate(Microphone.list_microphone_names())]
    Working_Devices = [index for index in Microphone.list_working_microphones()]

    Index = [i for i,n in Devices if n == device_name and i in Working_Devices]

    return Index[0]

def Listening(
                *args,
                spkrclass = None,
                Question : str = None,
                CallerNeeded : bool = True,
                Repeat : int = -1,
                device = "None",
                sample_rate : int = 48000,
                chunk_size : int = 1024):
    ###################################################################
    """
    "Question" ('str') = it is a string of a question that the program poses to the user (Default 'None').

    "CallerNeeded" ('bool') = specifies whether the bot name is needed to listen to the request (Default 'True').

    "Repeat" ('int') = specifies the number of times [ 1, 2, 3, ...] the bot will try to listen for an input (default [-1]).
        if set to [-1], the bot will keep listening until it gets acceptable input.

    "device_index" ('int') = specifies the device index of the device. (Default [0])

    "sample_rate" ('float') = specifies the sample rate of the device (Default [48000]).

    "chunk_size" ('int') = specifies the size of the chunk of the device (Default [1024]).

    Return Input 

    """
    ###################################################################
    content = Djson.content()
    
    Input = None
    confidence = None

    r = Recognizer()


    if type(device) == str:
        if device != 'None': device_index = get_device_index(device)
        else: device_index = 0
    elif type(device) == int:
        device_index = device

    if Repeat != -1: Repeated = 0
    else: Repeated = -2

    while Input == None and Repeated < Repeat:
        try:
            with Microphone(device_index=device_index, sample_rate=sample_rate, chunk_size=chunk_size) as source:
                r.adjust_for_ambient_noise(source, duration=0.7)
                r.pause_threshold = 0.5
                r.dynamic_energy_threshold = True
                
                try:
                    if Question != None and content["settings"]["use_gtts_voice_setting"]:
                        lenght, _ = spkrclass.say(Question)
                        sleep(int(round(lenght,0)))

                    audio = r.listen(source,timeout=None,phrase_time_limit=5)
                    data = r.recognize_google(audio,language="it-IT",pfilter=0,show_all=True,with_confidence=True)

                except Exception as e:
                    print(e)
                    Input = None
                    confidence = None
                else:
                    if len(data) != 0:
                        Input = (data['alternative'][0]['transcript']).lower()
                        confidence = (data['alternative'][0]['confidence'])
                    else:
                        Input = None
                        confidence = None

                if CallerNeeded:
                    if any(Caller.lower() in Input.lower() for Caller in AlphabetV2.Caller): pass
                    else: Input = None

        except sr.WaitTimeoutError as e:
            r = Recognizer()
            continue
        except sr.UnknownValueError as e:
            r = Recognizer()
            continue
        except Exception as e: 
            print(e)
        finally:
            if Input == None:
                if Repeat == -1: pass
                elif Repeat >= 1: Repeated += 1
                continue
            else:
                if content["settings"]["save_all_microphone_data"]:
                    with open(str(path) + "\Assets\Results\microphone-results " + str(datetime.now().strftime('%H-%M-%S')) + ".wav", "wb") as f: 
                        f.write(audio.get_wav_data())
                return Input, confidence