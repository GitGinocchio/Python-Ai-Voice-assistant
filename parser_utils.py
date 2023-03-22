from datastructures import AlphabetV2

class Parser_:
    def __init__(self,srt_markup : str, end_markup : str, sep_markup : str):
        assert isinstance(srt_markup, str), "Invalid start markup"
        assert isinstance(end_markup, str), "Invalid end markup"
        assert isinstance(sep_markup, str), "Invalid separator markup"

        self.srt_markup = srt_markup
        self.end_markup = end_markup
        self.sep_markup = sep_markup
        #----------------------------------------------------------------


    def Parsing(self, Phrase : str = ...):
        assert isinstance(Phrase, str), "Invalid Phrase type"
        if not Phrase.islower(): Phrase.lower()
        Phrase = f"{self.srt_markup}{Phrase.replace(' ',self.sep_markup).replace('è','Ã¨')}{self.end_markup}"
        return Phrase
    
    def Unparsing(self, Phrase : str = ...):
        assert isinstance(Phrase, str), "Invalid Phrase type"
        if not Phrase.islower(): Phrase.lower()
        for i in [self.srt_markup, self.end_markup]: Phrase = Phrase.replace(i, '')
        for i in [self.sep_markup]: Phrase = Phrase.replace(i, ' ')
        for i in ['ã¨','Ã¨']: Phrase = Phrase.replace(i,'è')
        Phrase = Phrase.strip()
        return Phrase

    def Finder(self, Phrase : str = ..., ToPass: int = -1, UnParsing: bool = True, Block_to_Function: bool = True, Tracked_TAG: str = None):
        assert isinstance(Phrase, str), "Invalid Phrase type"
        assert isinstance(ToPass, int), "Invalid ToPass type"
        assert isinstance(UnParsing, bool), "Invalid Unparsing type"
        assert isinstance(Block_to_Function, bool), "Invalid Block to function type"
        #assert isinstance(Tracked_TAG, str), "Invalid Tracked_TAG type"
        #----------------------------------------------------------------------------
        self.Phrase = Phrase
        self.Tracked_TAG = Tracked_TAG


        def Main(Phrase: str = self.Phrase,TAG: str = self.Tracked_TAG):
            if TAG != None:
                try:
                    Tag_pos = ([i for i in range(0,AlphabetV2.Lenpatterns) if AlphabetV2.Allintents[i]['tag'] == TAG][0])
                except IndexError:
                    raise IndexError(f"No matching found with {TAG} and json file")
                else:
                    if AlphabetV2.Allintents[Tag_pos]["accept info"] == "True":
                        Accept_info = True
                        Function = [Parser_('_','_','_').Parsing(Function) for Function in AlphabetV2.Allpatterns[Tag_pos] if Phrase.find(Parser_('_','_','_').Parsing(Function)) != -1][0]
                    else:
                        Accept_info = False
                        Function = [Parser_('','','_').Parsing(Function) for Function in AlphabetV2.Allpatterns[Tag_pos] if Phrase.find(Parser_('','','_').Parsing(Function)) != -1][0]
                    try:
                        Start_Function = Phrase.find(Function)
                        End_Function = len(Function) + int(Start_Function)
                    except IndexError:
                        raise IndexError(f"No Function Found, no information available for {TAG}")
                    else:
                        return Function, Start_Function, End_Function, Accept_info 

            else:
                for Tag_pos in range(0,AlphabetV2.Lenpatterns):
                    for Function in AlphabetV2.Allpatterns[Tag_pos]:
                        if AlphabetV2.Allintents[Tag_pos]["accept info"] == "True":
                            try:
                                Function = [Parser_('_','_','_').Parsing(Function) for Function in AlphabetV2.Allpatterns[Tag_pos] if Phrase.find(Parser_('_','_','_').Parsing(Function)) != -1][0]
                            except IndexError:
                                Function = None
                                continue
                            else:
                                if AlphabetV2.Allintents[Tag_pos]["accept info"] == "True":
                                    Accept_info = True
                                else:
                                    Accept_info = False

                                if Phrase.find(Function) != -1:
                                    try:
                                        Start_Function = Phrase.find(Function)
                                        End_Function = len(Function) + int(Start_Function)
                                    except IndexError:
                                        raise IndexError(f"No Function Found, no information available for {TAG}")
                                    else:
                                        return Function, Start_Function, End_Function, Accept_info 
                        
                        else:
                            try:
                                Function = [Parser_('_','_','_').Parsing(Function) for Function in AlphabetV2.Allpatterns[Tag_pos] if Phrase.find(Parser_('_','_','_').Parsing(Function)) != -1][0]
                            except IndexError:
                                Function = None
                                continue
                            else:
                                if AlphabetV2.Allintents[Tag_pos]["accept info"] == "True":
                                    Accept_info = True
                                else:
                                    Accept_info = False

                                if Phrase.find(Function) != -1:
                                    try:
                                        Start_Function = Phrase.find(Function)
                                        End_Function = len(Function) + int(Start_Function)
                                    except IndexError:
                                        raise IndexError(f"No Function Found, no information available for {TAG}")
                                    else:
                                        return Function, Start_Function, End_Function, Accept_info
                                    
        try:
            Func, start, finish, accept_info = Main()

            if accept_info:
                if ToPass != -1:
                    Passed = 0
                    i = finish + 1


                    while Passed < ToPass:
                        Dato = self.Phrase[finish:i]
                        
                        if self.end_markup in self.Phrase[finish:i]:
                            Dato = self.Phrase[finish:i]
                            break

                        if self.sep_markup in self.Phrase[finish:i]:
                            self.Phrase[finish:i]
                            finish = i
                            i = i + 1
                            Passed = Passed + 1
                        i = i + 1
                    Dato = self.Unparsing(Dato)
                elif ToPass == -1:
                    Dato = self.Phrase[finish::]

                    if Block_to_Function:
                        try:
                            _, startfn, _, _ = Main(Dato,TAG=None)
                        except TypeError:
                            startfn = None

                        if startfn != None:
                            Dato = self.Phrase[finish:finish+startfn]
                            Dato = self.Unparsing(Dato)
            else:
                Dato = None
            
            if UnParsing:
                if type(Dato) == type(''):
                    Dato = self.Unparsing(Dato)
                Func = self.Unparsing(Func)
                self.Phrase = self.Unparsing(self.Phrase)
            else:
                Dato = self.Parsing(Dato)
        except TypeError:
            Func = None
            start = None
            finish = None 
            accept_info = None
        
        return self.Phrase, Func, Dato