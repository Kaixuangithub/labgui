# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 05:01:18 2013

@author: pf
"""
import sys
import PyQt4.QtGui as QtGui

#just grab the parts we need from QtCore
from PyQt4.QtCore import Qt, SIGNAL, QString, QReadWriteLock, QSettings

#import plot_menu_and_toolbar

import os, string

import QtTools
import readconfigfile

import IOTool as io

import Tool
import DataManagement as DM
import CommandWindow as CW
from demo_signals import CommandWidget
import demo_fit_widget as adw
import MySliders as sl
import numpy as np

import PlotDisplayWindow

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

def pfcount(objet):
    i=0
    for e in objet:
        i=i+1
    return i

def dockWidgetCloseEvent(event):
    event.ignore()

class DialogBox(QtGui.QWidget):
    def __init__(self,label="",windowname="",parent=None):
        super(DialogBox, self).__init__(parent)
        self.grid = QtGui.QGridLayout()
        self.lbl=QtGui.QLabel(label,self)
        self.grid.addWidget(self.lbl,0,0)
        self.txt=QtGui.QLineEdit(self)
        self.grid.addWidget(self.txt,1,0)
        self.bt_ok=QtGui.QPushButton("Ok",self)
        self.grid.addWidget(self.bt_ok,2,0)
#        self.setLayout(self.grid)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout.addLayout(self.grid)

        self.setLayout(self.verticalLayout)
        self.setWindowTitle(windowname)
        self.resize(200, 120) 
    
        self.connect(self.bt_ok, SIGNAL("clicked()"),self.button_click)


    def button_click(self):
        self.emit(SIGNAL("dialogboxanswer(QString)"),self.txt.text())
        self.txt.setText("")
        self.hide()


# A silly little class that both prints and emits the text as a signal
class printerceptor():
    def __init__(self, parent = None):
        self.old_stdout = sys.stdout
        self.parent = parent
        
    def write(self, stri):
        self.old_stdout.write(stri)
        self.parent.emit(SIGNAL("print_to_console(PyQt_PyObject)"), stri)


class LabGui(QtGui.QMainWindow):
    #The command window
    cmdwin=None
    
    outputfile=None
    def __init__(self):
        # run the initializer of the class inherited from6
        super(LabGui, self).__init__()

        self.settings = QSettings(self)
        self.settings.setValue("state", self.saveState())       
        
        #defines the zone in which you can create widgets
        self.zoneCentrale = QtGui.QMdiArea()
        self.zoneCentrale.subWindowActivated.connect(self.update_current_window)
        self.setCentralWidget(self.zoneCentrale)

        self.lock = QReadWriteLock()
        
        #InstrumentHub is responsible for storing and managing the user choices about which instrument goes on which port
        self.instr_hub=Tool.InstrumentHub()
        #DataTaker is responsible for taking data from instruments in the InstrumentHub object
        self.datataker = DM.DataTaker(self.lock,self.instr_hub) 
        
        # handle data emitted by datataker (basically stuff it into a shared,central array)
        self.connect(self.datataker, SIGNAL("data(PyQt_PyObject)"),self.update_data_array)
        self.connect(self.datataker, SIGNAL("script_finished(bool)"),self.finished_DTT)
        self.data_array = np.array([])             


###### DOCK WIDGET SETUP: INSTRUMENT CONNECTION PANEL ###### 
        #contains the intrument list, their name, the port used for connection and the parameter to measure
        self.cmdwin = CW.CommandWindow(Tool.refresh_device_port_list(),self)
        self.connect(self.cmdwin,SIGNAL("ConnectInstrumentHub(bool)"),self.connect_instrument_hub)
        self.connect(self.cmdwin, SIGNAL("colorsChanged()"), self.update_colors) 
        self.connect(self.cmdwin, SIGNAL("labelsChanged()"), self.update_labels) 
        
        instDockWidget = QtGui.QDockWidget("Instrument Setup", self)
        instDockWidget.setObjectName("InstDockWidget")
        instDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        instScrollArea = QtGui.QScrollArea()
        instScrollArea.setWidgetResizable(True)
        instScrollArea.setEnabled(True)
        instScrollArea.setMaximumSize(375, 300)  # optional
        instScrollArea.setWidget(self.cmdwin)
        instDockWidget.setWidget(instScrollArea)
        self.addDockWidget(Qt.RightDockWidgetArea, instDockWidget)


####### DOCK WIDGET SETUP: CALCULATIONS PANEL ###### 
#        #contains live calculations using the output values of the different instruments as inputs 
#        self.calcWidget = CalcWindow.CalcWindow(parent = self)
#        self.connect(self.calcWidget, SIGNAL("colorsChanged()"), self.update_colors) 
#        self.connect(self.calcWidget, SIGNAL("labelsChanged()"), self.update_labels) 
#        calcDockWidget = QtGui.QDockWidget("Live Calculations", self)
#        calcDockWidget.setObjectName("startDockWidget")
#        calcDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
#        #self.connect(self.startWidget.startStopButton,SIGNAL('clicked()'),self.launch_DTT)
#        calcDockWidget.setWidget(self.calcWidget)
#        self.addDockWidget(Qt.RightDockWidgetArea, calcDockWidget)


####### DOCK WIDGET SETUP: START PANEL ###### 
#        #contains the path to save the data, the path to load the script from and the start/stop button
#        self.startWidget = sw.StartWidget(parent = self)
#        startDockWidget = QtGui.QDockWidget("Run experiment", self)
#        startDockWidget.setObjectName("startDockWidget")
#        startDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
#        #self.connect(self.startWidget.startStopButton,SIGNAL('clicked()'),self.launch_DTT)
#        startDockWidget.setWidget(self.startWidget)
#        self.addDockWidget(Qt.RightDockWidgetArea, startDockWidget)


####### DOCK WIDGET SETUP: LOAD PLOT PANEL ###### 
#        #contains the path to load previous data and the plot button
#        self.loadPlotWidget = lpw.LoadPlotWidget(parent = self,load_fname=readconfigfile.get_config_setting("DATAFILE"))
#        loadPlotDockWidget = QtGui.QDockWidget("Load previous data file", self)
#        loadPlotDockWidget.setObjectName("loadPlotDockWidget")
#        loadPlotDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
#        #self.connect(self.startWidget.startStopButton,SIGNAL('clicked()'),self.launch_DTT)
#        loadPlotDockWidget.setWidget(self.loadPlotWidget)
#        self.addDockWidget(Qt.RightDockWidgetArea, loadPlotDockWidget)

###### DOCK WIDGET SETUP: Command widget ###### 
        sender = QtGui.QDockWidget("Start", self)
        self.commandwidget=CommandWidget(parent=self)
        sender.setObjectName("commandDockWidget")
        sender.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        sender.setWidget(self.commandwidget)      
        self.addDockWidget(Qt.RightDockWidgetArea, sender)



###### DOCK WIDGET SETUP: DATA ANALYSE PANEL ###### 
        #contains buttons to create subsets and fit specific functions on go to analyse_data_widget.py for more detailed information
        self.dataAnalyseWidget = adw.AnalyseDataWidget(parent =self)
        analyseDataWidget = QtGui.QDockWidget("Fitting", self)
        analyseDataWidget.setObjectName("analyseDataWidget")
        analyseDataWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        analyseDataWidget.setWidget(self.dataAnalyseWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, analyseDataWidget)
#        self.connect(self.dataAnalyseWidget.addSubsetButton, SIGNAL("clicked()"), self.emit_axis_lim)


###### DOCK WIDGET SETUP: LIMITS MANAGMENT PANEL ###### 
#        self.limitsWidget = lw.LimitsWidget(parent =self)
#        limitsWidget = QtGui.QDockWidget("Limits", self)
#        limitsWidget.setObjectName("limitsWidget")
#        limitsWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
#        limitsWidget.setWidget(self.limitsWidget)
#        self.addDockWidget(Qt.RightDockWidgetArea, limitsWidget)


###### DOCK WIDGET SETUP: CONSOLE PANEL ######         
        #contains all text string emitted by the programm which is not an error message
        self.logTextEdit = QtGui.QTextEdit()
        self.logTextEdit.setReadOnly(True)
        logDockWidget = QtGui.QDockWidget("Output Console", self)
        logDockWidget.setObjectName("LogDockWidget")
        logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea|Qt.BottomDockWidgetArea)
        logDockWidget.setWidget(self.logTextEdit)
        self.addDockWidget(Qt.RightDockWidgetArea, logDockWidget)
        
        
#        self.db=DialogBox("Enter the max number of channel you want to have","Change number of channels")
#        self.db.closeEvent=dockWidgetCloseEvent       
#        self.connect(self.db,SIGNAL("dialogboxanswer(QString)"),self.reset_channel_number)
#        self.db.hide()
        
        #redirect print statements to show a copy on "console"
        sys.stdout = printerceptor(self)
        self.connect(self, SIGNAL("print_to_console(PyQt_PyObject)"), self.update_console) 
        
        
###### FILE MENU SETUP ######       
        self.fileSaveSettingsAction = QtTools.create_action(self, "Save Settings", slot=self.file_save_settings, shortcut=QtGui.QKeySequence.SaveAs,
                                        icon=None, tip="Save the current instrument settings")
        
        self.fileLoadSettingsAction = QtTools.create_action(self,"Load Settings", slot=self.file_load_settings, shortcut=QtGui.QKeySequence.Open,
                                        icon=None, tip="Load instrument settings from file")

        self.fileSaveFigAction = QtTools.create_action(self,"&Save Figure", slot=self.file_save_fig, shortcut=QtGui.QKeySequence.Save,
                                        icon=None, tip="Save the current figure")      
        
        self.filePrintAction = QtTools.create_action(self,"&Print Report", slot=self.file_print, shortcut=QtGui.QKeySequence.Print,
                                        icon=None, tip="Print the figure along with relevant information")                   

        self.fileMenu = self.menuBar().addMenu("File")  
        self.fileMenu.addAction(self.fileLoadSettingsAction)
        self.fileMenu.addAction(self.fileSaveSettingsAction)
        self.fileMenu.addAction(self.filePrintAction)       
        self.fileMenu.addAction(self.fileSaveFigAction)


###### PLOT MENU + TOOLBAR SETUP ######      
        self.plotToggleControlLAction = QtTools.create_action(self,"Toggle &Left Axes Control", slot=self.toggleControlL, shortcut=QtGui.QKeySequence("Ctrl+L"),
                                        icon="toggleLeft", tip="Toggle whether the mouse adjusts Left axes pan and zoom", checkable=True)                   

        self.plotToggleControlRAction = QtTools.create_action(self,"Toggle &Right Axes Control", slot=self.toggleControlR, shortcut=QtGui.QKeySequence("Ctrl+R"),
                                        icon="toggleRight", tip="Toggle whether the mouse adjusts right axes pan and zoom", checkable=True)                   

        self.plotToggleXControlAction = QtTools.create_action(self,"Toggle &X Axes Control", slot=self.toggleXControl, shortcut=QtGui.QKeySequence("Ctrl+X"),
                                        icon="toggleX", tip="Toggle whether the mouse adjusts x axis pan and zoom", checkable=True)                   
                    
        self.plotAutoScaleXAction = QtTools.create_action(self,"Auto Scale X", slot=self.toggleAutoScaleX, shortcut=QtGui.QKeySequence("Ctrl+A"),
                                        icon="toggleAutoScaleX", tip="Turn autoscale X on or off", checkable=True)                   
                    
        self.plotAutoScaleLAction = QtTools.create_action(self,"Auto Scale L", slot=self.toggleAutoScaleL, shortcut=QtGui.QKeySequence("Ctrl+D"),
                                        icon="toggleAutoScaleL", tip="Turn autoscale Left Y on or off", checkable=True)                   

        self.plotAutoScaleRAction = QtTools.create_action(self,"Auto Scale R", slot=self.toggleAutoScaleR, shortcut=QtGui.QKeySequence("Ctrl+E"),
                                        icon="toggleAutoScaleR", tip="Turn autoscale Right Y on or off", checkable=True)                   
                            
        self.plotDragZoomAction = QtTools.create_action(self,"Drag to zoom", slot=self.toggleDragZoom, shortcut=QtGui.QKeySequence("Ctrl+Z"),
                                        icon="zoom", tip="Turn drag to zoom on or off", checkable=True)                   

        self.plotPanAction = QtTools.create_action(self,"Drag to Pan", slot=self.togglePan, shortcut=QtGui.QKeySequence("Ctrl+P"),
                                        icon="pan", tip="Turn drag to Pan on or off", checkable=True)                   

        self.plotSelectAction = QtTools.create_action(self,"Drag to Select", slot=self.toggleSelect, shortcut=QtGui.QKeySequence("Ctrl+L"),
                                        icon="select", tip="Turn drag to Select on or off", checkable=True)         

        self.plotClearSelectAction = QtTools.create_action(self,"Hide selection box", slot=self.hide_selection_box,
                                        icon="clear_select", tip="Hide Selection box", checkable=False)         
                
        
        self.changeXscale=QtTools.create_action(self,"Set X log", slot=self.setXscale, shortcut=None,
                                        icon="logX", tip="Set the x scale to log")
        self.changeYscale=QtTools.create_action(self,"Set Y log", slot=self.setYscale, shortcut=None,
                                        icon="logY", tip="Set the y scale to log")
        self.changeYRscale=QtTools.create_action(self,"Set YR log", slot=self.setYRscale, shortcut=None,
                                        icon="logY", tip="Set the yr scale to log")
        self.removeFitAction = QtTools.create_action(self,"Remove Fit", slot=self.remove_fit, shortcut=None,
                                        icon="clear", tip="Reset the fit data to an empty array") 
        self.clearPlotAction = QtTools.create_action(self,"Clear Plot", slot=self.clear_plot, shortcut=None,
                                        icon="clear", tip="Clears the data arrays")                       

           
        self.plotMenu = self.menuBar().addMenu("&Plot")

        self.plotMenu.addAction(self.plotToggleXControlAction)
        self.plotMenu.addAction(self.plotToggleControlLAction)
        self.plotMenu.addAction(self.plotToggleControlRAction)

        self.plotMenu.addAction(self.plotAutoScaleXAction)    
        self.plotMenu.addAction(self.plotAutoScaleLAction)  
        self.plotMenu.addAction(self.plotAutoScaleRAction)
        
        self.plotMenu.addAction(self.plotPanAction)
        self.plotMenu.addAction(self.plotDragZoomAction)        
        
        self.plotMenu.addAction(self.removeFitAction)
        self.plotMenu.addAction(self.clearPlotAction)
        
        self.plotToolbar = self.addToolBar("Plot")
        self.plotToolbar.setObjectName ( "PlotToolBar")
        
        self.plotToolbar.addAction(self.plotToggleXControlAction)
        self.plotToolbar.addAction(self.plotToggleControlLAction)
        self.plotToolbar.addAction(self.plotToggleControlRAction)

        self.plotToolbar.addAction(self.plotAutoScaleXAction)
        self.plotToolbar.addAction(self.plotAutoScaleLAction)
        self.plotToolbar.addAction(self.plotAutoScaleRAction)   

        self.plotToolbar.addAction(self.plotPanAction)
        self.plotToolbar.addAction(self.plotDragZoomAction)   
        self.plotToolbar.addAction(self.plotSelectAction)
        self.plotToolbar.addAction(self.plotClearSelectAction)
        self.plotToolbar.addAction(self.changeXscale)
        self.plotToolbar.addAction(self.changeYscale)
        self.plotToolbar.addAction(self.changeYRscale)       


##### start/stop/pause buttons ########
        self.start_DTT_action=QtTools.create_action(self,"Start DTT",slot=self.start_DTT,shortcut=QtGui.QKeySequence("F5"),icon="start",tip="Launch DTT")        
        self.stop_DTT_action=QtTools.create_action(self,"Stop DTT",slot=self.stop_DTT,shortcut=QtGui.QKeySequence("F6"),icon="stop",tip="stop DTT")        
        self.pause_DTT_action=QtTools.create_action(self,"Pause DTT",slot=self.pause_DTT,shortcut=QtGui.QKeySequence("F7"),icon="pause",tip="pause DTT")        
        self.pause_DTT_action.setEnabled(False)        
        self.stop_DTT_action.setEnabled(False)
        
        self.instToolbar = self.addToolBar("Instruments")
        self.instToolbar.setObjectName ( "InstToolBar")
        
        self.instToolbar.addAction(self.start_DTT_action)
        self.instToolbar.addAction(self.pause_DTT_action)
        self.instToolbar.addAction(self.stop_DTT_action)
        
        
###### INSTRUMENT MENU SETUP ######      
        self.read_DTT=QtTools.create_action(self,"Read",slot=self.single_measure_DTT,shortcut=None,icon=None,tip="Take a one shot measure with DTT")       
        self.connect_hub=QtTools.create_action(self,"Connect Hub",slot=self.connect_instrument_hub,shortcut=QtGui.QKeySequence("Ctrl+I"),icon=None,tip="Refresh the list of instrument selected")

        self.windowMenu = self.menuBar().addMenu("&Meas/Connect")
        self.windowMenu.addAction(self.start_DTT_action)
        self.windowMenu.addAction(self.read_DTT)
        self.windowMenu.addAction(self.connect_hub)
        
        self.connect(self.commandwidget, SIGNAL("CommandSent(PyQt_PyObject)"), self.start_sweep)
#        self.connect(self.loadPlotWidget.plotButton,SIGNAL("clicked()"),self.create_plw)


###### WINDOW MENU SETUP ######   
        self.add_pdw=QtTools.create_action(self,"Add a plot area",slot=self.create_pdw,shortcut=None,icon=None,tip="Add a recordsweep window")   
        self.add_slider=QtTools.create_action(self,"Add a slider",slot=self.create_slider,shortcut=None,icon=None,tip="Add a slider window")
        
        #self.zoneCentrale.addSubWindow(self.sw)
        self.windowMenu = self.menuBar().addMenu("&Window")        
        self.windowMenu.addAction(self.add_pdw)
        self.windowMenu.addAction(self.add_slider)


##### END OF INIT ##### 
        settings_name=readconfigfile.get_settings_name()
        self.cmdwin.load_settings(settings_name)
#        self.calcWidget.load_settings(settings_name)
        
        #Initialise the InstrumentHub 
        self.connect_instrument_hub()
        #Create the object responsible to display information send by the datataker
        self.data_displayer=DM.DataDisplayer(self.datataker)       
        #show a plot by default
        self.create_pdw() 

        # platform-independent way to restore settings such as toolbar positions,
        # dock widget configuration and window size from previous session.
        self.settings = QSettings("XX Lab", "LabGUI")
        try:
            self.restoreState(self.settings.value("windowState").toByteArray())
            self.restoreGeometry(self.settings.value("geometry").toByteArray()) 
        except:
            pass #no biggie - probably means settings haven't been saved on this machine yet
        
    def closeEvent(self, event): 
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
    
        if reply == QtGui.QMessageBox.Yes:
            self.settings.setValue("windowState", self.saveState())
            self.settings.setValue("geometry", self.saveGeometry())
            self.settings.remove("script_name")
            event.accept()
            
        else:
            event.ignore()  
              
    def create_pdw(self):
        """
            add a new plot display window in the MDI area its channels are labeled according to the channel names on the cmd window.
            It is connected to the signal of data update.
        """
        pdw = PlotDisplayWindow.PlotDisplayWindow(data_array = self.data_array,name="Live Data Window",default_channels=self.instr_hub.get_instrument_nb())#self.datataker)
        self.connect(self, SIGNAL("data_array_updated(PyQt_PyObject)"),
                     pdw.update_plot)
        self.connect(pdw.mplwidget,SIGNAL("limits_changed(int,PyQt_PyObject)"),self.emit_axis_lim)
        
        #this is here temporary, I would like to change the plw when the live fit is ticked
        self.connect(self.dataAnalyseWidget, SIGNAL("data_set_updated(PyQt_PyObject)"),pdw.update_plot)        
        self.connect(self.dataAnalyseWidget, SIGNAL("update_fit(PyQt_PyObject)"), pdw.update_fit)
        self.connect(self,SIGNAL("remove_fit()"), pdw.remove_fit)
        
        self.connect(self, SIGNAL("colorsChanged(PyQt_PyObject)"), pdw.update_colors)             
        self.connect(self, SIGNAL("labelsChanged(PyQt_PyObject)"), pdw.update_labels) 

        self.update_labels()
        self.update_colors()
         
        self.zoneCentrale.addSubWindow(pdw)

        pdw.show()
    

    def create_plw(self):
        """
            add a new plot load window in the MDI area. The data and channels are loaded from a file
        """
        
        load_fname=str(self.loadPlotWidget.load_file_name())
        print "G2GUI.create_plw:loading "+load_fname+ " for plot"
        
        #check what the extension of the file is, one can define specific treatment for each extension
        extension=load_fname.rsplit('.')[len(load_fname.rsplit('.'))-1]
        if extension=="adat":
            [data,labels]=io.load_file_windows(load_fname,'\t')
        elif extension=="adat2":
            [data,labels]=io.load_file_windows(load_fname)
        else:
            [data,labels]=io.load_file_windows(load_fname)
                   
        print "G2GUI.create_plw: channel names are ",labels
        print data
        nb_channels=np.size(data,1)
        print "G2GUI.create_plw: ",nb_channels," channels in total"
        plw = PlotDisplayWindow.PlotDisplayWindow(data_array = data,name="Past Data Window",default_channels=nb_channels)
        self.connect(plw.mplwidget,SIGNAL("limits_changed(int,PyQt_PyObject)"),self.emit_axis_lim)
        self.connect(self.dataAnalyseWidget, SIGNAL("data_set_updated(PyQt_PyObject)"),plw.update_plot)        
        self.connect(self.dataAnalyseWidget, SIGNAL("update_fit(PyQt_PyObject)"), plw.update_fit)
        self.connect(self,SIGNAL("remove_fit()"), plw.remove_fit)
        
       #try to change the labels on the different channels according to the file formatting
        try:
            for i, param in enumerate(labels['param']):  
                plw.lineEdit_Name[i].setText(param)     
        except:
            pass
        #try to select the different channels according to a file with same name but .pset extension
        try:
            plw.set_axis_ticks(io.load_pset_file(load_fname,labels['param']))
        except:
            pass
        
        self.dataAnalyseWidget.load_experiment(load_fname)
        self.dataAnalyseWidget.refresh_active_set()
        self.zoneCentrale.addSubWindow(plw)
        plw.show()    
    
    
    def update_colors(self):
        """
            update the colors of the plot lines
        """
        color_list = self.cmdwin.get_color_list()
        self.emit(SIGNAL("colorsChanged(PyQt_PyObject)"),color_list)

    def update_labels(self):
        """
            update the colors of the plot lines
        """
        label_list = self.cmdwin.get_label_list()
        self.emit(SIGNAL("labelsChanged(PyQt_PyObject)"),label_list)
        
    def update_data_array(self, data_set): 
        """ slot for when the thread emits data """ 
        
        #convert this latest data to an array        
        data = np.array(data_set)

#        for calculation in self.calcWidget.get_calculation_list():
#            calculation = calculation.strip()
#            if calculation:
#                data = np.append(data, eval(calculation + '\n'))
#            else:
#                data = np.append(data, 0)
                
        # writes data and calculated columns
        self.write_data(data.tolist())
        
        # check if this is the first piece of data
        if self.data_array.size == 0:
            self.data_array = data
            
            # need to make sure the shape is 2D even though there's only 
            # one line of data so far
            self.data_array.shape = [1, self.data_array.size]
        else:            
            # vstack just appends the data
            self.data_array = np.vstack([self.data_array, data]) 
            
   
        self.emit(SIGNAL("data_array_updated(PyQt_PyObject)"), self.data_array)
        
    def update_current_window(self, x):
        current_window = self.zoneCentrale.activeSubWindow()
        
        if current_window: 
            current_widget = self.zoneCentrale.activeSubWindow().widget()
            
            # check if the activated window is a plot display
            # chose not to check by type because that could get messed up
            # if import/module names or class names get changed
            try:
                is_plot = current_widget.is_plot_display_window()
            except:
                is_plot = False
            if is_plot:
                # The plot menu and file menu actions need local references to 
                # these attributes of the currently selected plot window
                self.current_pdw = current_widget
                self.fig = current_widget.fig
                self.ax = current_widget.ax
                self.axR = current_widget.axR
                self.mplwidget = current_widget.mplwidget
                self.radioButton_X = current_widget.radioButton_X
                self.checkBox_Y = current_widget.checkBox_Y
              
                # TODO: update actions isChecked() statuses to reflect currently selected window
        else:
            #20130722 it runs this part of the code everytime I click somehwere else that inside the main window
            pass

    def start_sweep(self,data):
        self.datataker.set_sweep(data)
        self.toggle_DTT()
        
    def update_console(self, stri):    
        MAX_LINES = 50

        new_text = str(self.logTextEdit.toPlainText()).rstrip() + '\n' + stri
        stri = str(stri)

        line_list = new_text.splitlines()
        N_lines = min(MAX_LINES, len(line_list)) 
        
        new_text = string.join (line_list[-N_lines:], '\n')        
        
        self.logTextEdit.setPlainText(new_text)
        sb = self.logTextEdit.verticalScrollBar()
        sb.setValue(sb.maximum())

    def emit_axis_lim(self,mode,limits):
        """
            emits the limits of the selected axis on the highlighted plot
        """
        current_window = self.zoneCentrale.activeSubWindow()
        
        if current_window: 
            current_widget = self.zoneCentrale.activeSubWindow().widget()
            
        #this is a small check that we are no trying to get the limits from the wrong plot
            if current_widget.windowTitle()=="Past Data Window":    
                try:
                    paramX=current_widget.get_X_axis_index()
                    paramY=current_widget.get_Y_axis_index()
                except:
                    print "G2GUI.emit_axis_lim : the params are not defined, the default is X-> Channel 1 and Y->Channel 2"
                    paramX=0
                    paramY=1
            else:
                try:
                    paramX=current_widget.get_X_axis_index()
                    paramY=current_widget.get_Y_axis_index()
                except:
                    print "G2GUI.emit_axis_lim : the params are not defined, the default is X-> Channel 1 and Y->Channel 2"
                    paramX=0
                    paramY=1
            try:
                x=current_widget.data_array[:,paramX]
                xmin=limits[0][0]
                xmax=limits[0][1]
                imin=io.match_value2index(x,xmin)
                imax=io.match_value2index(x,xmax) 
                self.emit(SIGNAL("selections_limits(PyQt_PyObject,int,int,int)"),np.array([imin,imax,xmin,xmax]), paramX,paramY,mode)
            except:
                pass
            
    #THE MAIN POINT HERE IS TO MAKE SURE THAT THE COMMANDS SEND TO THE KEITHLEY DOES NOT INTERFERE WITH THE DATA TAKER!!! 
    def create_slider(self):
        #sl.Window(self.datataker)#
        slider=sl.Window(self.datataker)
        self.zoneCentrale.addSubWindow(slider)
        slider.show()
    
##### DATA MANAGEMENT RELATED FUNCTIONS    
    
    def single_measure_DTT(self):
        """
            triggers one measure of all instruments in instrument hub
        """
        self.datataker.initialize() 
        self.datataker.read_data()
        self.datataker.stop()

    def start_DTT(self):
        if self.datataker.isStopped():
            self.start_DTT_action.setEnabled(False)
            self.pause_DTT_action.setEnabled(True)
            self.stop_DTT_action.setEnabled(True)
            
            #self.start_DTT_.setText("Stop DTT")
            
            #just update the color boxes in case
            self.update_colors()
            self.update_labels()
            
            #read the name of the output file and determine if it exists
            of_name="output.txt"#str(self.startWidget.outputFileLineEdit.text())
            is_new_file= not os.path.exists(of_name)

            #if this file is new, the first 2 lines contain the instrument and parameters list
            if is_new_file:
                self.output_file = open(of_name, 'a')
                [instr_name_list,dev_list,param_list]=self.collect_instruments()
                self.output_file.write("#C"+str(self.cmdwin.get_label_list()).strip('[]') + '\n')
                self.output_file.write("#I"+str(self.cmdwin.get_descriptor_list()).strip('[]') + '\n')

                self.output_file.write("#P"+str(param_list).strip('[]') + '\n')

            else:
                #open it in append mode, so it won't erase previous data
                self.output_file = open(of_name, 'a')
                
                
            self.datataker.initialize(is_new_file)
            #read the name of the script file to run
        
            self.datataker.set_script(readconfigfile.get_script_name())           
            #this command is specific to Qthread, it will execute whatever is define in 
            #the method run() from DataManagement.py module
            self.datataker.start()

        elif self.datataker.isPaused():
            print "datataker was paused"
            self.start_DTT_action.setEnabled(False)
            self.pause_DTT_action.setEnabled(True)
            self.stop_DTT_action.setEnabled(True)
            self.datataker.resume()
        else:         
            print "Couldn't start DTT - already running!"
            
    def stop_DTT(self):
        """
            this executes when pressing the stop button
        """
        if not self.datataker.isStopped():  
#            self.datataker.resume()
            self.datataker.stop()
            self.output_file.close()  
            
            self.start_DTT_action.setEnabled(True)
            self.pause_DTT_action.setEnabled(False)
            self.stop_DTT_action.setEnabled(False)
            
            #self.start_DTT.setText("Start DTT")
#            self.startWidget.startStopButton.setText("Start!")
#            self.startWidget.increment_filename()
            #just make sure the pause setting is left as false after ther run
        else:         
            print "Couldn't stop DTT - it wasn't running!"
            
    def pause_DTT(self):
        """
            this executes when pressing the pause button
        """
        if not self.datataker.isStopped():   
            self.start_DTT_action.setEnabled(True)
            self.pause_DTT_action.setEnabled(False)
            self.stop_DTT_action.setEnabled(True)
            self.datataker.pause()
            
    def toggle_DTT(self):
        if self.datataker.isStopped():
            self.start_DTT()
        else:         
            self.stop_DTT()
    
    def finished_DTT(self, completed):
        """
            when the script is over it sends a signal to LabGui which calls this function
        """
        if completed:        
            self.start_DTT_action.setEnabled(True)
            self.pause_DTT_action.setEnabled(False)
            self.stop_DTT_action.setEnabled(False)
            
            #self.start_DTT.setText("Start DTT")
            #just make sure the pause setting is left as false after ther run
            self.datataker.resume(display=False)
            self.output_file.close()  
   
    def write_data(self, data_set):
        """
            this function handles the writing of the data into a file
        """
        if self.output_file:
            if not self.output_file.closed:
                # a quick way to make a comma separated list of the values
                stri = str(data_set).strip('[]\n\r') 
                #numpy arrays include newlines in their strings, get rid of them.
                stri = stri.replace('\n', '') 
                stri = stri.replace(',', ' ')
                
                self.output_file.write(stri + '\n')       
                print '>>' + stri      
     
    def isrunning(self):
        """
            indicates whether the datataker is running or not
        """
        return not self.datataker.stopped


    def connect_instrument_hub(self,signal=True):
        """
            When the button "Connect" is clicked this method actualise the InstrumentHub
            according to what the user choosed in the command window. 
            It cannot change while the DataTaker is running though
        """
        #@ISSUE
        #I should add something here to avoid that we reconnect the instrument hub if the # of instrument is different
        #and also not allow to take data if the current file header doesn't correspond to the intrument hub
        if signal:
            [instr_name_list,dev_list,param_list]=self.collect_instruments()
            actual_instrument_number=len(self.instr_hub.get_instrument_list())
            cmdwin_instrument_number=len(instr_name_list)
            #if the datataker is running the user should not modify the length of the instrument list and connect it
            connect=False
            if self.isrunning():
                if actual_instrument_number == cmdwin_instrument_number or actual_instrument_number==0:
                    connect=True
            else:
                connect=True
            
            if connect:
                print "Connect instrument hub..."
                self.instr_hub.connect_hub(instr_name_list,dev_list,param_list)
                print "...instrument hub connected"
                self.cmdwin.bt_connecthub.setEnabled(False)
            else:
                print
                print "You cannot connect a number of instrument different than "+str(actual_instrument_number)+" when the datataker is running"
                print
            
    def collect_instruments(self):
        """
            gather the text displayed in the comboboxes of the command window
        """
        return self.cmdwin.collect_device_info()
        
##### PLOT RELATED FUNCTIONS #####
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
        
    def remove_fit(self):
        self.emit(SIGNAL("remove_fit()"))
#        self.update_data_array()
    def clear_plot(self):
        self.data_array = np.array([])
        self.emit(SIGNAL("data_array_updated(PyQt_PyObject)"), self.data_array)
        
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
        if self.plotSelectAction.isChecked():
             self.plotSelectAction.setChecked(False)
        self.updateZoomSettings()

    def toggleDragZoom(self):
        if self.plotPanAction.isChecked():
             self.plotPanAction.setChecked(False)  
        if self.plotSelectAction.isChecked():
             self.plotSelectAction.setChecked(False)     
        self.updateZoomSettings()

    def toggleSelect(self):
        if self.plotDragZoomAction.isChecked():
            self.plotDragZoomAction.setChecked(False) 
        if self.plotPanAction.isChecked():
             self.plotPanAction.setChecked(False)   
        self.updateZoomSettings()
    
    def hide_selection_box(self):
        if self.mplwidget.selection_showing:
            self.mplwidget.select_rectangle.remove()
            self.mplwidget.selection_showing = False
            self.mplwidget.figure.canvas.draw()

        
    def updateZoomSettings(self):
        self.mplwidget.setActiveAxes(self.plotToggleXControlAction.isChecked(), 
                                     self.plotToggleControlLAction.isChecked(), 
                                     self.plotToggleControlRAction.isChecked()) 
        if self.plotDragZoomAction.isChecked():                              
            self.mplwidget.set_mouse_mode(self.mplwidget.ZOOM_MODE)
        elif self.plotPanAction.isChecked():
            self.mplwidget.set_mouse_mode(self.mplwidget.PAN_MODE)
        elif self.plotSelectAction.isChecked():
            self.mplwidget.set_mouse_mode(self.mplwidget.SELECT_MODE)  
            
        
        self.mplwidget.set_autoscale_x(self.plotAutoScaleXAction.isChecked())
        self.mplwidget.set_autoscale_yL(self.plotAutoScaleLAction.isChecked())
        self.mplwidget.set_autoscale_yR(self.plotAutoScaleRAction.isChecked())        
        
        
##### SAVING RELATED FUNCTIONS #####        
    def file_save_fig(self):
        fname = str(QtGui.QFileDialog.getSaveFileName(self, 'Open settings file', './'))
        if fname:
            self.fig.savefig(fname)

    def file_save_settings(self):
        fname = str(QtGui.QFileDialog.getSaveFileName(self, 'Save settings file as', './'))
        if fname:
            self.cmdwin.save_settings(fname)
        
    def file_load_settings(self):  
        fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Open settings file', './')) 
        if fname:
            self.cmdwin.load_settings(fname)

    def file_print(self):
        self.current_pdw.print_figure(file_name = self.output_file.name)

    
if __name__=="__main__":
    
    app = QtGui.QApplication(sys.argv)
    ex = LabGui()
    ex.show()
    sys.exit(app.exec_())
