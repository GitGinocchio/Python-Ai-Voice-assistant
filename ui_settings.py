from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtGui import QFont
#-----------------------------------------------------------------------------
from datastructures import config,CONFIG_FILE,path,Djson
content = Djson.content()

class Ui_SettingsWindow(QDialog):
    def __init__(self, parent):
        super(Ui_SettingsWindow,self).__init__(parent)
        uic.loadUi(fr'{path}\Assets\Ui\QSettings.ui',self)
        QFontStyle = QFont(content["settings"]["style"]["font"],content["settings"]["style"]["point size"])
        self.setFont(QFontStyle)
        self.setWindowTitle("Settings - Saved")
        self.show()
        
        self.State = True
        self.EnableFuncSaveButton = False
        self.CopiedRow = []
        #---------------------------------------------------------------
        self.ButtonClose.clicked.connect(self._Close)
        self.ButtonSave.clicked.connect(lambda: self._Save(self.tabWidget.currentIndex()))
        self.AddRowButton.clicked.connect(self._AddRow)
        self.RemoveRowButton.clicked.connect(self._RemoveRow)
        self.CopyRowButton.clicked.connect(self._CopyRow)
        self.PastRowButton.clicked.connect(self._PastRow)
        self.tabWidget.setCurrentIndex(0)
        self.General_Settings_load_data()
        self.ButtonSave.setEnabled(False)
        #---------------------------------------------------------------
        self.tabWidget.currentChanged.connect(self._OnTabWidgetChanged)
        #---------------------------------------------------------------
        self.fontComboBox.currentTextChanged.connect(lambda: self._EnableSaveButton(self.EnableFuncSaveButton))
        self.PointSizeBox.valueChanged.connect(lambda: self._EnableSaveButton(self.EnableFuncSaveButton))
        self.TableAppWidget.cellChanged.connect(lambda: self._EnableSaveButton(self.EnableFuncSaveButton))
        self.TableAppWidget.cellClicked.connect(lambda: self._EnableSaveButton(self.EnableFuncSaveButton))
        self.InputComboBox.currentTextChanged.connect(lambda: self._EnableSaveButton(self.EnableFuncSaveButton))
        self.OutputComboBox.currentTextChanged.connect(lambda: self._EnableSaveButton(self.EnableFuncSaveButton))
        self.SaveMicData.stateChanged.connect(lambda: self._EnableSaveButton(self.EnableFuncSaveButton))
        self.Lang.currentTextChanged.connect(lambda: self._EnableSaveButton(self.EnableFuncSaveButton))
        self.Tld.currentTextChanged.connect(lambda: self._EnableSaveButton(self.EnableFuncSaveButton))
        self.Slow.currentTextChanged.connect(lambda: self._EnableSaveButton(self.EnableFuncSaveButton))

    def _OnTabWidgetChanged(self):
        if self.tabWidget.currentIndex() == 0:
            self.EnableFuncSaveButton = False
            self.General_Settings_load_data()
        elif self.tabWidget.currentIndex() == 1:
            self.EnableFuncSaveButton = False
            self.Saved_Apps_load_data()
        elif self.tabWidget.currentIndex() == 2:
            self.EnableFuncSaveButton = False
            self.Audio_load_data()

    def _EnableSaveButton(self, enabled):
        if enabled:
            self.setWindowTitle("Settings - Unsaved")
            self.ButtonSave.setEnabled(True)
    
    #---------------------------------------------------------------
    #load data

    def General_Settings_load_data(self):
        content = Djson.content()
        self.fontComboBox.setCurrentText(content["settings"]["style"]["font"])
        self.PointSizeBox.setValue(content["settings"]["style"]["point size"])
        self.EnableFuncSaveButton = True

    def Saved_Apps_load_data(self):
        self.list = []
        try:
            if self.list == []:
                for app, path in config.items('APPS',False):
                    self.list.append({"APP" : app, "PATH" : path})
                #print(self.list)
                row = 0
                self.TableAppWidget.setRowCount(len(self.list))
                for item in self.list:
                    self.TableAppWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(item["APP"]))
                    self.TableAppWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(item["PATH"]))
                    row += 1
                self.StatusLabel.setText("<font color=\"green\">Status: File uploaded successfully...</font>")
        except Exception as e:
            print(str(e))
            self.StatusLabel.setText("<font color=\"red\">Status: File not uploaded, an error occurred...</font>")
        finally:
            self.list.clear()
            self.EnableFuncSaveButton = True
 
    def Audio_load_data(self):
        content = Djson.content()
        if len(content["sys_data"]["input_devices"]["selected"]) == 2:
            self.InputComboBox.clear()
            self.InputComboBox.addItems([name for index,name in content["sys_data"]["input_devices"]["devices"]])
            self.InputComboBox.setCurrentText(content["sys_data"]["input_devices"]["selected"][1])
        else:
            self.InputComboBox.clear()
            self.InputComboBox.addItems([name for index,name in content["sys_data"]["input_devices"]["devices"]])

        if len(content["sys_data"]["output_devices"]["selected"]) == 2:
            self.OutputComboBox.clear()
            self.OutputComboBox.addItems([name for index,name in content["sys_data"]["output_devices"]["devices"]])
            self.OutputComboBox.setCurrentText(content["sys_data"]["output_devices"]["selected"][1])
        else:
            self.OutputComboBox.clear()
            self.OutputComboBox.addItems([name for index,name in content["sys_data"]["output_devices"]["devices"]])
        
        #---------------------------------------------------------------------------------
        self.Lang.clear()
        self.Lang.addItems(self.parent().spkrclass.get_langs())
        self.Lang.setCurrentText(content["voice_properties"]["GTTS_settings"]["lang"])
        self.Tld.clear()
        self.Tld.addItems(self.parent().spkrclass.get_tlds())
        self.Tld.setCurrentText(content["voice_properties"]["GTTS_settings"]["tld"])
        self.Slow.setCurrentText(content["voice_properties"]["GTTS_settings"]["slow"].capitalize())
        #---------------------------------------------------------------------------------
        self.SaveMicData.setChecked(content["settings"]["save_all_microphone_data"])
        self.EnableFuncSaveButton = True

    #---------------------------------------------------------------
    # Table Widget Functions
    def _AddRow(self):
        currentRow = self.TableAppWidget.currentRow()
        #rowCount = self.TableAppWidget.rowCount()
        self.TableAppWidget.insertRow(currentRow + 1)

    def _RemoveRow(self):
        if self.TableAppWidget.rowCount() > 0:
            currentRow = self.TableAppWidget.currentRow()
            self.TableAppWidget.removeRow(currentRow)

    def _CopyRow(self):
        self.CopiedRow = []
        currentRow = self.TableAppWidget.currentRow()
        currentColumn = self.TableAppWidget.currentColumn()
        #self.TableAppWidget.insertRow(currentRow)
        columnCount = self.TableAppWidget.columnCount()

        for colum in range(columnCount):
            if not self.TableAppWidget.item(currentRow, colum) is None:
                self.CopiedRow.append(self.TableAppWidget.item(currentRow, colum).text()) 

    def _PastRow(self):
        currentRow = self.TableAppWidget.currentRow()
        columnCount = self.TableAppWidget.columnCount()

        for colum in range(columnCount):
            try:
                self.TableAppWidget.setItem(currentRow, colum, QTableWidgetItem(self.CopiedRow[colum]))
            except IndexError:
                self.CopiedRow.clear()
    #---------------------------------------------------------------



    #---------------------------------------------------------------
    def _Save(self, index):
        self.setWindowTitle("Settings - Saved")
        self.ButtonSave.setDisabled(True)
        ###DEPRECATION###
        def Saved_Apps_Saving(self):
            RowCount = self.TableAppWidget.rowCount()
            columnCount = self.TableAppWidget.columnCount()

            New_list = []

            try:
                config['APPS'].clear()

                for Row in range(RowCount):
                    try:
                        current_path = (self.TableAppWidget.item(Row, 1).text())
                    except AttributeError:
                        current_path = "None"
                    try:
                        current_app = (self.TableAppWidget.item(Row, 0).text())
                    except AttributeError:
                        current_app = "None"
           
                    if current_app and current_path != "None":
                        New_list.append({"APP" : current_app, "PATH" : current_path})

                    try:
                        HasOption = config.has_option("APPS",str(current_app).strip())

                        if not HasOption:
                            config['APPS'].update(([[str(current_app).strip(),str(current_path).strip()]]))
                        else:

                            print(str(current_app).strip(),str(current_path).strip())
                            self.State = "Corrupted"
                            #self.OpenDialogError()

                    except Exception as e:
                        print(str(e))

                if self.State == True:
                    #config['APPS'].clear()

                    with open(CONFIG_FILE,'w') as f:
                        config.write(f)

                    self.StatusLabel.setText("<font color=\"green\">Status: File saved successfully</font>")
                elif self.State == "Corrupted":
                    self.StatusLabel.setText("<font color=\"red\">Status: Error saving file, there are two APP with the same NAME or PATH</font>")
                    self.State = True
            except Exception as e:
                self.StatusLabel.setText(f"<font color=\"red\">Status:{str(e)}</font>")

        def Audio_Saving(self):
            content = Djson.content()
            #------------------------------------------------------
            input_device = self.InputComboBox.currentText()
            content["sys_data"]["input_devices"]["selected"].clear()
            content["sys_data"]["input_devices"]["selected"].extend([(index,name) for index,name in content["sys_data"]["input_devices"]["devices"] if name == input_device][0])
            #------------------------------------------------------
            output_device = self.OutputComboBox.currentText()
            content["sys_data"]["output_devices"]["selected"].clear()
            content["sys_data"]["output_devices"]["selected"].extend([(index,name) for index,name in content["sys_data"]["output_devices"]["devices"] if name == output_device][0])
            #------------------------------------------------------
            content["voice_properties"]["GTTS_settings"]["lang"] = self.Lang.currentText()
            content["voice_properties"]["GTTS_settings"]["tld"] = self.Tld.currentText()
            content["voice_properties"]["GTTS_settings"]["slow"] = self.Slow.currentText()
            #------------------------------------------------------
            self.parent().spkrclass.set_device([index for index,name in content["sys_data"]["output_devices"]["devices"] if name == output_device][0])
            self.parent().spkrclass.set_tld(self.Tld.currentText())
            self.parent().spkrclass.set_lang(self.Lang.currentText())
            self.parent().lstnrclass.set_device([index for index,name in content["sys_data"]["input_devices"]["devices"] if name == input_device][0])
            #------------------------------------------------------
            if self.SaveMicData.isChecked():
                content["settings"]["save_all_microphone_data"] = True
            else:
                content["settings"]["save_all_microphone_data"] = False
            #------------------------------------------------------
            Djson.save_to_file(content)

        def Font_Saving(self):
            content = Djson.content()
            #------------------------------------------------------

            Font = self.fontComboBox.currentText()
            Point_Size = self.PointSizeBox.value()
            content["settings"]["style"]["font"] = Font
            content["settings"]["style"]["point size"] = Point_Size
            #------------------------------------------------------
            QFontStyle = QFont(content["settings"]["style"]["font"],content["settings"]["style"]["point size"])

            self.setFont(QFontStyle)
            self.parent().lineEdit.setFont(QFontStyle)
            self.parent().SendButton.setFont(QFontStyle)
            self.parent().textBrowser.setFont(QFontStyle)
            self.parent().menubar.setFont(QFontStyle)

            #------------------------------------------------------
            Djson.save_to_file(content)


        ###CAUSED BY DEPREACATION###
        if index == 0:
            Font_Saving(self)
        if index == 1:
            Saved_Apps_Saving(self)
        elif index == 2:
            Audio_Saving(self)
        
    def _Close(self):
        self.close()


