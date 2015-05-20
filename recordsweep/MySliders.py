# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 13:42:55 2013

@author: samuelgaucher
"""

#!/usr/bin/env python

###############################
##                           ##
## Modify this code happily. ## 
## S.G.                      ##                    
## Summer 2013               ##
##                           ##
###############################

from PyQt4 import QtCore, QtGui
import time
import thread
import KT2400

#This is mainly for QReadwritelock()
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#import DataTakerThread as DTT
class Slider(QtGui.QGroupBox):

    valueChanged = QtCore.pyqtSignal(int)

    def __init__(self, orientation, title, parent=None):
        super(Slider, self).__init__(title, parent)

        # Create the slider
        self.slider = QtGui.QSlider(orientation)
        self.slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.slider.setTickInterval(1000)
        self.slider.setSingleStep(1)
        
        # Make sure it communicates its position
        self.slider.valueChanged.connect(self.valueChanged)
        
        # Create the man/auto/lock buttons. Set Manual as default
        self.autoButton = QtGui.QRadioButton("Auto Sweep")
        self.manButton = QtGui.QRadioButton("Manual")
        self.lockButton = QtGui.QRadioButton("Lock")
        self.manButton.setChecked(True)
        
        # Create, THEN Connect the slider and spinboxes
        self.createValueControls()
        self.createAutoSweepControls()
        self.autoSweepGroup.setHidden(True)
        
        #self.createStarter("Sweep")
        self.connectEvents()    
        
        # Layout configurations
        direction = QtGui.QBoxLayout.TopToBottom             
        slidersLayout = QtGui.QBoxLayout(direction)
        slidersLayout.addWidget(self.slider)
        slidersLayout.addWidget(self.lockButton)
        slidersLayout.addWidget(self.manButton)        
        slidersLayout.addWidget(self.autoButton)
        slidersLayout.addWidget(self.autoSweepGroup)
        slidersLayout.addWidget(self.controlsGroup)
        #slidersLayout.addWidget(self.starterGroup)
        self.setLayout(slidersLayout)
        
        # Initial values
        """ So weird...those initial values need to be put after the
            layout.addwidget otherwise it just won't work"""
        self.valueSpinBox.setValue(0)
        self.minimumSpinBox.setValue(0)
        self.maximumSpinBox.setValue(30000)
              
    # The following functions are used to set the slider values          
    def setValue(self, value):    
        self.slider.setValue(value)
                
    def setMinimum(self, value):    
        self.slider.setMinimum(value)

    def setMaximum(self, value):    
        self.slider.setMaximum(value)

    # Button actions
    def lockClicked(self):
        print "Slider locked"
        self.slider.setDisabled(True)
        self.minLabel.setDisabled(True)
        self.maxLabel.setDisabled(True)
        self.maxBox.setDisabled(True)
        self.minBox.setDisabled(True)
        self.autoSweepGroup.setHidden(True)
        self.valueSpinBox.setDisabled(True)
        self.minimumSpinBox.setDisabled(True)
        self.maximumSpinBox.setDisabled(True)
        
    def manClicked(self):
        print "Manual Sweep"
        self.slider.setTracking(True)
        self.slider.setUpdatesEnabled(True)
        self.slider.setEnabled(True)
        self.minLabel.setDisabled(True)
        self.maxLabel.setDisabled(True)
        self.maxBox.setDisabled(True)
        self.minBox.setDisabled(True)
        self.autoSweepGroup.setHidden(True)
        self.valueSpinBox.setEnabled(True)
        self.minimumSpinBox.setEnabled(True)
        self.maximumSpinBox.setEnabled(True)
    
    def autoClicked(self):
        print "Automatic Sweep"
        self.slider.setDisabled(True)
        self.minLabel.setDisabled(False)
        self.maxLabel.setDisabled(False)
        self.maxBox.setDisabled(False)
        self.minBox.setDisabled(False)
        self.autoSweepGroup.setHidden(False)
        self.valueSpinBox.setEnabled(True)
        self.minimumSpinBox.setEnabled(True)
        self.maximumSpinBox.setEnabled(True)
        self.autoSweepGroup.setVisible(True)

    def connectEvents(self):  
        """
        This fuction relates the sliders, SpinBoxes, buttons
        to what they should do.
        """
        # Make the value boxes change the sliders position
        self.valueSpinBox.valueChanged.connect(self.slider.setValue)
   
        # Make the sliders change the SpinBox state
        self.slider.valueChanged.connect(self.valueSpinBox.setValue) 
        
        # Set min and max
        self.minimumSpinBox.valueChanged.connect(self.slider.setMinimum)
        self.maximumSpinBox.valueChanged.connect(self.slider.setMaximum)           

        # Connect button actions
        self.lockButton.clicked.connect(self.lockClicked)
        self.manButton.clicked.connect(self.manClicked)
        self.autoButton.clicked.connect(self.autoClicked)
        
               
                
    def createValueControls(self):
        """
        These are the SpinBoxes that display/control the minimum, maximum
        and actual value of the voltage.
        """
        self.controlsGroup = QtGui.QGroupBox()
        self.controlsGroup.setAlignment(4) # wow this is how to center the title
        
        minimumLabel = QtGui.QLabel("Min.")
        maximumLabel = QtGui.QLabel("Max.")
        valueLabel = QtGui.QLabel("V (mV)")  
        
        self.minimumSpinBox = QtGui.QSpinBox()
        self.minimumSpinBox.setRange(0, 20000)
        self.minimumSpinBox.setSingleStep(1000)
        
        self.maximumSpinBox = QtGui.QSpinBox()
        self.maximumSpinBox.setRange(1, 30000)
        self.maximumSpinBox.setSingleStep(1000)
              
        self.valueSpinBox = QtGui.QSpinBox()
        self.valueSpinBox.setRange(0, 30000)
        self.valueSpinBox.setSingleStep(1)
        
        # Place the labels and SpinBoxes
        controlsLayout = QtGui.QGridLayout()
        controlsLayout.addWidget(minimumLabel, 2, 0)
        controlsLayout.addWidget(maximumLabel, 0, 0)
        controlsLayout.addWidget(valueLabel, 1, 0)
        controlsLayout.addWidget(self.minimumSpinBox, 2, 1)
        controlsLayout.addWidget(self.maximumSpinBox, 0, 1)
        controlsLayout.addWidget(self.valueSpinBox, 1, 1)
        self.controlsGroup.setLayout(controlsLayout)
        

              
    def createAutoSweepControls(self):
        """
        These are the SpinBoxes that display/control the minimum, maximum
        values for the autosweep mode.
        """
        self.autoSweepGroup = QtGui.QGroupBox()
        self.autoSweepGroup.setAlignment(4) # wow this is how to center the title
        
        self.minLabel = QtGui.QLabel("Start:")
        self.maxLabel = QtGui.QLabel("End:")
        self.minBox = QtGui.QSpinBox()
        self.minBox.setMinimum(0)
        self.minBox.setMaximum(30000)
        self.minBox.setRange(0, 30000)
        self.minBox.setSingleStep(1000)
        
        self.maxBox = QtGui.QSpinBox()
        self.maxBox.setMinimum(0)
        self.maxBox.setMaximum(30000)
        self.maxBox.setRange(0, 30000)
        self.maxBox.setSingleStep(1000) 
        
        controlsLayout = QtGui.QGridLayout()
        controlsLayout.addWidget(self.minLabel, 1, 0)
        controlsLayout.addWidget(self.maxLabel, 0, 0)
        controlsLayout.addWidget(self.minBox, 1, 1)
        controlsLayout.addWidget(self.maxBox, 0, 1)
        self.autoSweepGroup.setLayout(controlsLayout)
        
        
        # Initial values, making sure the start value is at the actual slider position
        self.valueSpinBox.valueChanged.connect(self.minBox.setMinimum) # :)
        self.valueSpinBox.valueChanged.connect(self.minBox.setMaximum) # :)

         
                
             
class Window(QtGui.QWidget):
        
    DEBUG=True    
    instrument_array = []
    #sliders = []
    
    def __init__(self,MainDTT):
        super(Window, self).__init__()
        
       # self.LOCK = QReadWriteLock()         
        self.datataker = MainDTT  
#        self.connect(self.datataker, SIGNAL("data(PyQt_PyObject)"),self.update_data)
        
        
        
        KT1 = KT2400.Instrument('GPIB0::25',self.DEBUG)
        self.instrument_array.append(KT1)
        
        KT2 = KT2400.Instrument('GPIB0::26',self.DEBUG)
        self.instrument_array.append(KT2)
        
        KT3 = KT2400.Instrument('GPIB0::27',self.DEBUG)
        self.instrument_array.append(KT3)
        
        self.setWindowTitle("3Sliders")
        self.setGeometry(0, 0, 600, 800)
        
#        for i in range(3):
#            self.sliders.append(Slider(QtCore.Qt.Vertical, "   V"+ str(i+1)))
        
        # Introduce the sliders instances
        self.slider1 = Slider(QtCore.Qt.Vertical, "   V1")
        self.slider2 = Slider(QtCore.Qt.Vertical, "   V2")
        self.slider3 = Slider(QtCore.Qt.Vertical, "   V3")
        
        # This will put the sliders in individual frames  
        self.stackedWidget1 = QtGui.QStackedWidget()
        self.stackedWidget1.addWidget(self.slider1)
        
        self.stackedWidget2 = QtGui.QStackedWidget()
        self.stackedWidget2.addWidget(self.slider2)
        
        self.stackedWidget3 = QtGui.QStackedWidget()
        self.stackedWidget3.addWidget(self.slider3)
        
        # This will call the print functions and display v1, v2, v3 independently
        self.slider1.valueSpinBox.valueChanged.connect(self.print_v1)
        self.slider2.valueSpinBox.valueChanged.connect(self.print_v2)
        self.slider3.valueSpinBox.valueChanged.connect(self.print_v3)
        #self.slider1.valueSpinBox.valueChanged.connect(self.SumVoltages)
        
        # Create the start/stop buttons
        self.createStarter("Sweep")
        
        # Launch the sweep voltage loops and threads
        self.startButton.pressed.connect(self.sweepVolt)
        self.stopButton.pressed.connect(self.enableStart)

                  
        # Place the widgets in the QHBox
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.starterGroup)      
        layout.addWidget(self.stackedWidget1)
        layout.addWidget(self.stackedWidget2) 
        layout.addWidget(self.stackedWidget3)
        self.setLayout(layout)
            

    # store the SpinBox values in variables
    def print_v1(self):
        v = float(self.slider1.valueSpinBox.value())
        v /= 1000
        print "v1 =", v
        self.instrument_array[0].set_voltage(v)
        self.datataker.read_data()
        
        
    def print_v2(self):
        v = float(self.slider2.valueSpinBox.value())
        v /= 1000
        print "v2 =", v
        self.instrument_array[1].set_voltage(v)
        self.datataker.read_data()
        
    def print_v3(self):
        v = float(self.slider3.valueSpinBox.value())
        v /= 1000
        print "v3 =", v
        self.instrument_array[2].set_voltage(v)
        self.datataker.read_data()

    def SumVoltages(self):
        v1 = int(self.slider1.valueSpinBox.value())
        v2 = int(self.slider2.valueSpinBox.value())
        v3 = int(self.slider3.valueSpinBox.value())        
        print "Sum =", v1+v2+v3
        
        
    def createStarter(self, title):
        self.starterGroup = QtGui.QGroupBox(title)
        self.starterGroup.setFixedHeight(145)
        self.starterGroup.setAlignment(4)
         
        # Create all the buttons         
        self.startButton = QtGui.QPushButton("Start") 
        self.recordButton = QtGui.QPushButton("Record") 
        self.stopButton = QtGui.QPushButton("Stop")
        
        # Place the buttons
        starterLayout = QtGui.QGridLayout()
        starterLayout.addWidget(self.startButton, 0, 0)
        starterLayout.addWidget(self.stopButton, 1, 0)
        starterLayout.addWidget(self.recordButton, 2, 0)
        

        self.starterGroup.setLayout(starterLayout)    
    

    
    def sweepVolt(self):
        """
        This function sweeps the voltages either up or down when start button is pressed
        """        
        self.startButton.setDisabled(True)      
                
        def runv1(self):   
            if self.slider1.autoButton.isChecked():
                if self.slider1.maxBox.value() > self.slider1.minBox.value():
                    while self.stopButton.isDown()==False and self.slider1.valueSpinBox.value() < self.slider1.maxBox.value():
                        v1 = self.slider1.valueSpinBox.value()
                        v1+=1
                        self.slider1.valueSpinBox.setValue(v1)
                        time.sleep(0.1)
                        
                elif self.slider1.maxBox.value() < self.slider1.minBox.value():
                    while self.stopButton.isDown()==False and self.slider1.valueSpinBox.value() > self.slider1.maxBox.value():
                        v1 = self.slider1.valueSpinBox.value()
                        v1-=1
                        self.slider1.valueSpinBox.setValue(v1)
                        time.sleep(0.1) 
                    
        def runv2(self):         
            if self.slider2.autoButton.isChecked():
                if self.slider2.maxBox.value() > self.slider2.minBox.value():
                    while self.stopButton.isDown()==False and self.slider2.valueSpinBox.value() < self.slider2.maxBox.value():
                        v2 = self.slider2.valueSpinBox.value()
                        v2+=1
                        self.slider2.valueSpinBox.setValue(v2)
                        time.sleep(0.1)
                    
                elif self.slider2.maxBox.value() < self.slider2.minBox.value():
                        while self.stopButton.isDown()==False and self.slider2.valueSpinBox.value() > self.slider2.maxBox.value():
                            v2 = self.slider2.valueSpinBox.value()
                            v2-=1
                            self.slider2.valueSpinBox.setValue(v2)
                            time.sleep(0.1)
                    
        def runv3(self):           
            if self.slider3.autoButton.isChecked():
                if self.slider3.maxBox.value() > self.slider3.minBox.value():
                    while self.stopButton.isDown()==False and self.slider3.valueSpinBox.value() < self.slider3.maxBox.value():
                        v3 = self.slider3.valueSpinBox.value()
                        v3+=1
                        self.slider3.valueSpinBox.setValue(v3)
                        time.sleep(0.1) 
                    
                elif self.slider3.maxBox.value() < self.slider3.minBox.value():
                        while self.stopButton.isDown()==False and self.slider3.valueSpinBox.value() > self.slider3.maxBox.value():
                            v3 = self.slider3.valueSpinBox.value()
                            v3-=1
                            self.slider3.valueSpinBox.setValue(v3)
                            time.sleep(0.1)


        """ That little piece of code took a week to figure out.
            The multiple threads allow to run while loops for the 
            voltage sweep without freezing the GUI"""
        try:
            thread.start_new_thread(runv1, (self, ))
            thread.start_new_thread(runv2, (self, ))
            thread.start_new_thread(runv3, (self, ))
        except:
             print "Error: unable to start thread"
 


    def enableStart(self):
        """
        You need to define a function if you want to connect a button to the action
        """
        self.startButton.setEnabled(True)
    
        
if __name__ == '__main__':
    
    import sys
    er=QReadWriteLock()
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


  
    

    
    
    
    




