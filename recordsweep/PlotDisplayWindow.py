# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 13:18:32 2012

Copyright (C) 10th april 2015 Benjamin Schmidt
License: see LICENSE.txt file

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

#from PyQt4.QtSvg import *
import PyQt4.QtGui as QtGui
from PyQt4.QtCore import  SIGNAL, Qt, QRect,QSize


import QtTools

import numpy as np, matplotlib.pyplot as plt


from matplotlib.ticker import MultipleLocator, FormatStrFormatter


from mplZoomWidget import MatplotlibZoomWidget
import ui_plotdisplaywindow
from matplotlib import dates
from matplotlib import ticker
from PlotPreferences import marker_set,line_set,color_blind_friendly_colors
import datetime

from collections import OrderedDict


"""
This describe what element will be displayed on each line of the window option panel.
It does it row by row, chan_contr contain each row element which consist of the label and the type of the objet.
The label can be any string, the type has to be predifined
"""
chan_contr=OrderedDict()
chan_contr["groupBox_Name"]=["Channel","lineEdit"]
chan_contr["groupBox_X"]=["X","radioButton"]
chan_contr["groupBox_Y"]=["Y","checkBox"]
chan_contr["groupBox_YR"]=["Y","checkBox"]
chan_contr["groupBox_invert"]= ["+/-","checkBox"]
chan_contr["groupBox_color"]= ["Col","colorButton"]
chan_contr["groupBox_marker"]= ["M","comboBox"]
chan_contr["groupBox_line"]= ["L","comboBox"]

def get_groupBox_purpouse(name):
    return name.split("_")[1]
    
class PlotDisplayWindow(QtGui.QMainWindow, ui_plotdisplaywindow.Ui_PlotDisplayWindow):
    """
    The argument 'channel_controls' should be an OrderedDict object (from collections import OrderedDict)\n
    Each key will be a unique identifier of the channel control, the item should consist of a list for which the first element is the label of the channel control and the second element, the type of QtQui.\n
    It need to be either 'lineEdit','radioButton','checkBox' or 'comboBox', any other keyword will create an error.\n
    What callback function is associated with each control can be defined in the method 'add_channel_control'
    
    """
    def __init__(self, parent=None, data_array=np.array([]),name="Main Window",default_channels=10,channel_controls=chan_contr):
        # run the initializer of the class inherited from
        super(PlotDisplayWindow, self).__init__()
                    
        #store the choice of channel controls parameters
        self.channel_controls=channel_controls
        
        self.color_set=color_blind_friendly_colors(default_channels)
        # this is where most of the GUI is made
        self.setupUi(self,self.channel_controls)
        self.customizeUi(default_channels)

        #Create an instance of auto-hiding widget which will contain the channel controls
        autoHide =  QtTools.QAutoHideDockWidgets(Qt.RightDockWidgetArea, self) 
        
        # axes and figure initialization - short names for convenience   
        self.fig = self.mplwidget.figure
        self.setWindowTitle(name)
        self.ax = self.mplwidget.axes
        self.axR = self.mplwidget.axesR

        self.ax.xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset = False))
        self.major_locator=self.ax.xaxis.get_major_locator()
        self.ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset = False))
        self.axR.yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset = False))
  
        self.fig.canvas.draw()              
        
        # this is for a feature that doesn't exist yet
        self.history_length = 0

        self.num_channels = 0
        self.left_lines = [] 
        self.right_lines = [] 
        
        #Fills self.lineEdit_Name = [], self.comboBox_Type = [], self.comboBox_Instr = []. self.comboBox_Param = []
        #Whenever connect(obbject,SIGNAL(),function) is used it will call the function whenever the object is manipulated or something emits the same SIGNAL()
        for i in range (default_channels):   
            self.add_channel_controls()
        
        # objects to hold line data. Plot empty lists just to make handles
        # for line objects of the correct color   


        # create data_array attribute and use channel 0 as X by default
        self.data_array = data_array
        self.chan_X = 0
        self.time_Xaxis=False
        self.date_txt=self.fig.text(0.03,0.95,"",fontsize=15)

        
    def customizeUi(self, default_channels):       
       
       
        #this will be a dictionnary with the same keys as self.channel_controls corresponding to list
        #of 'N_channel' control Qwidgets.
        self.channel_objects={}
        for name,item in self.channel_controls.items():
            self.channel_objects[name]=[]
        
        # create a layout within the blank "plot_holder" widget and put the 
        # custom matplotlib zoom widget inside it. This way it expands to fill
        # the space, and we don't need to customize the ui_recordsweep.py file
        self.gridLayout_2 = QtGui.QGridLayout(self.plot_holder)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        self.mplwidget = MatplotlibZoomWidget(self.plot_holder)
        self.mplwidget.setObjectName("mplwidget") 
        self.gridLayout_2.addWidget(self.mplwidget, 0, 0, 1, 1)
  

    
    def add_channel_controls (self):
        """
        create an instance of each of the channel control objects for a new channel, assign the settings and link to the callback function.\n
        It also create an empty line for each axis.
        """
        #index of boxes to create
        i = self.num_channels
        
        self.num_channels = self.num_channels + 1    

        pos_LE = lambda x: 20 * (x + 1)
        
        line1, = self.ax.plot([], [])     
        line2, = self.axR.plot([], [])
        
        for name,item in self.channel_controls.items():
            if item[1]=="radioButton":
                self.channel_objects[name].append(QtGui.QRadioButton(self.groupBoxes[name]))
                self.channel_objects[name][i].setText("")
                self.connect(self.channel_objects[name][i], SIGNAL("toggled(bool)"),self.XRadioButtonHandler)  
            elif item[1]=="checkBox":
                self.channel_objects[name].append(QtGui.QCheckBox(self.groupBoxes[name]))
                self.channel_objects[name][i].setText("")
                self.connect(self.channel_objects[name][i], SIGNAL("stateChanged(int)"), self.YCheckBoxHandler)
            elif item[1]=="comboBox":
                self.channel_objects[name].append(QtGui.QComboBox(self.groupBoxes[name]))
                if get_groupBox_purpouse(name)=="marker":
                    cbb_list=marker_set
                elif get_groupBox_purpouse(name)=="line":
                    cbb_list=line_set
                self.channel_objects[name][i].addItems(cbb_list)
#                self.channel_objects[name][i].setStyleSheet ("QComboBox::drop-down {border-width: 0px;} QComboBox::down-arrow {image: url(noimg); border-width: 0px;}")
                self.channel_objects[name][i].setMaxVisibleItems(len(cbb_list))
                self.connect(self.channel_objects[name][i], SIGNAL("currentIndexChanged(int)"), self.ComboBoxHandler)
            elif item[1]=="lineEdit":
                self.channel_objects[name].append(QtGui.QLineEdit(self.groupBoxes[name]))
                self.channel_objects[name][i].setText(QtGui.QApplication.translate("RecordSweepWindow", "", None, QtGui.QApplication.UnicodeUTF8))
                self.connect(self.channel_objects[name][i], SIGNAL("textEdited(QString)"), self.lineEditHandler)
            elif item[1]=="colorButton":
                self.channel_objects[name].append(QtGui.QPushButton(self.groupBoxes[name]))               
                color=self.color_set[np.mod(i,len(self.color_set))]
                line1.set_color(color)
                line2.set_color(color)
                self.channel_objects[name][i].setStyleSheet('QPushButton {background-color: %s}'%color)
                self.channel_objects[name][i].setFixedSize(15,15)
                self.connect(self.channel_objects[name][i], SIGNAL("clicked()"),self.colorButtonHandler) 
            
            self.channel_objects[name][i].setObjectName(name + "#" + str(i))
            self.channel_objects[name][i].setGeometry(QRect(7, 20*(i+1), 16, 16))
            if item[1]=="lineEdit":
                self.channel_objects[name][i].setGeometry(QRect(10, pos_LE(i), 81, 16))
            elif item[1]=="comboBox" :
                self.channel_objects[name][i].setGeometry(QRect(7, 20*(i+1), 32, 16))
            self.channel_objects[name][i].show()
#        self.radio
        #create line objects and append them to self.ax[R].lines autoatically

        
    """#####################################################################"""
    """These handler function take action when someone interact with the button, checkbox, lineEdit etc... the names are explicit"""
        
    def XRadioButtonHandler(self):
#        print "X clicked"  
        obj=self.sender()         
        name=obj.objectName()
        name=str(name.split("#")[0])
 
        for num, box in enumerate(self.channel_objects[name]):
            if box.isChecked():
                self.chan_X = num
                label=self.channel_objects["groupBox_Name"][num].text()
                self.ax.set_xlabel(label)
                if label=="time(s)":
                    self.time_Xaxis=True

                    hfmt=self.set_axis_time(want_format=True)
                    self.ax.xaxis.set_major_formatter(hfmt)
                    
                    
                    major_ticks=self.ax.xaxis.get_major_ticks()
#                 
                    for i,tick in enumerate(major_ticks):
                        if i==1:
                            n=tick.label.get_text()
                            label_i=n.split(" ")[0]
                        tick.label.set_rotation('vertical')
                    self.date_txt.set_text("Date :"+label_i)
                else:
                    self.time_Xaxis=False
                    self.date_txt.set_text("")
                    self.ax.xaxis.set_major_locator(self.major_locator)
                    self.ax.xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset = False))
                    
                    for tick in self.ax.xaxis.get_major_ticks():
                        tick.label.set_rotation('horizontal')
        self.update_plot() 
        
    def YCheckBoxHandler(self):  
        """Update which data is used for the Y axis (both left and right)"""
        tot_label = ""
#        print "Y clicked"     
        obj=self.sender()         
        name=obj.objectName()
        name=str(name.split("#")[0])

        for num, box in enumerate(self.channel_objects[name]):
            if box.isChecked():
                label = str(self.channel_objects["groupBox_Name"][num].text())
                #unit = self.UNITS[str(self.comboBox_Param[num].currentText())]
                tot_label = tot_label + ", " + label #+ " (" + unit + ")" + ", "
                
        if get_groupBox_purpouse(name)=="Y":
                    self.ax.set_ylabel(tot_label.lstrip(', '))
        elif get_groupBox_purpouse(name)=="YR":
                    self.axR.set_ylabel(tot_label.lstrip(', '))
        
        self.update_plot()             


    def ComboBoxHandler(self,num):
        obj=self.sender()         
        name=obj.objectName()
        
        name,idx=name.split("#")
        name=str(name)
        idx=int(idx)
        
        if get_groupBox_purpouse(name)=="marker":
            self.set_marker(idx,str(obj.currentText()))
        elif get_groupBox_purpouse(name)=="line":
            self.set_linestyle(idx,str(obj.currentText()))
            
            
            
    def colorButtonHandler(self):
        obj=self.sender()         
        name=obj.objectName()
        
        name,idx=name.split("#")
        name=str(name)
        idx=int(idx)

        color = QtGui.QColorDialog.getColor(initial = obj.palette().color(1))
        obj.setStyleSheet('QPushButton {background-color: %s}'%color.name())
#        btn.palette().color(1).name()
        print color.name()
        self.set_color(idx,str(color.name()))
    
    def lineEditHandler(self,mystr):
        obj=self.sender()         
        name=obj.objectName()
        name,idx=name.split("#")
        name=str(name)
        idx=int(idx)
        
        if self.channel_objects["groupBox_X"][idx].isChecked():
            self.ax.set_xlabel(self.channel_objects[name][idx].text())
            self.update_plot()


    def set_axis_ticks(self,ticks):
        if not len(ticks)==3:
            print "some ticks are missing, you should have ticks for X, YL and YR axes"
        else:
            for t in ticks[1]:
                self.channel_objects["groupBox_Y"][t].setCheckState(True)
#                print "Y",str(self.lineEdit_Name[t].text())
            for t in ticks[2]:
                self.channel_objects["groupBox_YR"][t].setCheckState(True)
#                print "YR",str(self.lineEdit_Name[t].text())
                
            self.channel_objects["groupBox_X"][ticks[0]].setChecked(True)
#            print "X",str(self.lineEdit_Name[ticks[0]].text())
            
    
    def get_X_axis_label(self):
        """Update which data is used for the X axis"""
        for num, box in enumerate(self.channel_objects["groupBox_X"]):
            if box.isChecked():
                label=str(self.channel_objects["groupBox_Name"][num].text())
        #getting rid of the eventual units
        if label.find('(')==-1:
            pass
        else:
            label=label[0:label.rfind('(')]
        return label
        
        
    def get_Y_axis_labels(self):  
        """Update which data is used for the Y axis (both left and right)"""
        labels = []
        
        for num, box in enumerate(self.channel_objects["groupBox_Y"]):
            if box.isChecked():
                label=str(self.channel_objects["groupBox_Name"][num].text())
                label=label[0:label.rfind('(')]
                labels.append(label)
        for num, box in enumerate(self.channel_objects["groupBox_YR"]):
            if box.isChecked():
                label=str(self.channel_objects["groupBox_Name"][num].text())
                label=label[0:label.rfind('(')]
                if not label in labels:
                    labels.append(label)
        return labels
    
    def get_X_axis_index(self):
        """Update which data is used for the X axis"""
        index=0
        for num, box in enumerate(self.channel_objects["groupBox_X"]):
            if box.isChecked():
                index=num
        return index
        
        
    def get_Y_axis_index(self):  
        """Update which data is used for the Y axis (both left and right)"""
        index = 0
        for num, box in enumerate(self.channel_objects["groupBox_Y"]):
            if box.isChecked():
                index=num
        return index
    


    def convert_timestamp(self, timestamp):
        dts = map(datetime.datetime.fromtimestamp, timestamp)
        return dates.date2num(dts) # converted        

    def set_axis_time(self,want_format=False):
        """
            convert the time to a certain format
        """

        if want_format:
            time_interval=self.data_array[-1,self.chan_X]-self.data_array[0,self.chan_X]
            if time_interval<500:
                hfmt = dates.DateFormatter('%m/%d %H:%M:%S')
            else:
                hfmt = dates.DateFormatter('%m/%d %H:%M')
            return hfmt
        else:
            time_data = self.convert_timestamp(self.data_array[:,self.chan_X])
            return time_data
        

    def set_marker(self,idx,marker):
        """change the marker style of the plotted line in position idx"""
        if idx < len(self.ax.lines):
            self.ax.lines[idx].set_marker(marker)
            self.axR.lines[idx].set_marker(marker)
        self.mplwidget.rescale_and_draw() 
        
    def set_linestyle(self,idx,linesty):
        """change the style of the plotted line in position idx"""
        if idx < len(self.ax.lines):
            self.ax.lines[idx].set_linestyle(linesty)
            self.axR.lines[idx].set_linestyle(linesty)
        self.mplwidget.rescale_and_draw() 
        

    def set_color(self,idx,color):
        """change the color of the plotted line in position idx"""
        if idx < len(self.ax.lines):
            self.ax.lines[idx].set_color(color)
            self.axR.lines[idx].set_color(color)                
        self.mplwidget.rescale_and_draw()              
        

    def update_markers(self, marker_list):
        """change the marker style of all the lines according to a maker list"""
        for idx, m in enumerate(marker_list):
            if idx < len(self.ax.lines):
                self.ax.lines[idx].set_marker(m)
                self.axR.lines[idx].set_marker(m)                
        self.mplwidget.rescale_and_draw() 

    def update_colors(self, color_list):
        """change the color of all the lines according to a color list"""
        for idx, color in enumerate(color_list):
            if idx < len(self.ax.lines):
                self.ax.lines[idx].set_color(color)
                self.axR.lines[idx].set_color(color)                
        self.mplwidget.rescale_and_draw()                 

    def update_labels(self, label_list):
        """change the label of all the lines according to a label list"""
        for idx, label_text in enumerate(label_list):
            if idx == len(self.channel_objects["groupBox_Name"]):
                self.add_channel_controls()
                
            self.channel_objects["groupBox_Name"][idx].setText(label_text)             

        
    def update_plot(self, data_array = None): 
        """
            take a matrix (data_array) with a number of rows equal to the number of channel/lines in the window and plot them along the line direction
            it only plots if the checkbox of the line is checked
        """
#        print "updateplot data PDW"
        if not data_array == None:
#            print data_array
            self.data_array = data_array

        if self.data_array.size>0 :
            # if the number of columns is more than the number of control boxes
            
            try:
                #if the window was deleted the shape of the very first vector is (num_channel,)
                #and then become (nline,num_channel)
                num_channel=self.data_array.shape[1]
            except:
                num_channel=self.data_array.size
                
            while self.num_channels <  num_channel:
                self.add_channel_controls()

                            
            if self.time_Xaxis:
                xdata=self.set_axis_time()
            else:
                xdata = self.data_array[:,self.chan_X]   

            for chan_Y, [line_L, line_R] in enumerate(zip (self.ax.lines, self.axR.lines)):
                if self.data_array.size>0:
                    if self.channel_objects["groupBox_invert"][chan_Y].isChecked():
                        ydata = -self.data_array[:, chan_Y]
                    else:
                        ydata = self.data_array[:, chan_Y]                        
                    #look which checkbox is checked and plot corresponding data
                    if self.channel_objects["groupBox_Y"][chan_Y].isChecked() and self.data_array.size>0:
                        line_L.set_data(xdata, ydata)
                    else:
                        line_L.set_data([],[])
                    #look which checkbox is checked and plot corresponding data    
                    if self.channel_objects["groupBox_YR"][chan_Y].isChecked() and self.data_array.size>0:
                        line_R.set_data(xdata, ydata)
                    else:
                        line_R.set_data([],[])      
        self.mplwidget.rescale_and_draw() 
                

    def update_fit(self,data_array = None):
        """
            take a matrix (data_array) with a number of lines equal to 2 and a number of rows equal the number of lines in self.data_array
            and plot line 1 as a function of line 2
            right now there is only the possibility to create one fit at the time as we wanted to be able to access the line number and modify the fit or delete it. 
            we can always plot more things on the plot area but we wanted to have some control on the objects
        """
#        print "PDW.update_fit"
        if not data_array == None:
            # if the number of columns is more than the number of control boxes
#            print "chan num", self.num_channels
#            print len(self.ax.lines)
            if self.num_channels == len(self.ax.lines):
                line, = self.ax.plot([],[])
#                print line
                
            if data_array.size > 0:
#                print "updating"
                xdata = data_array[0]    
                ydata = data_array[1]
                self.ax.lines[-1].set_data(xdata, ydata)
#                print len(self.ax.lines)
#                print self.ax.lines[-1]
#                self.ax.lines[-1].set_color('or')
                                     
            #call a method defined in the module mplZoomwidget.py         
            self.mplwidget.rescale_and_draw() 
            
    def remove_fit(self):
        """
            remove the last line on the ax as this position is by default reserved for the fit function. There is probaly a cleverer way to do so...
        """
        self.ax.lines[-1].set_data([], [])

            
    def print_figure(self, file_name = "unknown"):
        """Sends the current plot to a printer"""
        
        printer = QPrinter()
        
        # Get the printer information from a QPrinter dialog box
        dlg = QPrintDialog(printer)        
        if(dlg.exec_()!= QDialog.Accepted):
             return
             
        p = QPainter(printer)
        
        # dpi*3 because otherwise it looks pixelated (not sure why, bug?)
        dpi = printer.resolution()
        
#        # copy the current figure contents to a standard size figure
#        fig2 = plt.figure(figsize=(8,5), dpi = dpi)
#        
#        ax = fig2.add_subplot(1,1,1)
#        for line in self.ax.lines:
#            if line.get_xdata() != []:
#                ax.plot (line.get_xdata(), line.get_ydata(), label= line.get_label())
#        ax.set_xlim(self.ax.get_xlim())
#        ax.set_ylim(self.ax.get_ylim())
#        ax.set_xlabel(self.ax.get_xlabel())
#        ax.set_ylabel(self.ax.get_ylabel())        
#        
#        self.fig.savefig(
#        # support for printing right axes should go here        
#        
#        # Shink current axis by 20%
#        box = ax.get_position()
#        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        
        # Put a legend to the right of the current axis
        #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
        # goal: print the figure with the same aspect ratio as it's shown on the 
        # screen, but fixed width to fill the page nicely
 
        margin_inches = 0.5
        paper_width = 8.5
        
        max_width = paper_width - 2*margin_inches
        max_height = 7
        
        width = self.fig.bbox_inches.width
        height = self.fig.bbox_inches.height
        
        ratio = height/width 
        if ratio > max_height/max_width:
            # scale on width, because otherwise won't fit on page.
            dpi_scale = max_height/height
            height = max_height
            width = ratio/height
        else:
            dpi_scale = max_width/width
            width = max_width
            height = ratio * width
            
        self.fig.savefig("temp.png", dpi=dpi * dpi_scale * 10) 

        
        # half inch margins
        margin_top = 0.5*dpi
        margin_left = 0.5*dpi       
        
        # matplotlib's svg rendering has a bug if the data extends beyond the
        # plot limits. Below is what would be used for temp.svg
        #svg = QtSvg.QSvgRenderer("temp.svg")
        #svg.render(p, QRectF(margin_top,margin_left, 8*dpi, 5*dpi))

        p.drawImage(QRectF(margin_top,margin_left, width*dpi, height*dpi), 
                    QImage("temp.png", format='png'))
        p.drawText(margin_left, 600, "Data recorded to: " + file_name)    
        p.end() 
        
    def is_plot_display_window(self):
        """used to differentiate PlotDisplayWindow from LoadPlotWindow"""
        return True
        
def convert_timestamp(timestamp):
    dts = map(datetime.datetime.fromtimestamp, timestamp)
    return dates.date2num(dts) # converted    
        
# This snippet makes it run as a standalone program
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    form = PlotDisplayWindow(default_channels=6)
#    data=np.array([np.arange(10) for a in range(10)])
    data=np.loadtxt("sample_name_TEST_1130_001.dat")
    
    form.update_plot(data)
    form.show()
    app.exec_()
    
#    data=np.loadtxt("sample_name_TEST_1128_008.dat")
#    time_interval=data[-1,0]-data[0,0]
#    print time_interval
#    time_data = convert_timestamp(data[:,0])
##        xlim = convert_timestamp(self.ax.get_xlim())
##        print xlim
##    print time_data
#        # matplotlib date format object
#    hfmt = dates.DateFormatter('%m/%d %H:%M:%S')        
#      
#    fig=plt.figure()
#    ax=fig.add_subplot(111)
#    ax.plot(time_data,data[:,1])
#    plt.xticks(rotation='vertical')
##    plt.xticks()
##    plt.subplots_adjust(bottom=.3)
#        #plt.show()
###        for li in self.ax.lines:
####            if li.get_xdata().size >0:
####                print li.get_data()
###            li.set_xdata(time_data)
##                
##    ax.xaxis.set_major_locator()
#    ax.xaxis.set_major_formatter(hfmt)
#    
##    print ax.xaxis.get_xticklabels()
#    
#    for i in ax.xaxis.get_major_ticks():
#        print i.label.get_text()
##       
###        print "ready to draw"
###        self.mplwidget.rescale_and_draw()              
#    
#
#
#    plt.show()
