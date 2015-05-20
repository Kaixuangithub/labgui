# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 14:47:26 2014

@author: pfduc
"""
#import matplotlib.pyplot as plt
import PyQt4.QtCore as QtCore
from PyQt4.QtCore import Qt
import PyQt4.QtGui as QtGui
#from PyQt4.QtGui import *
import sys
import numpy as np
from random import random
import PlotDisplayWindow

try:
    _fromUtf8 = QtGui.QString.fromUtf8
except:
    _fromUtf8 = lambda s: s


class CommandWidget(QtGui.QWidget):
    
    def __init__(self, parent = None):
        super(CommandWidget,self).__init__(parent) 
        
        #main layout of the form is the verticallayout
        self.verticalLayout = QtGui.QVBoxLayout()      
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        """
        here will be displayed the button to create subsets and choose between livefit or postfit, also the number of the subset is displayed
        """
        
        self.titleLayout = QtGui.QHBoxLayout()
        
        self.titleLayout.setObjectName(_fromUtf8("titleLayout"))  
        alabel = QtGui.QLabel(self)
        alabel.setText("Sweep in current")
        
        self.verticalLayout.addWidget(alabel)
        
        self.num_loop=None
#        alabel = QtGui.QLabel(self)
#        alabel.setText("Repetition of the measure")
#        self.num_loop = QtGui.QLineEdit (self)
#        self.num_loop.setText("1")
#        self.titleLayout.addWidget(alabel)
#        self.titleLayout.addWidget(self.num_loop)
#        self.verticalLayout.addLayout(self.titleLayout)
        
        self.currentLayout = QtGui.QHBoxLayout()
        
        self.currentLayout.setObjectName(_fromUtf8("currentLayout"))
        self.current_start = QtGui.QLineEdit (self)
        self.current_stop = QtGui.QLineEdit (self)
        self.current_step = QtGui.QLineEdit (self)
        alabel = QtGui.QLabel(self)
        self.currentLayout.addWidget(alabel)
        self.currentLayout.addWidget(self.current_start)
        alabel = QtGui.QLabel(self)
        self.currentLayout.addWidget(alabel)
        self.currentLayout.addWidget(self.current_stop)
        alabel = QtGui.QLabel(self)
        self.currentLayout.addWidget(alabel)
        self.currentLayout.addWidget(self.current_step)
        self.startIButton =QtGui.QPushButton(self)
        self.stopIButton =QtGui.QPushButton(self)
        self.currentLayout.addWidget(self.startIButton)
        self.currentLayout.addWidget(self.stopIButton)
        fill_layout_textbox(self.currentLayout,["I start :","1","I stop :","5","I step :","1","Start","Stop"])
        
        self.connect(self.startIButton,QtCore.SIGNAL('clicked()'),self.on_startIButton_clicked)
        self.verticalLayout.addLayout(self.currentLayout)
        
        
#        self.voltageLayout = QtGui.QHBoxLayout()
#        
#        self.voltageLayout.setObjectName(_fromUtf8("voltageLayout"))
#        self.voltage_start = QtGui.QLineEdit (self)
#        self.voltage_stop = QtGui.QLineEdit (self)
#        self.voltage_step = QtGui.QLineEdit (self)
#        alabel = QtGui.QLabel(self)
#        self.voltageLayout.addWidget(alabel)
#        self.voltageLayout.addWidget(self.voltage_start)
#        alabel = QtGui.QLabel(self)
#        self.voltageLayout.addWidget(alabel)
#        self.voltageLayout.addWidget(self.voltage_stop)
#        alabel = QtGui.QLabel(self)
#        self.voltageLayout.addWidget(alabel)
#        self.voltageLayout.addWidget(self.voltage_step)
#        self.startVButton =QtGui.QPushButton(self)
#        self.stopVButton =QtGui.QPushButton(self)
#        self.voltageLayout.addWidget(self.startVButton)
#        self.voltageLayout.addWidget(self.stopVButton)
#        fill_layout_textbox(self.voltageLayout,["V start :","","V stop :","","V step :","","Start","Stop"])
#                
#        self.connect(self.startVButton,QtCore.SIGNAL('clicked()'),self.on_startVButton_clicked)
#        self.verticalLayout.addLayout(self.voltageLayout)
#        
        self.setLayout(self.verticalLayout)
#        
#    def on_startVButton_clicked(self):
#        data=np.array([float(self.voltage_start.text()),float(self.voltage_stop.text()),float(self.voltage_step.text())])
#        data={"voltage":data} 
#        self.emit(QtCore.SIGNAL("CommandSent(PyQt_PyObject)"),data)        
        
        
    def on_startIButton_clicked(self):
        data=np.array([float(self.current_start.text()),float(self.current_stop.text()),float(self.current_step.text())])
        data={"current":data}
        try:
            data["num_loop"]=int(self.num_loop.text())
        except:
            pass
        self.emit(QtCore.SIGNAL("CommandSent(PyQt_PyObject)"),data)   

        

        
class ExecutableWidget(QtGui.QWidget):
    
    def __init__(self, parent = None):
#        print "myfilepath ",fname
        super(ExecutableWidget,self).__init__(parent) 
        self.connect(parent,QtCore.SIGNAL("CommandRelayed(PyQt_PyObject)"),self.write_command)
        #main layout of the form is the verticallayout
        self.verticalLayout = QtGui.QVBoxLayout()      
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        """
        here will be displayed the button to create subsets and choose between livefit or postfit, also the number of the subset is displayed
        """
        
        self.titleLayout = QtGui.QHBoxLayout()
        
        self.titleLayout.setObjectName(_fromUtf8("titleLayout"))  
        alabel = QtGui.QLabel(self)
        alabel.setText("Execute:")
        self.verticalLayout.addWidget(alabel)
        
        self.execLayout = QtGui.QHBoxLayout()
        
        self.execLayout.setObjectName(_fromUtf8("execLayout"))

        self.executable = QtGui.QLineEdit (self)
        self.execLayout.addWidget(self.executable)
        
        self.verticalLayout.addLayout(self.execLayout)

        self.setLayout(self.verticalLayout)
        
    def write_command(self,data):
        R=1
        error=0.5
        print "Recieving the data"
        channel=data.keys()[0]
        start=data[channel][0]
        stop=data[channel][1]
        step=data[channel][2]
        input_array=np.arange(start,stop,step)
        data_array=np.array(np.zeros((len(input_array),2)))
        for i,input_var in enumerate(input_array):
            meas_var=(input_var*R)*(1+random()*error)
            self.executable.setText("Input : %.3fA, Output : %.3fV"%(input_var,meas_var))
            data_array[i,0]=input_var
            data_array[i,1]=meas_var
            self.emit(QtCore.SIGNAL("data_array_updated(PyQt_PyObject)"),data_array)
            
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        # run the initializer of the class inherited from6
        super(MainWindow, self).__init__()

        self.data_array=[]        
        
        self.zoneCentrale = QtGui.QMdiArea()
        self.setCentralWidget(self.zoneCentrale)
        sender = QtGui.QDockWidget("Sender", self)
        reciever = QtGui.QDockWidget("Reciever", self)
        
        self.sender=CommandWidget(parent=self)

        self.reciever=ExecutableWidget(parent=self)
        
        sender.setWidget(self.sender)     
        reciever.setWidget(self.reciever)  
        
        self.connect(self.sender,QtCore.SIGNAL("CommandSent(PyQt_PyObject)"),self.relay_command)
        self.connect(self.reciever,QtCore.SIGNAL("data_array_updated(PyQt_PyObject)"),self.update_plot)
        
        self.addDockWidget(Qt.LeftDockWidgetArea, sender)
        self.addDockWidget(Qt.RightDockWidgetArea, reciever)
        
        
        pdw = PlotDisplayWindow.PlotDisplayWindow(data_array = self.data_array,name="Live Data Window",default_channels=2)
        self.connect(self, QtCore.SIGNAL("data_array_updated(PyQt_PyObject)"),pdw.update_plot)
         
        self.zoneCentrale.addSubWindow(pdw)

        pdw.show()
        
#        sender2 = QtGui.QDockWidget("Sender", self)
#        self.sender2=CommandWidget(parent=self)        
#        sender2.setWidget(self.sender2)
#        self.addDockWidget(Qt.LeftDockWidgetArea, sender2)
#        self.connect(self.sender2,QtCore.SIGNAL("CommandSent(PyQt_PyObject)"),self.relay_command)
        
    def relay_command(self,data):
        print "relaying the data :",data
        self.emit(QtCore.SIGNAL("CommandRelayed(PyQt_PyObject)"),data)
    def update_plot(self,data):
         self.emit(QtCore.SIGNAL("data_array_updated(PyQt_PyObject)"),data)
        
def clear_layout(layout):
    """
    This function loop over a layout objects and delete them properly
    """
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        layout.removeWidget(widget)
        try:
            widget.setParent(None)
        except:
            pass
        widget.close()

def fill_layout_textbox(layout,text):
    """
    This function loop over a layout objects set their texts
    """
    for label,i in zip(text,range(layout.count())):
        item = layout.itemAt(i)
        widget = item.widget()
        widget.setText(str(label))
        

if __name__=="__main__":
    
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
#    cmd = CommandWidget()
    ex.show()
#    cmd.show()
    sys.exit(app.exec_())