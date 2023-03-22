from PyQt5.QtWidgets import QApplication
#----------------------------------------------------------------
from ui_mainwindow import Ui_MainWindow
from thread_mngr import ThreadManager
from ui_settings import Ui_SettingsWindow
from ui_systray import Ui_SysTray
#----------------------------------------------------------------
import sys

#print(type(eval("False")), eval("False"))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = Ui_MainWindow(ThreadManager,Ui_SettingsWindow,Ui_SysTray)
    sys.exit(app.exec_())
