from datastructures import AlphabetV2,Notifications,path,config,Djson
from parser_utils import Parser_

#IMPORTS
from time import sleep
import random,requests,time,os,googlesearch,webbrowser
from datetime import datetime
import pyautogui as p
import subprocess
import wikipedia
import bs4
#------------------------------


class attempt:
    def __init__(self,parent,threadmngrclass,spkrclass,testo : str, tag: str, pattern: list, info: bool, dfltresponses : list, failed_dfltresponses : list):
        self.parent = parent
        self.spkrclass = spkrclass
        self.threadmngrclass = threadmngrclass
        self.testo = testo
        self.tag = tag
        self.pattern = pattern
        self.info = info
        self.dfltresponses = dfltresponses
        self.failed_dfltresponses = failed_dfltresponses
        #---------------------------------------------------------------------
        self.Caller = None
        self.Dato = None
        self.Responses = []
        self.strtTimer = 0

        if any(Caller.lower() in self.testo.lower() for Caller in AlphabetV2.AllCallers):
            for Caller in AlphabetV2.AllCallers:
                if Caller.lower() in self.testo.lower():
                    if self.tag != 'None':
                        #add on ui_main_window this:
                        """
                        istance = attempt('parent',"Google che ore sono","hours",list,True,list,list)

                        if istance != 'None':
                            #self.update_text_browser(self.testo,"You")
                        ecc...
                        
                        """
                    self.Caller = Caller.lower().capitalize()
                    break
    
    def getreponse(self):
        """

        """
        self.strtTimer = time.time()
        #speakclass = Speaker(fr"{str(path)}\%Temp%\response.wav",'it','it')
        speakclass = self.spkrclass
        parserclass = Parser_('<','>','_')

        try:
            self.parent.update_text_browser(self.testo,"You")
            assert self.Caller != None
            

            if self.tag == 'hours':
                try:
                    Random_Response = random.choice(self.dfltresponses).replace('a\'','à').replace('e\'','è')
                    Response = Random_Response.format(datetime.now().strftime('%H e %M'))

                    self.parent.update_text_browser(Response,self.Caller)
                    lenght, _ = speakclass.say(Response)
                    sleep(lenght)


                except Exception as e:
                    print(str(e))
                    Random_Failed_Response = random.choice(self.failed_dfltresponses)
                    self.parent.update_text_browser(Random_Failed_Response,self.Caller)
                    lenght, _ = speakclass.say(Random_Failed_Response)
                    sleep(lenght)
            
            elif self.tag =='greetings':
                try:
                    current_hour = int(datetime.now().strftime('%H'))
                    Responses = self.dfltresponses[0]
                    content = Djson.content()

                    if len(content["settings"]["User"]["nicknames"]) != 0:
                        User = random.choice(content["settings"]["User"]["nicknames"])
                    elif len(content["settings"]["User"]["name"]) != 0:
                        User = content["settings"]["User"]["name"]
                        if len(content["settings"]["User"]["lastname"]) != 0:
                            User = User + " " + content["settings"]["User"]["lastname"]
                    else:
                        User = os.getlogin()


                    num = random.randint(0,1)

                    if num == 0:
                        RandomResponse = (random.choice(Responses["simple answers"])).format(User)
                    elif num == 1:
                        #morning
                        if current_hour >= 5 and current_hour <= 12:
                            RandomResponse = (random.choice(Responses["morning"])).format(User)
                        #afternoon
                        if current_hour > 12 and current_hour < 18:
                            RandomResponse = (random.choice(Responses["afternoon"])).format(User)
                        #evening
                        if current_hour >= 18:
                            RandomResponse = (random.choice(Responses["evening"])).format(User)
                        #night                    
                        if current_hour >= 0 and current_hour < 5:
                            RandomResponse = (random.choice(Responses["night"])).format(User)

                    #-------------------------------------------------------------------
                    self.parent.update_text_browser(RandomResponse,self.Caller)
                    lenght, _ = speakclass.say(RandomResponse)
                    sleep(lenght)

                except Exception as e:
                    print(str(e)) 

            elif self.tag == 'weather':

                Format = "C"
                try:
                    try:
                        ParsedText = parserclass.Parsing(self.testo)
                        _, _, self.Dato = parserclass.Finder(Phrase=ParsedText ,ToPass= -1 ,Block_to_Function=True ,Tracked_TAG=self.tag)
                        chars = ['?','!',';','.',',',]
                        Location = [self.Dato.replace(char,'') for char in chars][0].strip().lower().capitalize()
                        Location = Location.replace(' ','+')
                    except IndexError:
                        import geocoder
                        g = geocoder.ip('me')
                        Location = g.city.replace(' ','+')
                        latlng = g.latlng

                        Response = f"Non hai precisato una 'Location', verra' utilizzata la posizione attuale ({latlng}), potrebbe essere poco precisa."
                        self.parent.update_text_browser(Response, self.Caller,Space=True) #lenght,_ = Speaker.Say(Response) #sleep(lenght)
                        del geocoder
                    finally:
                        data = requests.get(url=f'https://wttr.in/{Location}?format=j2',params="lang=it",timeout=10)
                        data.raise_for_status()
                        data = data.json()

                        data_with_hourly = requests.get(url=f'https://wttr.in/{Location}?format=j1',params="lang=it",timeout=10)
                        data_with_hourly.raise_for_status()
                        data_with_hourly = data_with_hourly.json()

                        region = data["nearest_area"][0]["region"][0]["value"]
                        country = data["nearest_area"][0]["country"][0]["value"]
                        area_name = data["nearest_area"][0]["areaName"][0]["value"]

                        if self.Dato != None and Location.lower() == region.lower():
                            Response = f"In {region}, {country}."
                        elif self.Dato != None and Location.lower() == country.lower():
                            Response = f"In {country}."
                        elif self.Dato != None and Location.lower() == area_name.lower():
                            Response = f"A {area_name}, {region}, {country}."
                        else:
                            Response = f"A {area_name}, {region}, {country}."

                        self.parent.update_text_browser(Response, self.Caller) 
                        lenght,_ = speakclass.say(Response) 
                        sleep(lenght)
                        #----------------------------------------------------------------------------------------
                        description = (data['current_condition'][0]['lang_it'][0]['value'])


                        if Format == 'C':
                            min_temp_C = (data['weather'][0]['mintempC'])
                            Response = f"Prevedo {description}, la temperatura minima è {min_temp_C}°C"
                        elif Format == 'F':
                            min_temp_F = (data['weather'][0]['mintempF'])
                            Response = f"Prevedo {description}, la temperatura minima è {min_temp_F}°F"

                        self.parent.update_text_browser(Response, self.Caller) 
                        lenght,_ = speakclass.say(Response) 
                        sleep(lenght)
                        #----------------------------------------------------------------------------------------

                        if Format == 'C':
                            #temp_C_feels_like = data["current_condition"][0]["FeelsLikeC"]
                            temp_C = data["current_condition"][0]["temp_C"]
                            Response = f"La temperatura attuale è di: {temp_C}°C."
                        elif Format == 'F':
                            temp_F = data["current_condition"][0]["temp_F"]
                            Response = f"La temperatura attuale è di: {temp_F}°F."
                        
                        self.parent.update_text_browser(Response, self.Caller) 
                        lenght,_ = speakclass.say(Response) 
                        sleep(lenght)
                        #----------------------------------------------------------------------------------------
                        percentages_of_rain = [int(i["chanceofrain"]) for i in data_with_hourly["weather"][0]["hourly"]]
                        #print(percentages_of_rain)

                        if max(percentages_of_rain) >= 5.0:
                            Response = f"La probabilità di pioggia più alta rilevata durante la giornata è del {max(percentages_of_rain)}%"
                            self.parent.update_text_browser(Response, self.Caller)
                            lenght,_ = speakclass.say(Response)
                            sleep(lenght)
                        #----------------------------------------------------------------------------------------   
                        percentages_of_snow = [int(i["chanceofsnow"]) for i in data_with_hourly["weather"][0]["hourly"]]
                        #print(percentages_of_snow)

                        if max(percentages_of_snow) >= 5.0:
                            Response = f"La probabilità più alta di una nevicata rilevata durante la giornata è del {max(percentages_of_snow)}%"
                            self.parent.update_text_browser(Response, self.Caller)
                            lenght,_ = speakclass.say(Response)
                            sleep(lenght) 
                        #----------------------------------------------------------------------------------------


                        #----------------------------------------------------------------------------------------
                        Response = f"Maggiori informazioni sul meteo utilizzato a <a href=https://wttr.in/{Location}?format> https://wttr.in/{Location}?format </a>"
                        self.parent.update_text_browser(Response, self.Caller,Space=True) 
                except Exception as e:
                    RandomResponse = random.choice(self.failed_dfltresponses)
                    Response = RandomResponse.format([e])
                    self.parent.update_text_browser(Response, self.Caller,Space=True,Color="Red") 

            elif self.tag == 'Play and Pause':
                try:
                    p.hotkey('playpause')
                except Exception as e:
                    print(str(e))
            
            elif self.tag == 'Skip':
                try:
                    p.hotkey('nexttrack')
                except Exception as e:
                    print(str(e)) 

            elif self.tag == 'Back Skip':
                try:
                    p.press('prevtrack',2)
                except Exception as e:
                    print(str(e)) 

            elif self.tag == 'Play a Song':
                try:
                    ParsedText = parserclass.Parsing(self.testo)
                    _, _, self.Dato = parserclass.Finder(Phrase=ParsedText, ToPass= -1, Block_to_Function=True,Tracked_TAG=self.tag)
                    Response = f"Riproduco {self.Dato}"
                    self.parent.update_text_browser(Response,self.Caller)
                    lenght, _ = speakclass.say(Response)
                    sleep(lenght)


                    link = googlesearch.lucky(self.Dato)
                    link = googlesearch.filter_result(link=link)
                    webbrowser.open_new_tab(link)
                except Exception as e:
                    print(str(e))

            elif self.tag == 'ScreenShot':
                try:
                    DatetimeNow = str(datetime.now().strftime('%H.%M.%S'))
                    ScreenShot_Path = f"{path}\Assets\ScreenShots"
                    ScreenShot_Name = f'ScreenShot {DatetimeNow}.png'
                    ScreenShot_File = f"{ScreenShot_Path}\{ScreenShot_Name}"

                    p.screenshot(f"{ScreenShot_File}")

                    Response_1 = f"Ho fatto uno ScreenShot"
                    Response_2 = f"Nome del file: {ScreenShot_Name}"

                    self.parent.update_text_browser(Response_1,self.Caller)
                    lenght, _ = speakclass.say(Response_1)
                    sleep(lenght)
                    self.parent.update_text_browser(Response_2,self.Caller)
                    lenght, _ = speakclass.say(Response_2)
                    sleep(lenght)

                
                except Exception as e:
                    print(str(e))

            elif self.tag == 'Google Search and Wikipedia':
                
                def Wikipedia(Lang: "str",Phrase: "str",Sentences: "float",Parsing: "bool"):
                    wikipedia.set_lang(Lang)
                    Response = wikipedia.summary(Phrase,sentences=Sentences)
                    #sentences=5
                    #'it'
                    #Cached.dato

                    if Parsing == True:
                        for parola in [',','.',';',':','(',')']:
                            Response = str.strip(Response.replace(parola,parola +'\n'))
                    for parola in ['==','=']:
                        Response = str.strip(Response.replace(parola, '||'))        

                    return Response
                
                def GoogleSearch(Phrase: 'any'):
                    link = googlesearch.lucky(Phrase)
                    link = googlesearch.filter_result(link=link)
                    webbrowser.open_new_tab(link)
                    #webbrowser.open_new_tab(f'https://google.com/search?q={Phrase}')

                    def SearchForUndefinedResult(link):
                        Unilink = requests.get(link)
                        Unilink.raise_for_status()

                        tags = ['h1','p',]
                        Carachters = ['\n','\ns']
                        Texts = []
                        soup = bs4.BeautifulSoup(Unilink.content,'html.parser')

                        for tag in tags:
                            elements = soup.find_all(tag,limit=1)
                            for element in elements:
                                text = element.text
                                for C in Carachters:
                                    text = text.replace(C,'')
                                Texts.append(text.strip())

                        return Texts
                    Responses = SearchForUndefinedResult(link=link)
                    for Response in Responses:
                        self.update_text_browser(Response,self.Caller)
                        lenght, _ = speakclass.say(Response)
                        sleep(lenght)

                def FailedSearchClutch():
                    try:
                        Response = f"ho trovato questo risultato"
                        self.parent.update_text_browser(Response,self.Caller)
                        lenght, _ = speakclass.say(Response)
                        sleep(lenght)
                        GoogleSearch(self.Dato)

                    except Exception as e:
                        print(str(e))
                #search(query=link,tld=domain[1],lang='it',tbs=3,safe='on')

                try:
                    ParsedText = parserclass.Parsing(self.testo)
                    if '_e\'_' in ParsedText:
                        ParsedText = ParsedText.replace('_e\'_','_è_')

                    _, _, self.Dato = parserclass.Finder(Phrase=ParsedText, ToPass= -1, Block_to_Function=True,Tracked_TAG=self.tag)

                    print(self.Dato)

                    n = 0
                    for parola in ["cos'è","chi è ","cerca il significato di "]:
                        if parola in self.testo:
                            n = n + 1
                        else:
                            pass
                    if n > 1:
                        raise "REQUEST ERROR: expected one request, but three were given: ( significato di , chi è , cos'è ))"


                    Response = f"Cerco {self.Dato}, potrebbe volerci un po' di tempo, in base a quanto è lunga la definizione"
                    self.parent.update_text_browser(str(Response),self.Caller)
                    lenght, _ = speakclass.say(Response)
                    sleep(lenght)

                    try:
                        Wikipedia_Response = Wikipedia('it',self.Dato,Sentences=3,Parsing=False)
                        Response = f"Secondo Wikipedia: {Wikipedia_Response}"
                        self.parent.update_text_browser(f"<br>Secondo Wikipedia:<br><br>{Wikipedia_Response}<br><br>",self.Caller)
                        lenght, _ = speakclass.say(Response)
                        sleep(lenght)

                    except Exception as e:
                        print(f"{str(e)}")
                        FailedSearchClutch()
                except Exception as e:
                    print(f"{str(e)}")

            elif self.tag == 'Google Search results':
                try:
                    ParsedText = parserclass.Parsing(self.testo)
                    _, _, self.Dato = parserclass.Finder(Phrase=ParsedText, ToPass= -1, Block_to_Function=True,Tracked_TAG=self.tag)

                    Response = f"Ho trovato questo risultato"
                    self.parent.update_text_browser(Response,self.Caller)
                    lenght, _ = speakclass.say(Response)
                    sleep(lenght)

                    webbrowser.get().open(f'https://google.com/search?q={self.Dato}')
                except Exception as e:
                    print(str(e))

            elif self.tag == 'Open':
                try:
                    flags = 0x00000010
                    ParsedText = parserclass.Parsing(self.testo)
                    _, _, self.Dato = parserclass.Finder(Phrase=ParsedText, ToPass= -1, Block_to_Function=True,Tracked_TAG=self.tag)


                    def FindCombinations(Dato: str):
                        for word in [' e ',' , ',', ']:
                            Dato = Dato.replace(word,' ')

                        words = Dato.strip().split(sep=' ')

                        combinations = []

                        import itertools
                        for length in range(1, len(words) + 1):
                            for subset in itertools.product(words, repeat=length):
                                combinations.append(" ".join(subset))
                        #print(combinations)
                        del itertools

                        apps = []
                        apps_not_found = []

                        for combination in combinations:
                            try:
                                app = config['APPS'][combination]
                            except KeyError:
                                pass
                            else:
                                app = (combination,config['APPS'][combination])
                                apps.append(app)

                        #print([app[0] for app in apps])

                        for word in words:
                            if any(i.find(word) != -1 for i in [app[0] for app in apps]):
                                pass
                            else:
                                apps_not_found.append(word)

                        return apps, apps_not_found, words
                    apps,apps_not_found, words = FindCombinations(self.Dato)

                    #----------------------------------------------------------------

                    if len(apps) != 0:
                        for app in apps:

                            try:
                                if app[1] == '':
                                    Response = f"Non e presente nessuna path per {app[0]}, controlla di aver salvato correttamente l'applicazione"
                                    self.parent.update_text_browser(Response,self.Caller)
                                    lenght, _ = speakclass.say(Response)
                                    sleep(lenght)
                                
                                elif any(word in app[1] for word in ['http://','http:\\','https://','https:\\']):
                                    Response = f"Sto aprendo {app[0]}"
                                    self.parent.update_text_browser(Response,self.Caller)
                                    lenght, _ = speakclass.say(Response)
                                    sleep(lenght)


                                    link = str.strip(app[1].replace(' ',''))
                                    webbrowser.open(link,autoraise=True)

                                elif "exe" in app[1]:
                                    Response = f"Sto aprendo {app[0]}"
                                    self.parent.update_text_browser(Response,self.Caller)
                                    lenght, _ = speakclass.say(Response)
                                    sleep(lenght)

                                    subprocess.Popen([app[1]],restore_signals=True,creationflags=flags,start_new_session=True,shell=True)
                                    #subprocess.run([app],restore_signals=True,start_new_session=True,shell=True,)
                                else:
                                    Response = f"Sto aprendo {app[0]} in modalità compatibilità"
                                    self.parent.update_text_browser(Response,self.Caller)
                                    lenght, _ = speakclass.say(Response)
                                    sleep(lenght)

                                    subprocess.Popen([app[1]],restore_signals=True,start_new_session=True,creationflags=flags,shell=True)       
                            
                            except Exception as e:
                                print(str(e))

                        if len(apps_not_found) != 0:
                            for app in apps_not_found:
                                Response = f"Non ho trovato nessuna applicazione chiamata {app}, la cercherò per te sul tuo browser"
                                self.parent.update_text_browser(Response,self.Caller)
                                lenght, _ = speakclass.say(Response)
                                sleep(lenght)

                                link = googlesearch.lucky(app)
                                webbrowser.open_new_tab(link)

                    elif len(apps_not_found) != 0:
                        for app in apps_not_found:
                            Response = f"Non ho trovato nessuna applicazione chiamata {app}, la cercherò per te sul tuo browser"
                            self.parent.update_text_browser(Response,self.Caller)
                            lenght, _ = speakclass.say(Response)
                            sleep(lenght)

                            link = googlesearch.lucky(app)
                            webbrowser.open_new_tab(link)

                except Exception as e:
                    print(e)

            elif self.tag == 'Close':
                try:
                    ParsedText = parserclass.Parsing(self.testo)

                    _, _, self.Dato = Parser_('<','>','_').Finder(Phrase=ParsedText, ToPass= -1, Block_to_Function=True,Tracked_TAG=self.tag)

                    Responses = self.dfltresponses[0]

                    def Find_Exe(Path: any):
                        i = 0

                        while True:
                            Path[i::]
                            if not "\\" in Path[i::]:
                                return Path[i::]
                            else:
                                i = i + 1
                    
                    def FindCombinations(Dato: str):
                        for word in [' e ',' , ',', ']:
                            Dato = Dato.replace(word,' ')

                        words = Dato.strip().split(sep=' ')

                        combinations = []

                        import itertools
                        for length in range(1, len(words) + 1):
                            for subset in itertools.product(words, repeat=length):
                                combinations.append(" ".join(subset))
                        #print(combinations)
                        del itertools

                        apps = []
                        apps_not_found = []

                        for combination in combinations:
                            try:
                                app = config['APPS'][combination]
                            except KeyError:
                                pass
                            else:
                                app = (combination,config['APPS'][combination])
                                apps.append(app)

                        #print([app[0] for app in apps])

                        for word in words:
                            if any(i.find(word) != -1 for i in [app[0] for app in apps]):
                                pass
                            else:
                                apps_not_found.append(word)

                        return apps, apps_not_found, words
                    apps,apps_not_found,_ = FindCombinations(self.Dato)
                    #print(apps,apps_not_found)


                    if len(apps) != 0:
                        for app in apps:
                            try:
                                exe = Find_Exe(app[1])
            
                                Random_Response = random.choice(Responses["process found"]).replace('a\'','à').replace('e\'','è')
                                Response = Random_Response.format(app[0],exe)
                                self.parent.update_text_browser(Response,self.Caller)
                                lenght, _ = speakclass.say(Response)
                                sleep(lenght)
                                returncode = os.system("TASKKILL /F /IM " + exe)
                                self.parent.update_text_browser(Response="Command executed with return code {}".format(returncode),Caller=self.Caller,Space=True)
                            
                            except Exception as e:
                                print(e)
                        
                        if len(apps_not_found) != 0:
                            for app in apps_not_found:
                                Response = f"Non ho trovato nessuna applicazione chiamata {app}."
                                self.parent.update_text_browser(Response,self.Caller)
                                lenght, _ = speakclass.say(Response)
                                sleep(lenght)
                    
                    elif len(apps_not_found) != 0:
                        for app in apps_not_found:
                            Response = f"Non ho trovato nessuna applicazione chiamata {app}."
                            self.update_text_browser(Response,self.Caller)
                            lenght, _ = speakclass.say(Response)
                            sleep(lenght)
                except Exception as e:
                    print(str(e)) 

            elif self.tag == 'STOP':
                speakclass.stop(False)

                # find the exact thread and stop it here

                #try:
                    #endTimer = time.time()
                    #time_passed = (endTimer - self.strtTimer)

                    #if Notifications.RunningTime["Bool"]:
                        #Response = Notifications.RunningTime["Value"]
                        #self.parent.update_text_browser(f"{Response}<br>{str(round(time_passed,3))} seconds","[System]","orange",True)
                    #return time_passed,self.Responses, self.Caller, self.Dato
                #except Exception as e:
                    #print(e)
                #finally:
                    #self.threadmngrclass.any_signal.emit('START LISTEN THREAD')
                    #self.threadmngrclass.deleteLater()
                    #self.spkrclass.stop(False)

            else:
                if Notifications.NotUnderstand["Bool"]:
                    Response = Notifications.NotUnderstand["Value"]
                    self.parent.update_text_browser(Response,self.Caller)
                    lenght, _ = speakclass.say(Response)
                    sleep(lenght)

        except AssertionError:
            pass
        except Exception as e:
            print(e)
        finally:
            endTimer = time.time()
            time_passed = (endTimer - self.strtTimer)
            
            if self.tag != 'STOP':

                if Notifications.RunningTime["Bool"]:
                    Response = Notifications.RunningTime["Value"]
                    self.parent.update_text_browser(f"{Response}<br>{str(round(time_passed,3))} seconds","[System]","orange",True)
            return time_passed,self.Responses, self.Caller, self.Dato
