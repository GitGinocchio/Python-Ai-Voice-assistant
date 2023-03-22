from PyQt5.QtWidgets import QSystemTrayIcon,QMenu,QAction
from PyQt5.QtGui import QIcon
#-----------------------------------------------------------------------------
from datastructures import Djson, path

class Ui_SysTray(QSystemTrayIcon):
    def __init__(self,threadmngr,parent):
        super().__init__(parent)
        self.threadmngr = threadmngr
        self.setIcon(QIcon(fr'{path}\Assets\icons\mic.ico'))
        #----------------------------------------------------------------
        #Menus
        self.Menu = QMenu()
        self.SubMenu = QMenu(title="Settings")
        #Actions
        self.Menu.addMenu(self.SubMenu)
        self.showMainWindow = QAction(text="Main Window",parent=self)
        self.Menu.addAction(self.showMainWindow)
        #----------------------------------------------------------------
        self.setContextMenu(self.Menu)
        #----------------------------------------------------------------
        self.activated.connect(self.IconClicked)
        self.showMainWindow.triggered.connect(self._ShowMainWindow)

    def IconClicked(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.setIcon(QIcon(fr'{path}\Assets\icons\mic_green.png'))
            self.parent().DisableAll(True)
            self._Start_Listener_Thread()
        if reason == QSystemTrayIcon.ActivationReason.MiddleClick:
            print("middle click")
        if reason == QSystemTrayIcon.ActivationReason.Context:
            print("Context click")            
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            print("Trigger click")      
        if reason == QSystemTrayIcon.ActivationReason.Unknown:
            print("Unknown click") 

    def _ShowMainWindow(self):
        if self.parent().isVisible():
            self.parent().hide()
        else:
            self.parent().show()

    def _Start_Listener_Thread(self):
        try:
            content = Djson.content()
            name = content["sys_data"]["input_devices"]["selected"]["name"]
            index = content["sys_data"]["input_devices"]["selected"]["index"]
            if len(index) != 0 and type(index[0]) == type(0): device = index[0]
            else: device = name[0]
        except IndexError as e:
            print(e)
        else:
            if content["settings"]["always_listen"]["with_sys_tray_active"]:
                if content["settings"]["ask"]["with_sys_tray_active"]:
                    self.Listener_Thread = self.threadmngr(index=2,parent=self.parent(),Question="Cosa posso fare per te?",CallerNeeded=True,device=device)
                    self.Listener_Thread.start(0)
                    self.Listener_Thread.any_signal.connect(self._Start_Processing_Thread)
                else:
                    self.Listener_Thread = self.threadmngr(index=2,parent=self.parent(),CallerNeeded=True,device=device)
                    self.Listener_Thread.start(0)
                    self.Listener_Thread.any_signal.connect(self._Start_Processing_Thread)
            else:
                if content["settings"]["ask"]["with_sys_tray_active"]:
                    self.Listener_Thread = self.threadmngr(index=2,parent=self.parent(),Question="Cosa posso fare per te?",Repeat=1,CallerNeeded=True,device=device)
                    self.Listener_Thread.start(0)
                    self.Listener_Thread.any_signal.connect(self._Start_Processing_Thread)
                else:
                    self.Listener_Thread = self.threadmngr(index=2,parent=self.parent(),Repeat=1,CallerNeeded=True,device=device)
                    self.Listener_Thread.start(0)
                    self.Listener_Thread.any_signal.connect(self._Start_Processing_Thread)                      
    
    def _Start_Processing_Thread(self,message: str):
        self.parent().DisableAll(True)
        self.setIcon(QIcon(fr'{path}\Assets\icons\mic.png'))
        if message != 'None':
            self.message = message
            self.Processing_data_Thread = self.threadmngr(index=1,parent=self.parent(),message=self.message,SPEAK=False)
            self.Processing_data_Thread.start(0)
            content = Djson.content()
            if content["settings"]["always_listen"]["with_sys_tray_active"]:
                self.setIcon(QIcon(fr'{path}\Assets\icons\mic_green.png'))
                self.parent().DisableAll(True)
                self.Processing_data_Thread.any_signal.connect(self._Start_Listener_Thread)
