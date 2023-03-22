from datastructures import Djson, AlphabetV2, path
import speech_recognition as sr
from speech_recognition import Microphone, Recognizer
from time import sleep
from datetime import datetime
import pyaudio

def get_device_index_by_name(device_name : str = None):
    """
    """

    content = Djson.content()
    if device_name != None:
        device_index = [index for index,name in content["sys_data"]["input_devices"]["devices"] if name == device_name][0]
    else:
        device_index = content["sys_data"]["input_devices"]["devices"][0]
    return int(device_index)

class listener:
    def __init__(self,spkrclass : classmethod,*, device : str | int = None, sample_rate : int = 44100, chunk_size : int = 1024):
        self.p = pyaudio.PyAudio()
        self.spkrclass = spkrclass
        self.r = Recognizer()
        self.device = device
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size

        if self.device != None:
            if type(self.device) == int:
                info = self.p.get_device_info_by_index(self.device)
            elif type(self.device) == str:
                info = self.p.get_device_info_by_index(self.get_device_index_by_name(self.device))
            self.sample_rate = info['defaultSampleRate']
            self.device = info['index']
        else:
            info = self.p.get_default_input_device_info()
            self.sample_rate = info['defaultSampleRate']
            self.device = info['index']

    def set_device(self,device_index : int = None):
        if device_index is None:
            content = Djson.content()
            if len(content["sys_data"]["input_devices"]["selected"]) == 2:
                self.device = content["sys_data"]["input_devices"]["selected"][0]
            else:
                self.device = content["sys_data"]["input_devices"]["devices"][0]
        else:
            self.device = device_index
        info = self.p.get_device_info_by_index(self.device)
        self.sample_rate = info['defaultSampleRate']
        self.device = info['index']
        
    def get_device_index_by_name(self,device_name : str = None):
        """
        """

        content = Djson.content()
        if device_name != None:
            device_index = [index for index,name in content["sys_data"]["input_devices"]["devices"] if name == device_name][0]
        else:
            device_index = content["sys_data"]["input_devices"]["devices"][0]
        return int(device_index)

    def listen(self,*, question : str = None, callerneeded : bool = True, repeat : int = -1):
        assert isinstance(self.device,(int,str))
        content = Djson.content()
        
        input = None
        confidence = None

        if repeat != -1: repeated = 0
        else: repeated = -2

        while input == None and repeated < repeat:
            try:
                with Microphone(self.device,int(self.sample_rate),int(self.chunk_size)) as source:
                    self.r.adjust_for_ambient_noise(source, duration=0.7)
                    self.r.pause_threshold = 0.5
                    self.r.dynamic_energy_threshold = True
                    
                    try:
                        if question != None and content["settings"]["use_gtts_voice_setting"]:
                            lenght, _ = self.spkrclass.say(question)
                            sleep(lenght)

                        audio = self.r.listen(source,timeout=None,phrase_time_limit=5)
                        data = self.r.recognize_google(audio,language="it-IT",pfilter=0,show_all=True,with_confidence=True)

                    except Exception as e:
                        print(e)
                        input = None
                        confidence = None
                    else:
                        if len(data) != 0:
                            input = (data['alternative'][0]['transcript']).lower()
                            confidence = (data['alternative'][0]['confidence'])
                            
                            if callerneeded:
                                if any(Caller.lower() in input.lower() for Caller in AlphabetV2.Caller): pass
                                else: input = None
                        else:
                            input = None
                            confidence = None
            except sr.WaitTimeoutError as e:
                continue
            except sr.UnknownValueError as e:
                continue
            except Exception as e: 
                print("Error",e)
            finally:
                if input == None:
                    if repeat == -1: pass
                    elif repeat >= 1: repeated += 1
                    continue
                else:
                    if content["settings"]["save_all_microphone_data"]:
                        with open(str(path) + "\Assets\Results\microphone-results " + str(datetime.now().strftime('%H-%M-%S')) + ".wav", "wb") as f: 
                            f.write(audio.get_wav_data())
                    return input, confidence








#FILE = fr"{str(path)}\%Temp%\response.wav"
#sp = Speaker(fp=FILE,lang='en',device=None,tld='com',rfa=True)


#index = get_device_index_by_name("YOUR MICROPHONE")
#l = listener(spkrclass=sp)

#output, precision = l.listen(question="YOUR TEXT HERE")
#print(output, precision)
