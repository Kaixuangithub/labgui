# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 13:18:32 2012

@author: Benjamin Schmidt

TODO:
    - add toolbar for plot navigation
    - more descriptive output in print 
    - disable appropriate inputs when acquisition starts
    - end thread more gracefully    
    - move instrument objects to main thread / shared?
    - print the right axes as well as the left
"""

from __future__ import division
import time

# import like this because everything starts with Q anyways and it keeps
# the code just slightly cleaner
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from PyQt4.QtSvg import *
import PyQt4.QtGui as QtGui, PyQt4.QtCore as QtCore

import numpy as np

import visa

from mplZoomWidget import MatplotlibZoomWidget
import ui_recordsweep

import DataTakerThread as DTT
import readconfigfile


# Not sure what this is for - it's copy-paste from some example.
try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class RecordSweepWindow(QMainWindow, ui_recordsweep.Ui_RecordSweepWindow):
    # Don't increase this without debugging - it's the size of the colour list 
    MAX_CHANNELS = 10
    
    # instruments available as well as parameters and unit lists
    [INSTRUMENT_TYPES,AVAILABLE_PARAMS,UNITS]=readconfigfile.get_drivers(readconfigfile.get_drivers_path())

    def __init__(self, MainDTT,parent=None):
        # run the initializer of the class inherited from
        super(RecordSweepWindow, self).__init__()
        
        # this is where most of the GUI is made
        self.setupUi(self)
        self.customizeUi()
        # set up a separate thread for taking data. When data is ready, it 
        # should emit a signal which will triger self.update_data here
        #self.lock = threadlock         
        self.datataker = MainDTT#DTT.DataTakerThread(self.lock, self)  
        self.connect(self.datataker, SIGNAL("data(PyQt_PyObject)"),
                     self.update_data)
        self.connect(self.datataker, SIGNAL("script_finished(bool)"),
                     self.script_finished_cleanup)

        # axes and figure initialization - short names for convenience        
        self.fig = self.mplwidget.figure
        self.ax = self.mplwidget.axes
        self.axR = self.mplwidget.axesR

        self.fig.canvas.draw()              
        
        # this is for a feature that doesn't exist yet
        self.history_length = 0
        
        # objects to hold line data. Plot empty lists just to make handles
        # for line objects of the correct color
        line_set_L = []
        line_set_R = []
        for i in range (self.MAX_CHANNELS):            
            line1, = self.ax.plot([], [], self.color_set[i])     
            line2, = self.axR.plot([], [], self.color_set[i])
            
            line_set_L.append(line1)
            line_set_R.append(line2)
        
        self.ax.lines = line_set_L
        self.axR.lines = line_set_R

        # create the empty data array and use channel 0 as X by default
        self.data_array = np.array([])
        self.chan_X = 0
        
        self.refresh_instrument_list()
        try:
            self.load_settings(readconfigfile.get_settings_name())
        except:
            print "the setting file couldn't be open"
            
        self.outputFileLineEdit.setText(readconfigfile.get_file_name() + '.dat') 
        
        self.scriptFileLineEdit.setText(readconfigfile.get_script_name()) 
        
    def customizeUi(self):       
        #Contains the name of the value measured that will be used for axis labeling
        self.lineEdit_Name = []
        #Contains the name of the instruments' drivers
        self.comboBox_Type = []
        #Contains the GPIB address of the instruments
        self.comboBox_Instr = []
        #Contains the list of parameters of an instrument
        self.comboBox_Param = []  
        #Tick which measured quantity will be diplayed on X axis
        self.radioButton_X = [] 
        #Tick which measured quantity will be diplayed on Y left axis
        self.checkBox_Y = [] 
        #Tick which measured quantity will be diplayed on Y right axis
        self.checkBox_YR = []
        
        
        # create a layout within the blank "plot_holder" widget and put the 
        # custom matplotlib zoom widget inside it. This way it expands to fill
        # the space, and we don't need to customize the ui_recordsweep.py file
        self.gridLayout_2 = QtGui.QGridLayout(self.plot_holder)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        
        self.mplwidget = MatplotlibZoomWidget(self.plot_holder)
        self.mplwidget.setObjectName(_fromUtf8("mplwidget")) 
        self.gridLayout_2.addWidget(self.mplwidget, 0, 0, 1, 1)
  
   
        self.color_set = ['cyan', 'black', 'blue', 'red', 'green', 'orange', 'magenta', 'maroon', 'plum','violet'] 
        
        #Fills self.lineEdit_Name = [], self.comboBox_Type = [], self.comboBox_Instr = []. self.comboBox_Param = []
        #Whenever connect(obbject,SIGNAL(),function) is used it will call the function whenever the object is manipulated or something emits the same SIGNAL()
        for i in range (self.MAX_CHANNELS):   

            pos_LE = lambda x: (20 * x + 1) + 50
            
            self.lineEdit_Name.append(QtGui.QLineEdit(self.groupBox_Name))
            self.lineEdit_Name[i].setGeometry(QtCore.QRect(10, pos_LE(i), 81, 16))
            self.lineEdit_Name[i].setText(QtGui.QApplication.translate("RecordSweepWindow", "", None, QtGui.QApplication.UnicodeUTF8))
            self.lineEdit_Name[i].setObjectName(_fromUtf8("lineEdit_Name"))
            self.lineEdit_Name[i].setStyleSheet('QLineEdit {color: %s}'%self.color_set[i])           
            
            self.comboBox_Type.append(QtGui.QComboBox(self.groupBox_Type))
            self.comboBox_Type[i].setGeometry(QtCore.QRect(5, 20 * (i+1), 71, 16))
            self.comboBox_Type[i].setObjectName(_fromUtf8("comboBox"))
            self.comboBox_Type[i].addItems(self.INSTRUMENT_TYPES)
            self.connect(self.comboBox_Type[i], QtCore.SIGNAL("currentIndexChanged(int)"), self.ComboBoxTypeHandler)                  

            self.comboBox_Instr.append(QtGui.QComboBox(self.groupBox_Instr))
            self.comboBox_Instr[i].setGeometry(QtCore.QRect(5, 20 * (i+1), 71, 16))
            self.comboBox_Instr[i].setObjectName(_fromUtf8("comboBox"))
            
            self.comboBox_Param.append(QtGui.QComboBox(self.groupBox_Param))
            self.comboBox_Param[i].setGeometry(QtCore.QRect(5, 20 * (i+1), 71, 16))
            self.comboBox_Param[i].setObjectName(_fromUtf8("comboBox"))

            self.radioButton_X.append(QtGui.QRadioButton(self.groupBox_X))
            self.radioButton_X[i].setGeometry(QtCore.QRect(7, 20*(i+1), 16, 16))
            self.radioButton_X[i].setText(_fromUtf8(""))
            self.radioButton_X[i].setObjectName(_fromUtf8("radioButton_" + str(i)))
            self.connect(self.radioButton_X[i], QtCore.SIGNAL("toggled(bool)"), self.XRadioButtonHandler)                          
      
            self.checkBox_Y.append(QtGui.QCheckBox(self.groupBox_Y))
            self.checkBox_Y[i].setGeometry(QtCore.QRect(5, 20 * (i+1), 16, 16))
            self.checkBox_Y[i].setText(_fromUtf8(""))
            self.checkBox_Y[i].setObjectName(_fromUtf8("checkBox_" +str(i)))  
            self.connect(self.checkBox_Y[i], QtCore.SIGNAL("stateChanged(int)"), self.YCheckBoxHandler)     
            
            self.checkBox_YR.append(QtGui.QCheckBox(self.groupBox_YR))
            self.checkBox_YR[i].setGeometry(QtCore.QRect(5, 20 * (i+1), 16, 16))
            self.checkBox_YR[i].setText(_fromUtf8(""))
            self.checkBox_YR[i].setObjectName(_fromUtf8("checkBox_" +str(i)))  
            self.connect(self.checkBox_YR[i], QtCore.SIGNAL("stateChanged(int)"), self.YCheckBoxHandler)     
            
        #Creates actions that will be used to fill menus
        self.fileSaveSettingsAction = self.createAction("Save Settings", slot=self.fileSaveSettings, shortcut=QtGui.QKeySequence.SaveAs,
                                        icon=None, tip="Save the current instrument settings")
        
        self.fileLoadSettingsAction = self.createAction("Load Settings", slot=self.fileLoadSettings, shortcut=QtGui.QKeySequence.Open,
                                        icon=None, tip="Load instrument settings from file")               
        
        self.fileSaveFigAction = self.createAction("&Save Figure", slot=self.fileSaveFig, shortcut=QtGui.QKeySequence.Save,
                                        icon=None, tip="Save the current figure")      
        
        self.filePrintAction = self.createAction("&Print Report", slot=self.filePrint, shortcut=QtGui.QKeySequence.Print,
                                        icon=None, tip="Print the figure along with relevant information")                   
        
        self.plotToggleControlLAction = self.createAction("Toggle &Left Axes Control", slot=self.toggleControlL, shortcut=QtGui.QKeySequence("Ctrl+L"),
                                        icon="toggleLeft", tip="Toggle whether the mouse adjusts Left axes pan and zoom", checkable=True)                   

        self.plotToggleControlRAction = self.createAction("Toggle &Right Axes Control", slot=self.toggleControlR, shortcut=QtGui.QKeySequence("Ctrl+R"),
                                        icon="toggleRight", tip="Toggle whether the mouse adjusts right axes pan and zoom", checkable=True)                   

        self.plotToggleXControlAction = self.createAction("Toggle &X Axes Control", slot=self.toggleXControl, shortcut=QtGui.QKeySequence("Ctrl+X"),
                                        icon="toggleX", tip="Toggle whether the mouse adjusts x axis pan and zoom", checkable=True)                   
                    
        self.plotAutoScaleXAction = self.createAction("Auto Scale X", slot=self.toggleAutoScaleX, shortcut=QtGui.QKeySequence("Ctrl+A"),
                                        icon="toggleAutoScaleX", tip="Turn autoscale X on or off", checkable=True)                   
                    
        self.plotAutoScaleLAction = self.createAction("Auto Scale L", slot=self.toggleAutoScaleL, shortcut=QtGui.QKeySequence("Ctrl+D"),
                                        icon="toggleAutoScaleL", tip="Turn autoscale Left Y on or off", checkable=True)                   

        self.plotAutoScaleRAction = self.createAction("Auto Scale R", slot=self.toggleAutoScaleR, shortcut=QtGui.QKeySequence("Ctrl+E"),
                                        icon="toggleAutoScaleR", tip="Turn autoscale Right Y on or off", checkable=True)                   
                            
        self.plotDragZoomAction = self.createAction("Drag to zoom", slot=self.toggleDragZoom, shortcut=QtGui.QKeySequence("Ctrl+Z"),
                                        icon="zoom", tip="Turn drag to zoom on or off", checkable=True)                   

        self.plotPanAction = self.createAction("Drag to Pan", slot=self.togglePan, shortcut=QtGui.QKeySequence("Ctrl+P"),
                                        icon="pan", tip="Turn drag to Pan on or off", checkable=True)                   
         
        self.changeXscale=self.createAction("Set X log", slot=self.setXscale, shortcut=None,
                                        icon="logX", tip="Set the x scale to log")
        self.changeYscale=self.createAction("Set Y log", slot=self.setYscale, shortcut=None,
                                        icon="logY", tip="Set the y scale to log")
        self.changeYRscale=self.createAction("Set YR log", slot=self.setYRscale, shortcut=None,
                                        icon="logY", tip="Set the yr scale to log")
        
        #Fills up the menus displayed on the top left of the window (default position)
        self.fileMenu = self.menuBar().addMenu("File")  

        self.fileMenu.addAction(self.fileLoadSettingsAction)
        self.fileMenu.addAction(self.fileSaveSettingsAction)
        self.fileMenu.addAction(self.filePrintAction)       
        self.fileMenu.addAction("Refresh Instrument List", self.refresh_instrument_list)
        self.fileMenu.addAction(self.fileSaveFigAction)
        

        
        self.plotMenu = self.menuBar().addMenu("&Plot")
        
        self.plotMenu.addAction(self.plotToggleXControlAction)
        self.plotMenu.addAction(self.plotToggleControlLAction)
        self.plotMenu.addAction(self.plotToggleControlRAction)

        self.plotMenu.addAction(self.plotAutoScaleXAction)    
        self.plotMenu.addAction(self.plotAutoScaleLAction)  
        self.plotMenu.addAction(self.plotAutoScaleRAction)
        
        self.plotMenu.addAction(self.plotPanAction)
        self.plotMenu.addAction(self.plotDragZoomAction)
        
        
        #why not self.plotToolbar ?
        plotToolbar = self.addToolBar("Plot")
        plotToolbar.addAction(self.plotToggleXControlAction)
        plotToolbar.addAction(self.plotToggleControlLAction)
        plotToolbar.addAction(self.plotToggleControlRAction)

        plotToolbar.addAction(self.plotAutoScaleXAction)
        plotToolbar.addAction(self.plotAutoScaleLAction)
        plotToolbar.addAction(self.plotAutoScaleRAction)   

        plotToolbar.addAction(self.plotPanAction)
        plotToolbar.addAction(self.plotDragZoomAction)   
        plotToolbar.addAction(self.changeXscale)
        plotToolbar.addAction(self.changeYscale)
        plotToolbar.addAction(self.changeYRscale)
        self.tabWidget.setCurrentIndex(0)
    
    #change the x axis scale to linear if it was log and reverse
    def set_Xaxis_scale(self,axis):
        curscale=axis.get_xscale()
#        print curscale
        if curscale=='log':
            axis.set_xscale('linear')
        elif curscale=='linear':
            axis.set_xscale('log')
           
    #change the y axis scale to linear if it was log and reverse
    def set_Yaxis_scale(self,axis):
        curscale=axis.get_yscale()
#        print curscale
        if curscale=='log':
            axis.set_yscale('linear')
        elif curscale=='linear':
            axis.set_yscale('log')
    
    def setXscale(self):
        self.set_Xaxis_scale(self.ax)
    def setYscale(self):
        self.set_Yaxis_scale(self.ax)
    def setYRscale(self):
        self.set_Yaxis_scale(self.axR)
        
    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):     
        action = QtGui.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon("./images/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, QtCore.SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action        
    
    def refresh_instrument_list(self):
        """ Load instrument list for use in combo boxes """       
        try:
            self.AVAILABLE_PORTS = visa.get_instruments_list()
        except visa.VisaIOError as e:
            if e.error_code == -1073807343:
                print "GPIB does not seem to be connected"
            self.AVAILABLE_PORTS = ["GBIB0::" +str(i) for i in range(10)]        
        except:
            print "Unknown GPIB problem."
            
    def toggleAutoScaleX(self):
        if self.plotAutoScaleXAction.isChecked():
            self.plotToggleXControlAction.setChecked(False)   
        else:
            self.plotToggleXControlAction.setChecked(True)    
        self.updateZoomSettings()

    def toggleAutoScaleL(self):
        if self.plotAutoScaleLAction.isChecked():
            self.plotToggleControlLAction.setChecked(False)            
        else:
            self.plotToggleControlLAction.setChecked(True)              
        self.updateZoomSettings()

    def toggleAutoScaleR(self):
        if self.plotAutoScaleRAction.isChecked():
            self.plotToggleControlRAction.setChecked(False)            
        else:       
            self.plotToggleControlRAction.setChecked(True)      
        self.updateZoomSettings()
        
    def toggleXControl(self):
        if self.plotToggleXControlAction.isChecked():
            self.plotAutoScaleXAction.setChecked(False)             
        self.updateZoomSettings()
            
    def toggleControlL(self):
        if self.plotToggleControlLAction.isChecked():
            self.plotAutoScaleLAction.setChecked(False)               
        self.updateZoomSettings()
         
    def toggleControlR(self):
        if self.plotToggleControlLAction.isChecked():
            self.plotAutoScaleRAction.setChecked(False)             
        self.updateZoomSettings()

    def togglePan(self):
        if self.plotDragZoomAction.isChecked():
            self.plotDragZoomAction.setChecked(False)             
        self.updateZoomSettings()

    def toggleDragZoom(self):
        if self.plotPanAction.isChecked():
             self.plotPanAction.setChecked(False)             
        self.updateZoomSettings()
            
    def updateZoomSettings(self):
        self.mplwidget.setActiveAxes(self.plotToggleXControlAction.isChecked(), 
                                     self.plotToggleControlLAction.isChecked(), 
                                     self.plotToggleControlRAction.isChecked()) 
        if self.plotDragZoomAction.isChecked():                              
            self.mplwidget.mouseMode = self.mplwidget.ZOOM_MODE
        elif self.plotPanAction.isChecked():
            self.mplwidget.mouseMode = self.mplwidget.PAN_MODE
            
        
        self.ax.set_autoscalex_on(self.plotAutoScaleXAction.isChecked())
        self.ax.set_autoscaley_on(self.plotAutoScaleLAction.isChecked())
        self.axR.set_autoscaley_on(self.plotAutoScaleRAction.isChecked())        
      
    def fileSaveFig(self):
        fname = str(QFileDialog.getSaveFileName(self, 'Open settings file', './'))
        if fname:
            self.fig.savefig(fname)

    def fileSaveSettings(self):
        fname = str(QFileDialog.getSaveFileName(self, 'Save settings file as', './'))
        if fname:
            self.save_settings(fname)
        
    def fileLoadSettings(self):  
        fname = str(QFileDialog.getOpenFileName(self, 'Open settings file', './'))       
        if fname:
            self.load_settings(fname)

    def filePrint(self):
        """Sends the current plot to a printer"""
        
        printer = QPrinter()
        
        # Get the printer information from a QPrinter dialog box
        dlg = QPrintDialog(printer)        
        if(dlg.exec_()!= QDialog.Accepted):
             return
             
        p = QPainter(printer)
        
        # dpi*3 because otherwise it looks pixelated (not sure why, bug?)
        dpi = printer.resolution() * 3
        
        # copy the current figure contents to a standard size figure
        fig2 = figure(figsize=(8,5), dpi = dpi)

        ax = fig2.add_subplot(1,1,1)
        for line in self.ax.lines:
            if line.get_xdata() != []:
                ax.plot (line.get_xdata(), line.get_ydata(), label= line.get_label())
        ax.set_xlim(self.ax.get_xlim())
        ax.set_ylim(self.ax.get_ylim())
        ax.set_xlabel(self.ax.get_xlabel())
        ax.set_ylabel(self.ax.get_ylabel())        
        
        # support for printing right axes should go here        
        
        # Shink current axis by 20%
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        
        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
        fig2.savefig("temp.png", dpi=dpi) 
        
        
        # half inch margins
        margin_top = 0.5*dpi
        margin_left = 0.5*dpi       
        
        # matplotlib's svg rendering has a bug if the data extends beyond the
        # plot limits. Below is what would be used for temp.svg
        #svg = QtSvg.QSvgRenderer("temp.svg")
        #svg.render(p, QRectF(margin_top,margin_left, 8*dpi, 5*dpi))

        p.drawImage(QRectF(margin_top,margin_left, 8*dpi, 5*dpi), 
                    QImage("temp.png", format='png'))
        p.drawText(margin_left, 600, "Data recorded to: " + self.out_file.name)
        print "about to send to printer"        
        p.end()           

           
    def load_settings(self, fname):
        """ Load in instrument and initial plot settings from a file"""

        settings_file = open(fname)
        
        idx = 0
        for li in self.lineEdit_Name:
            li.setText('')
            
        for line in settings_file:
            # file format is comma-separated list of settings for each channel
            settings = line.split(',')
            self.lineEdit_Name[idx].setText(settings[0])
            instr_type = settings[1].strip().upper()
            
            if instr_type in self.INSTRUMENT_TYPES:           
                # set the index to the index corresponding to the instrument 
                # type (found using the findtext function)
                self.comboBox_Type[idx].setCurrentIndex(
                                  self.comboBox_Type[idx].findText(instr_type))
                
                if instr_type == "TIME":
                    self.comboBox_Instr[idx].clear()
                else:
                    port = settings[2].strip().upper()
                    
                    # if the port appears to be valid, select it in the box
                    # otherwise add it, but show an icon indicating the problem
                    if port in self.AVAILABLE_PORTS:
                        self.comboBox_Instr[idx].setCurrentIndex(
                                       self.comboBox_Instr[idx].findText(port))
                    else:
                        self.comboBox_Instr[idx].addItem(
                                                QIcon("not_found.png"), port)
                        self.comboBox_Instr[idx].setCurrentIndex(
                                            self.comboBox_Instr[idx].count()-1)
                        
                    self.comboBox_Param[idx].clear()
                    self.comboBox_Param[idx].addItems(
                                             self.AVAILABLE_PARAMS[instr_type])

                    param = settings[3].strip().upper()
                    if param in self.AVAILABLE_PARAMS[instr_type]:                       
                        self.comboBox_Param[idx].setCurrentIndex(
                                      self.comboBox_Param[idx].findText(param))
                                      
            X_checked = (settings[4].strip().upper() == "TRUE")
            Y_checked = (settings[5].strip().upper() == "TRUE")
            self.radioButton_X[idx].setChecked(X_checked)
            self.checkBox_Y[idx].setChecked(Y_checked)
            
            idx +=1
        
        settings_file.close()
        
        #manually call these to update the axes labels
        self.XRadioButtonHandler()
        self.YCheckBoxHandler()
        
        #focus on the instrument settings, not plot settings
        self.tabWidget.setCurrentIndex(0)
        
        
    def save_settings(self, fname):
        """Generates a settings file that can be read with load_settings."""        
        
        settings_file = open(fname, 'w')
        
        idx = 0
        for idx in range (self.MAX_CHANNELS):
            name = str(self.lineEdit_Name[idx].text())
            if name and not name.isspace(): 
                settings_file.write(self.lineEdit_Name[idx].text() +', ')
                settings_file.write(self.comboBox_Type[idx].currentText() +', ')
                settings_file.write(self.comboBox_Instr[idx].currentText() +', ')
                settings_file.write(self.comboBox_Param[idx].currentText() +', ')
                settings_file.write(str(self.radioButton_X[idx].isChecked()) +', ')
                settings_file.write(str(self.checkBox_Y[idx].isChecked()) +'\n')
        settings_file.close()
        
        
    def XRadioButtonHandler(self):
        """Update which data is used for the X axis"""
        for num, box in enumerate(self.radioButton_X):
            if box.isChecked():
                self.chan_X = num
                self.ax.set_xlabel(self.lineEdit_Name[num].text())
                
        self.update_plot() 
        
    def YCheckBoxHandler(self):  
        """Update which data is used for the Y axis (both left and right)"""
        label = ""
        
        for num, box in enumerate(self.checkBox_Y):
            if box.isChecked():
                name = str(self.lineEdit_Name[num].text())
                unit = self.UNITS[str(self.comboBox_Param[num].currentText())]
                label = label + name + " (" + unit + ")" + ", "
        self.ax.set_ylabel(label.rstrip(', '))

        label = ""
        for num, box in enumerate(self.checkBox_YR):
            if box.isChecked():
                name = str(self.lineEdit_Name[num].text())
                unit = self.UNITS[str(self.comboBox_Param[num].currentText())]
                label = label + name + " (" + unit + ")" + ", "
        self.axR.set_ylabel(label.rstrip(', '))
        self.update_plot()         
    
    def ComboBoxTypeHandler(self):
        for typeBox, instrBox, paramBox in zip (self.comboBox_Type, 
                                                self.comboBox_Instr, 
                                                self.comboBox_Param):     
            if typeBox == self.sender():
                for i in range(instrBox.count() + 1):
                        instrBox.removeItem(0)
                        
                text = typeBox.currentText()
                if text == "TIME":
                    instrBox.clear()
                else:
                    instrBox.clear()
                    instrBox.addItems(self.AVAILABLE_PORTS)
                paramBox.clear()
                paramBox.addItems(self.AVAILABLE_PARAMS[str(text)])
                    
    def update_data(self, data_set): 
        
        # check if this is the first piece of data
        if self.data_array.size == 0:
            self.data_array = data_set
            
            # need to make sure the shape is 2D even though there's only 
            # one line of data so far
            data_set.shape = [1, data_set.size]
        else:            
            # vstack just appends the data
            self.data_array = np.vstack([self.data_array, data_set])
            
        self.update_plot()

    def update_plot(self): 
        """ put the latest data into the line objects"""

        first = 0
        if self.history_length:
            first = max(0, self.data_array.shape[0] - self.history_length)
            
        
            
        for chan_Y, [line_L, line_R] in enumerate(zip (self.ax.lines, 
                                                       self.axR.lines)):
                                              
            if self.checkBox_Y[chan_Y].isChecked() and self.data_array.size>0:
#                if self.INSTRUMENT_TYPES[self.chan_X]=='TIME':
                line_L.set_data(self.data_array[first:,self.chan_X], 
                                self.data_array[first:, chan_Y])
            else:
                line_L.set_data([],[])
                
            if self.checkBox_YR[chan_Y].isChecked() and self.data_array.size>0:
                line_R.set_data(self.data_array[first:,self.chan_X], 
                                self.data_array[first:, chan_Y])
            else:
                line_R.set_data([],[])
                
        self.mplwidget.rescale_and_draw()
    
    
    def script_finished_cleanup(self, state):
            self.startStopButton.setText("Start")           

    @pyqtSignature("")
    def on_outputFileButton_clicked(self):
        fname = str(QFileDialog.getSaveFileName(self, 'Save output file as', 
                                                self.outputFileLineEdit.text()))
        if fname:
            self.outputFileLineEdit.setText(fname)        

    @pyqtSignature("")
    def on_scriptFileButton_clicked(self):
        fname = str(QFileDialog.getOpenFileName(self, 'Load script from', './scripts/'))
        if fname:
            self.scriptFileLineEdit.setText(fname) 
             
    @pyqtSignature("")
    def on_startStopButton_clicked(self):

        if self.datataker.isStopped():    
            name_list = []
            type_list = []
            dev_list = []
            param_list = []
            
            # for loop gets all the info about the instruments to use
            for lineEdit, cb_Type, cb_Instr, cb_Param  in zip(
                    self.lineEdit_Name, self.comboBox_Type, 
                    self.comboBox_Instr, self.comboBox_Param):
                        
                lineEdit.setReadOnly(True)
                name = str(lineEdit.text())
                if not name.isspace():                    
                    name_list.append(name)
                    type_list.append(str(cb_Type.currentText()))
                    dev_list.append(str(cb_Instr.currentText()))
                    param_list.append(str(cb_Param.currentText()))
                else:
                    name_list.append("None")
                    type_list.append("None")
                    dev_list.append("None")
                    param_list.append("None")                    
           
            for name, line in zip (name_list, self.ax.lines):
                line.set_label(name)
            
            self.tabWidget.setCurrentIndex(1)
            
            self.datataker.output_file_name = str(self.outputFileLineEdit.text())
            self.datataker.script_file_name = str(self.scriptFileLineEdit.text())
            
            self.datataker.initialize(name_list, type_list, dev_list, param_list) 
            self.datataker.start()
            
            self.startStopButton.setText("Stop")          
        else:         
            self.datataker.stop()
            self.startStopButton.setText("Start")   
        

# This snippet makes it run as a standalone program
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = RecordSweepWindow()
    form.show()
    app.exec_()
