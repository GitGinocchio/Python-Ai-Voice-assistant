from gtts import gTTS
import gtts
import librosa
import soundfile as sf
from time import sleep
import time
import os
import pyaudio
import wave
import threading
#from pynput import keyboard
#----------------------------------------------------------------
from datastructures import path,Djson


#langs = [lang for lang in gtts.lang.tts_langs()]

#p = pyaudio.PyAudio()
#listofdevices = [p.get_device_info_by_index(i) for i in range(p.get_device_count())]
#print(listofdevices[0])
#for i in range(len(listofdevices)):
    #if listofdevices[i]['maxOutputChannels'] > 0:
        #print(listofdevices[i]["index"],listofdevices[i]["name"])
#print(listofdevices)


    
class Speaker:
    def __init__(self,fp : str,device : int | str = None,lang : str ='en', tld : str = 'com',slow : str = "False",rfa  : bool = True): # = content["sys_data"]["output_devices"]["selected"][0]
        self.p = pyaudio.PyAudio()
        self.device = device
        self.fp = fp
        self.lang = lang
        self.tld = tld
        self.slow = slow
        self.lenght = 0.0
        self.start_audio_time = 0.0
        self.actual_audio_time = 0.0
        self.stream = None
        self.rfa = rfa

        if self.device != None:
            if type(self.device) == int:
                self.device = [self.p.get_device_info_by_index(self.device)][0]['index']
            elif type(self.device) == str:
                self.device = [self.p.get_device_info_by_index(self.get_device_index_by_name(self.device))][0]['index']
        else:
            self.device = [self.p.get_default_output_device_info()][0]['index']

    def get_device_index_by_name(self,device_name : str = None):
        """
        """

        content = Djson.content()
        if device_name != None:
            device_index = [index for index,name in content["sys_data"]["output_devices"]["devices"] if name == device_name][0]
        else:
            device_index = content["sys_data"]["output_devices"]["devices"][0]
        return int(device_index)

    def set_device(self, device_index : int = None):
        if device_index is None:
            content = Djson.content()
            if len(content["sys_data"]["output_devices"]["selected"]) == 2:
                self.device = content["sys_data"]["output_devices"]["selected"][0]
            else:
                self.device = content["sys_data"]["output_devices"]["devices"][0]
        else:
            self.device = device_index
        
        self.stream = None

    def set_tld(self, tld : str = "com"):
        tlds = self.get_tlds()
        if tld in tlds:
            self.tld = tld
    
    def set_lang(self, lang : str = "en"):
        langs = self.get_langs()
        if lang in langs:
            self.lang = lang

    def get_langs(self):
        return [str(lang) for lang in gtts.lang.tts_langs()]
    
    def get_tlds(self):
        return [tld.replace('.google.','') for tld in ".google.com .google.ad .google.ae .google.com.af .google.com.ag .google.com.ai .google.al .google.am .google.co.ao .google.com.ar .google.as .google.at .google.com.au .google.az .google.ba .google.com.bd .google.be .google.bf .google.bg .google.com.bh .google.bi .google.bj .google.com.bn .google.com.bo .google.com.br .google.bs .google.bt .google.co.bw .google.by .google.com.bz .google.ca .google.cd .google.cf .google.cg .google.ch .google.ci .google.co.ck .google.cl .google.cm .google.cn .google.com.co .google.co.cr .google.com.cu .google.cv .google.com.cy .google.cz .google.de .google.dj .google.dk .google.dm .google.com.do .google.dz .google.com.ec .google.ee .google.com.eg .google.es .google.com.et .google.fi .google.com.fj .google.fm .google.fr .google.ga .google.ge .google.gg .google.com.gh .google.com.gi .google.gl .google.gm .google.gr .google.com.gt .google.gy .google.com.hk .google.hn .google.hr .google.ht .google.hu .google.co.id .google.ie .google.co.il .google.im .google.co.in .google.iq .google.is .google.it .google.je .google.com.jm .google.jo .google.co.jp .google.co.ke .google.com.kh .google.ki .google.kg .google.co.kr .google.com.kw .google.kz .google.la .google.com.lb .google.li .google.lk .google.co.ls .google.lt .google.lu .google.lv .google.com.ly .google.co.ma .google.md .google.me .google.mg .google.mk .google.ml .google.com.mm .google.mn .google.ms .google.com.mt .google.mu .google.mv .google.mw .google.com.mx .google.com.my .google.co.mz .google.com.na .google.com.ng .google.com.ni .google.ne .google.nl .google.no .google.com.np .google.nr .google.nu .google.co.nz .google.com.om .google.com.pa .google.com.pe .google.com.pg .google.com.ph .google.com.pk .google.pl .google.pn .google.com.pr .google.ps .google.pt .google.com.py .google.com.qa .google.ro .google.ru .google.rw .google.com.sa .google.com.sb .google.sc .google.se .google.com.sg .google.sh .google.si .google.sk .google.com.sl .google.sn .google.so .google.sm .google.sr .google.st .google.com.sv .google.td .google.tg .google.co.th .google.com.tj .google.tl .google.tm .google.tn .google.to .google.com.tr .google.tt .google.com.tw .google.co.tz .google.com.ua .google.co.ug .google.co.uk .google.com.uy .google.co.uz .google.com.vc .google.co.ve .google.vg .google.co.vi .google.com.vn .google.vu .google.ws .google.rs .google.co.za .google.co.zm .google.co.zw .google.cat".split()]

    def __func_for_thread__(self):
        """DON'T CALL THIS FUNCTION, USE 'SAY' OR 'PLAY' INSTEAD"""
        self.stream.start_stream()
        self.start_audio_time = time.time()

        while self.stream.is_active():
            sleep(0.1)

        
        end_audio_time = time.time()
        self.actual_audio_time += round((end_audio_time - self.start_audio_time),3)

        while True:

            if self.rfa:
                if round(self.actual_audio_time,3) >= self.lenght:
                    self.lenght = 0.0
                    self.start_audio_time = 0.0
                    self.actual_audio_time = 0.0
                    self.remove()
                    #print("file played completely")
            break

    def say(self,phrase : str, wait : bool = False, rfa : bool = True):
        """
        
            "phrase" = the phrase that the voice assistant must say

            "wait" = the time to wait for play the file audio (NOTE: the code will wait until file speak is finished)

            "rfa" = if "True" the file audio will be played and removed after it finishes COMPLETELY

        returns:
            
            "lenght (float)" = lenght of the mp3 file
            
            "path (str)" = path of the saved file in string
        """
        self.phrase = phrase
        self.wait = wait

        def callback(in_data, frame_count, time_info, status):
            #print(in_data, frame_count, time_info, status)
            data = self.wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        try:
            tts = gTTS(
                text=self.phrase, 
                lang=self.lang, 
                tld=self.tld, 
                slow=eval(self.slow), 
                lang_check=False
                )
            list = [i for i in tts.stream()]
            with open(self.fp, 'wb') as f: f.write(list[0])
            x,_ = librosa.load(self.fp, sr=16000)
            sf.write(self.fp, x, 16000)
            self.wf = wave.open(self.fp, 'rb')
        except Exception as e:
            print(e)

        try:
            """
            see doc here:

            see is_format_supported()

            https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.is_format_supported
            
            """
            self.stream = self.p.open(
                format=self.p.get_format_from_width(self.wf.getsampwidth(),unsigned=True),
                channels=self.wf.getnchannels(),
                rate=self.wf.getframerate(),
                output=True,
                output_device_index=self.device,
                stream_callback=callback)
        except OSError as e:
            print(e, " | will be used default device")
            self.stream = self.p.open(
                format=self.p.get_format_from_width(self.wf.getsampwidth()),
                channels=self.wf.getnchannels(),
                rate=self.wf.getframerate(),
                output=True,
                output_device_index=[self.p.get_default_output_device_info()][0]['index'],
                stream_callback=callback)
        finally:
            try:
                if wait:
                    self.__func_for_thread__()
                else:
                    threading.Thread(target=self.__func_for_thread__,daemon=True).start()
                # get lenght
                frames = self.wf.getnframes()
                framerate = self.wf.getframerate()
                self.lenght = float(frames) / float(framerate)
            except Exception as e:
                print(e)
            else:
                return ((self.lenght), (self.fp))

    def stop(self, close : bool = False):
        if self.stream != None:
            if self.stream.is_active():
                self.stream.stop_stream()

        if close:
            self.remove()
    
    def play(self):
        if self.stream != None:
            if self.stream.is_stopped():   
                threading.Thread(target=self.__func_for_thread__,daemon=True).start()

    def remove(self):
        if self.stream != None:
            if self.stream.is_active():
                self.stream.stop_stream()
            self.wf.close()
        if os.path.exists(self.fp):
            os.remove(self.fp)

    def terminate(self):
        self.remove()
        self.p.terminate()

#FILE = fr"{str(path)}\%Temp%\response.wav"

#sp = Speaker(fp=FILE,lang='it',device=30,tld='it',rfa=True) # device=30
#lenght,file = sp.say("Ciao questo e' un file audio che ho creato in questo momento...")
#print(lenght)
#sp.set_lang("en")
#sleep(lenght)
#lenght,file = sp.say("Ciao questo e' un file audio che ho creato in questo momento...")
#sp.set_lang("en")
#lenght,file = sp.say("Ciao questo e' un file audio...")
#print(lenght)
#sleep(lenght)



#while True:
    #sleep(0.1)
#lenght,file = sp.say("Come stai?")
#sleep(lenght)