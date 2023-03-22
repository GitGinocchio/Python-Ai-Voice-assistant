from PyQt5.QtCore import QThread, pyqtSignal
#-----------------------------------------------------------------------------
from datastructures import Djson
#-----------------------------------------------------------------------------

class ThreadManager(QThread):
    any_signal = pyqtSignal(str)
    def __init__(self,index , parent,spkrclass=None,lstnrclass=None,question=None,callerneeded=None,repeat=None,message=None):
        super(ThreadManager, self).__init__(parent)
        self.index = index
        #######################
        self.p = parent
        self.spkrclass = spkrclass
        #######################
        self.message = message
        #######################
        self.question = question
        self.callerneeded = callerneeded
        self.repeat = repeat
    
    def run(self):
        #INIT
        if self.index == 0:
            try:
                from init_data import check_input_pyaudio_devices,check_output_pyaudio_devices
                check_input_pyaudio_devices()
                check_output_pyaudio_devices()
                del check_input_pyaudio_devices,check_output_pyaudio_devices


                content = Djson.content()
                input_device_zero = content["sys_data"]["input_devices"]["devices"][0]
                if len(content["sys_data"]["input_devices"]["selected"]) != 2:
                    content["sys_data"]["input_devices"]["selected"].clear()
                    content["sys_data"]["input_devices"]["selected"].extend(input_device_zero)
                else:
                    if content["sys_data"]["input_devices"]["selected"] not in content["sys_data"]["input_devices"]["devices"]: 
                        content["sys_data"]["input_devices"]["selected"].clear()
                        content["sys_data"]["input_devices"]["selected"].extend(input_device_zero)
                

                output_device_zero = content["sys_data"]["output_devices"]["devices"][0]
                if len(content["sys_data"]["output_devices"]["selected"]) != 2:
                    content["sys_data"]["output_devices"]["selected"].clear()
                    content["sys_data"]["output_devices"]["selected"].extend(output_device_zero)
                else:
                    if content["sys_data"]["output_devices"]["selected"] not in content["sys_data"]["output_devices"]["devices"]: 
                        content["sys_data"]["output_devices"]["selected"].clear()
                        content["sys_data"]["output_devices"]["selected"].extend(output_device_zero)
                
                Djson.save_to_file(content)
            except Exception as e:
                print("Error", e)
            finally:
                self.deleteLater()
        #ATTEMPT
        if self.index == 1:
            try:
                from pre_processing_ai import AI_Objectification
                from answering import attempt

                TAG, PROB_HIT, INTENT, PATTERN, DEFAULT_RESPONSE, FAILED_RESPONSES ,ACCEPT_INFO, STEMMEDPHRASE = AI_Objectification(self.message,0.90)
                print(TAG,PROB_HIT)

                istance = attempt(parent=self.parent(),threadmngrclass=self,spkrclass=self.spkrclass,testo=self.message,tag=TAG,pattern=PATTERN,info=ACCEPT_INFO,dfltresponses=DEFAULT_RESPONSE,failed_dfltresponses=FAILED_RESPONSES)
                time_passed, Responses, Caller, Dato = istance.getreponse()
                """
                #print(time_passed, Responses, Caller, Dato)

                #if Caller != None and TAG != 'None':
                    #for Response in Responses: 
                        #self.parent().update_text_browser(Response=Response,Caller=Caller)
                        #if self.SPEAK:
                            #if Response != None:
                                #if content["settings"]["use_gtts_voice_setting"]:
                                    #lenght, _ = self.spkrclass.say(Response)
                                    #sleep(lenght)
                                #else:
                                    #self.spkrclass.say(Response)

                    #if Notifications.RunningTime["Bool"]:
                        #Response = Notifications.RunningTime["Value"]
                        #self.parent().update_text_browser(f"{Response}<br>{str(round(time_passed,3))} seconds","[System]","orange",True)
                #else:
                    #self.parent().update_text_browser(self.message,"You")
                """
            except Exception as e:
                print(str(e))
            finally:
                del AI_Objectification,attempt
                self.any_signal.emit('START LISTEN THREAD')
                self.parent().DisableAll(False)
                self.deleteLater()
        #LISTEN
        if self.index == 2:
            try:
                vocalmessage, confidence = self.lstnrclass.listen(question=self.question,callerneeded=self.callerneeded,repeat=self.repeat)

                self.any_signal.emit(vocalmessage)
                self.parent().DisableAll(False)
            except Exception as e:
                self.parent().DisableAll(False)
                self.any_signal.emit('None')
            finally:
                self.deleteLater()