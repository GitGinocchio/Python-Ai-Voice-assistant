from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtGui import QIcon,QFont
from PyQt5 import QtCore
#-----------------------------------------------------------------------------
from datastructures import config,path,Djson
#-----------------------------------------------------------------------------
from speaker_utils_with_stop_func import Speaker
from listener_with_pyaudio_istance import listener

class Ui_MainWindow(QMainWindow):
    def __init__(self,threadmngr,childsettings,childsystray):
        super().__init__()
        content = Djson.content()
        self.threadmngr = threadmngr
        self.childsettings = childsettings
        self.childsystray = childsystray
        self.spkrclass = Speaker(
                fp=fr"{str(path)}\%Temp%\response.wav",
                lang=content["voice_properties"]["GTTS_settings"]["lang"],
                tld=content["voice_properties"]["GTTS_settings"]["tld"],
                slow=content["voice_properties"]["GTTS_settings"]["slow"])
        self.lstnrclass = listener(self.spkrclass)
        init_Thread = self.threadmngr(0,self)
        init_Thread.start(0)
        self.spkrclass.set_device(content["sys_data"]["output_devices"]["selected"][0])
        self.lstnrclass.set_device(content["sys_data"]["input_devices"]["selected"][0])
        #----------------------------------------------------------------
        #systray
        self.StartTimer = 0
        self.systrayactive = False
        self.icon = None
        #----------------------------------------------------------------
        uic.loadUi(fr'{path}\Assets\Ui\QMainwindow.ui',self)
        #uic.loadUi(fr'{path}\Assets\Ui\QMainwindow without top bar.ui',self)
        self.setWindowIcon(QIcon(fr'{path}\Assets\icons\mic.ico'))
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        #self.showMaximized()
        #self.showFullScreen()
        QFontStyle = QFont(
            content["settings"]["style"]["font"],
            content["settings"]["style"]["point size"]
            )
        self.lineEdit.setFont(QFontStyle)
        self.SendButton.setFont(QFontStyle)
        self.textBrowser.setFont(QFontStyle)
        self.menubar.setFont(QFontStyle)
        self.show()
        #---------------------------------------------------------------
        #Menu Buttons
        #self.exit.clicked.connect(self.Exit)
        #self.maximize.clicked.connect(self.Maximize)
        #self.minimize.clicked.connect(self.Minimize)
        self.actionExit.triggered.connect(self.Exit)
        self.actionTray.triggered.connect(self.SystemTray)
        self.actionClear_Chat.triggered.connect(self.ClearChat)
        self.actionSettings.triggered.connect(self.OpenSettingsTab)

        #UI Buttons
        self.SendButton.clicked.connect(self.SendMessage)
        self.ListenButton.clicked.connect(self.Start_Listener_Thread)
    
    #---------------------------------------------------------------
    """
    'button clicked'
    ...
    self.spkrclass.stop(False)
    ...
    stop audio player
    ...
    (maybe same thing with thread manager)
    """


    def DisableAll(self, param : bool):
        self.SendButton.setDisabled(param)
        self.ListenButton.setDisabled(param)
        self.menuMenu.setDisabled(param)
    #---------------------------------------------------------------

    #@pyqtSlot(str)
    def Start_Listener_Thread(self):
        try:
            self.ListenButton.setIcon(QIcon(fr'{path}\Assets\icons\mic_green.png'))
            self.Listener_Thread = self.threadmngr(index=2,parent=self,spkrclass=self.spkrclass,lstnrclass=self.lstnrclass,question="Cosa posso fare per te?",callerneeded=True,repeat=1)
            self.Listener_Thread.start(0)
            self.Listener_Thread.any_signal.connect(self.Start_Processing_Thread)
        except Exception as e:
            print(e)

    def Start_Processing_Thread(self,message: str):
        self.ListenButton.setIcon(QIcon(fr'{path}\Assets\icons\mic.png'))
        if message != 'None':
            #self.DisableAll(True)
            self.message = message
            self.Processing_data_Thread = self.threadmngr(index=1,parent=self,spkrclass=self.spkrclass,message=self.message)
            self.Processing_data_Thread.start(0)

    def SendMessage(self):
        #self.DisableAll(True)
        Message = self.lineEdit.text()
        self
        if Message.strip() != '':
            self.Start_Processing_Thread(Message)
            self.lineEdit.clear()
        else:
            self.DisableAll(False)

    def OpenSettingsTab(self):
        ui = self.childsettings(parent=self)
        content = Djson.content()
        ui.setFont(QFont(content["settings"]["style"]["font"],int(content["settings"]["style"]["point size"])))
        ui.exec_()

    def update_text_browser(self,Response: str, Caller: str = None, Color: str = "#727272", Space : bool = False):
        if Caller != None:
            if Space:
                self.textBrowser.append(f"<span style=\"color:{Color};\"><br>{Caller}: {Response}<br></span>")
            else:
                self.textBrowser.append(f"<span style=\"color:{Color};\">{Caller}: {Response}</span>")

        else:
            if Space:
                self.textBrowser.append(f"<span style=\"color:{Color};\"><br>{Response}<br></span>")
            else:
                self.textBrowser.append(f"<span style=\"color:{Color};\">{Response}</span>")
        #self.textBrowser.moveCursor(QtGui.QTextCursor.End)
    
    #MENU

    def ClearChat(self):
        self.textBrowser.clear()

    def SystemTray(self):
        if self.systrayactive:
            if self.icon.isVisible():
                self.icon.setVisible(False)
            else:
                self.icon.setVisible(True)
        else:
            self.systrayactive = True
            self.icon = self.childsystray(self.threadmngr,parent=self)
            self.icon.show()


    def Maximize(self):

        self.showMaximized()

    def Minimize(self):
        self.showMinimized()

    def Exit(self):
        if self.systrayactive and self.icon.isVisible():
            self.hide()
        else:
            self.close()
            if self.spkrclass.stream != None:
                if self.spkrclass.stream.is_active():
                    self.spkrclass.stop(False)
                self.spkrclass.terminate()



