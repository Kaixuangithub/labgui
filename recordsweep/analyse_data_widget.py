# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 11:11:45 2013

@author: pf
"""
#import matplotlib.pyplot as plt
import PyQt4.QtCore as QtCore
from PyQt4.QtCore import Qt
import PyQt4.QtGui as QtGui
#from PyQt4.QtGui import *
import sys
import analyse_data as ad
import numpy as np
import IOTool as io

try:
    _fromUtf8 = QtGui.QString.fromUtf8
except:
    _fromUtf8 = lambda s: s

#fileName="C:/Users/pfduc/Dropbox/McGill/Ploting/Integration Gas Flow/140616_B24_E5_296_last_test.txt"
#fileName=None
class AnalyseDataWidget(QtGui.QWidget):
    
    def __init__(self, parent = None,fname=None):
#        print "myfilepath ",fname
        super(AnalyseDataWidget,self).__init__(parent) 
        if parent:
            self.connect(parent,QtCore.SIGNAL("selections_limits(PyQt_PyObject,int,int,int)"),self.update_selection_limits)
            self.connect(parent,QtCore.SIGNAL("data_array_updated(PyQt_PyObject)"),self.update_experiment)
        
        self.fit_func=None
        self.fit_funcs_names=io.list_module_func("Fitting")
       
        self.fname=str(fname)
        
        #contains the x axis index, y axis index, the axis limits, the mode (pan,zoom,selection)
        self.fit_selection_parameters=[0,1,[],1]
        
#        self.experiment=ad.live_experiment() 
        self.experiment=ad.experiment()       
        self.index_fit=None
        self.has_fit=False
        if not self.fname:
            print "AnalyseDataWidget :",fname
            self.load_experiment(self.fname)
        
        #main layout of the form is the verticallayout
        self.verticalLayout = QtGui.QVBoxLayout()      
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        """
        here will be displayed the button to create subsets and choose between livefit or postfit, also the number of the subset is displayed
        """
        self.commandLayout = QtGui.QHBoxLayout()
        
        self.commandLayout.setObjectName(_fromUtf8("commandLayout"))
        self.addSubsetButton = QtGui.QPushButton(self)
        self.addSubsetButton.setText("Create subset")
        self.removeSubsetButton = QtGui.QPushButton(self)
        self.removeSubsetButton.setText("Remove subset")
        self.fitCombo= QtGui.QComboBox(self)
        self.fitCombo.setObjectName(_fromUtf8("fit_comboBox"))
        self.fitCombo.addItems(self.fit_funcs_names)
        self.fit_func=io.import_module_func("Fitting",str(self.fitCombo.currentText()))
        self.liveFitCheckBox=QtGui.QCheckBox(self)
        self.liveFitCheckBox.setObjectName(_fromUtf8("livefit_checkBox"))
        self.liveFitCheckBox.setText("LiveFit")
        self.indexValue = QtGui.QLineEdit (self)
        self.commandLayout.addWidget(self.indexValue)
        self.commandLayout.addWidget(self.addSubsetButton)
        self.commandLayout.addWidget(self.removeSubsetButton)
        self.commandLayout.addWidget(self.fitCombo)
        
        
        
        
        self.commandLayout.addWidget(self.liveFitCheckBox)
        
        self.verticalLayout.addLayout(self.commandLayout)


        """
        here will be displayed the buttons to save the fitted subsets and to move through subsets
        """
        self.navigationLayout = QtGui.QHBoxLayout()

        self.navigationLayout.setObjectName(_fromUtf8("navigationLayout"))
        self.previousButton = QtGui.QPushButton(self)
        self.previousButton.setText("<==")
        self.nextButton = QtGui.QPushButton(self)
        self.nextButton.setText("==>")
        self.navigationLayout.addWidget(self.previousButton)
        self.navigationLayout.addWidget(self.nextButton)
        
        self.verticalLayout.addLayout(self.navigationLayout)
        
        
        """
        here will be displayed the x-axis boundaries over which the plot is made
        """
        self.selectionLayout = QtGui.QHBoxLayout()
        
        alabel = QtGui.QLabel(self)
        self.XminIndex = QtGui.QLineEdit (self)
        self.XmaxIndex = QtGui.QLineEdit (self)
        self.Xmin = QtGui.QLineEdit (self)
        self.Xmax = QtGui.QLineEdit (self)
        alabel = QtGui.QLabel(self)
        self.selectionLayout.addWidget(alabel)
        self.selectionLayout.addWidget(self.XminIndex)
        alabel = QtGui.QLabel(self)
        self.selectionLayout.addWidget(alabel)
        self.selectionLayout.addWidget(self.XmaxIndex)
        alabel = QtGui.QLabel(self)
        self.selectionLayout.addWidget(alabel)
        self.selectionLayout.addWidget(self.Xmin)
        alabel = QtGui.QLabel(self)
        self.selectionLayout.addWidget(alabel)
        self.selectionLayout.addWidget(self.Xmax)
        fill_layout_textbox(self.selectionLayout,["Imin :","","Imax :","","Xmin :","","Xmax :",""])
        
        self.verticalLayout.addLayout(self.selectionLayout)
        
        self.create_phys_layout()
        self.create_fit_layout()
        
        self.saveLayout = QtGui.QHBoxLayout()

        self.saveLayout.setObjectName(_fromUtf8("saveLayout"))
        self.saveButton = QtGui.QPushButton(self)
        self.saveButton.setText("Save Data")
        self.save_setButton = QtGui.QPushButton(self)
        self.save_setButton.setText("Save Set")
        self.navigationLayout.addWidget(self.saveButton)
        self.navigationLayout.addWidget(self.save_setButton)
        self.verticalLayout.addLayout(self.saveLayout)
        
        self.setLayout(self.verticalLayout)
        
        self.connect(self.removeSubsetButton,QtCore.SIGNAL('clicked()'),self.on_removesubsetButton_clicked)
        self.connect(self.addSubsetButton,QtCore.SIGNAL('clicked()'),self.on_addsubsetButton_clicked)
        self.connect(self.fitCombo, QtCore.SIGNAL("currentIndexChanged(int)"), self.fit_func_changed)
        self.connect(self.liveFitCheckBox, QtCore.SIGNAL("stateChanged(int)"), self.livefit_check_box_handler) 
        self.connect(self.previousButton,QtCore.SIGNAL('clicked()'),self.on_previousButton_clicked)
        self.connect(self.nextButton,QtCore.SIGNAL('clicked()'),self.on_nextButton_clicked)
        self.connect(self.saveButton,QtCore.SIGNAL('clicked()'),self.on_saveButton_clicked)
        self.connect(self.save_setButton,QtCore.SIGNAL('clicked()'),self.on_save_setButton_clicked)
      
    
#        self.emit(QtCore.SIGNAL("add_line(PyQt_PyObject)"), np.array([[],[]]))
#        self.connect(self.dataAnalyseWidget, QtCore.SIGNAL("rem_last_line(int)"), plw.rem_last_line)    
    
    def load_experiment(self,fname=None):
        print "analyse_data_widget.load_experiment :",self.liveFitCheckBox.isChecked()
        if self.liveFitCheckBox.isChecked():
            print "analyse_data_widget.load_experiment : Cannot allow you to load a previous experiment while the LiveFit Checkbox is checked"
        else:
            if not fname==None:
                fname=str(fname)
                self.experiment=ad.experiment(fname)
                #this gets rid of the extension of the filename and of the path
                self.fname=fname.split('/')
                self.fname=str(self.fname[len(self.fname)-1]).split('.')[0]
            else:
                print "analyse_data_widget.load_experiment:there is no file to load an experiment"
        self.refresh_active_set()
        
    def fit_func_changed(self):
        self.fit_func=io.import_module_func("Fitting",str(self.fitCombo.currentText()))
#        print io.get_func_variables(self.fit_func)
        self.remove_fit_layout()
        self.remove_phys_layout()
        self.create_phys_layout()
        self.create_fit_layout()
        
    def on_fitButton_clicked(self,paramX='Time',paramY='FLOW',x_bounds=None):
        print "analyse_data_widget.AnalyseDataWidget.on_fitButton_clicked\n"
        self.experiment.fit(paramX,paramY,self.fit_func,x_bounds)
        
#        if not self.has_fit:
#            self.emit(QtCore.SIGNAL("add_line(PyQt_PyObject)"), np.array([[],[]]))
#            self.has_fit=True

        self.refresh_active_set()
    
    def on_removesubsetButton_clicked(self):
        self.experiment.remove_subset()
        self.on_previousButton_clicked        
        self.refresh_active_set()
        
    def on_addsubsetButton_clicked(self):
       self.create_subset()
       
    def create_subset(self):
        print "analysa_data_widget.create_subset : ",self.fit_selection_parameters
        xlims=self.fit_selection_parameters[2]
        paramX=self.fit_selection_parameters[0]
        paramY=self.fit_selection_parameters[1]
        if not xlims==None:
            print "analysa_data_widget.create_subset : axisLims : ",xlims
            print "analysa_data_widget.create_subset : paramX : ",paramX        
            start=xlims[0]
            end=xlims[1]
    
            self.experiment.create_subset(start,end,paramX)
            self.on_fitButton_clicked(paramX,paramY)
            self.refresh_active_set()
        else:
            print "analysa_data_widget.create_subset : xlims was none\n"
        
    def on_previousButton_clicked(self):
        self.experiment.previous_data_set()
        self.refresh_active_set()
        
    def on_nextButton_clicked(self):
        self.experiment.next_data_set()
        self.refresh_active_set()
        
    def livefit_check_box_handler(self,index):
        isChecked=self.liveFitCheckBox.isChecked()
        state=not isChecked
        self.previousButton.setEnabled(state)
        self.nextButton.setEnabled(state)
        self.addSubsetButton.setEnabled(state)
        self.removeSubsetButton.setEnabled(state)
        self.saveButton.setEnabled(state)
        self.save_setButton.setEnabled(state)
        
        if isChecked:
            self.indexValue.setText("LIVE Fit")
            print "ADW.livefit_check_box_handler : LIVE"
            self.experiment=ad.live_experiment()
        else:
            self.indexValue.setText("Raw Data")
            if not self.fname==None:
                print "ADW.livefit_check_box_handler : loading : ",self.fname
                try:
                    self.load_experiment(self.fname)
                except:
                    print "analyse_data_widget : livefit_check_box_handler : the filename to load the experiment isn't specified"
#        print "ADW.livefit_check_box_handler ",self.liveFitCheckBox.isChecked()
        return self.liveFitCheckBox.isChecked()
    
    def on_saveButton_clicked(self):
        if not self.fname:
            fname = str(QtGui.QFileDialog.getSaveFileName(self, 'Save output file as', 
                                                './'+self.fname+'.adat'))
        else:
            fname=self.fname +'.adat'
                                    
#        fname = str(QFileDialog.getOpenFileName(self, 'Load load from', './'))
        print fname
        if fname:
            of=open(fname, 'a')
            self.experiment.savefile(of)
            of.close()
    
    def on_save_setButton_clicked(self):
        if not self.fname:
            fname = str(QtGui.QFileDialog.getSaveFileName(self, 'Save output file as', 
                                                './'+self.fname+'.aset'))
        else:
            fname=self.fname +'.aset'
                                    
#        fname = str(QFileDialog.getOpenFileName(self, 'Load load from', './'))
        print fname
        if fname:
            of=open(fname, 'a')
            self.experiment.saveset(of)
            of.close()
        
    """
    might be buggy
    """
    def update_experiment(self,data):
#        print "ADW.update_experiment : data"
        if self.liveFitCheckBox.isChecked():
            self.experiment.update_data_set(data,self.fit_func,self.fit_selection_parameters)
            self.refresh_active_set()
        else:
            pass
#            print "ADW.update_experiment : Experiment not updated"
#        if not self.fit_selection_parameters==None:
#            self.on_fitButton_clicked(self.fit_selection_parameters[0],self.fit_selection_parameters[1],self.fit_selection_parameters[2])
    
    def update_selection_limits(self,limits,paramX,paramY,mode):
#        print "analyse_data_widget.update_selection_limits\n"
        fill_layout_textbox(self.selectionLayout,["Imin :","%i"%(limits[0]),"Imax :","%i"%(limits[1]),"Xmin :","%.2f"%(limits[2]),"Xmax :","%.2f"%(limits[3])])
        self.fit_selection_parameters=[paramX,paramY,limits,mode]
    
    def refresh_active_set(self,exptype='flow'):

        physp=self.experiment.get_active_physparams()
        fitp=self.experiment.get_active_fit_params()
        limp=self.experiment.get_active_lim_params()
        
#        print "ftip in refresh_active_set: ",fitp,"\n"

        if not physp==None:
            fill_layout_textbox(self.phys_paramLayout,physp)

        if not fitp==None:
            fill_layout_textbox(self.fit_paramLayout,fitp)
        if not limp==[]:
            Imin="%i"%(limp[0][0])
            Imax="%i"%(limp[0][1])
            Xmin="%.2f"%(limp[1])
            Xmax="%.2f"%(limp[2])
            fill_layout_textbox(self.selectionLayout,["Imin :",Imin,"Imax :",Imax,"Xmin :",Xmin,"Xmax :",Xmax])
        else:
            try:
                Imin="%i"%(self.fit_selection_parameters[2][0])
            except:
                Imin=""
            try:
                Imax="%i"%(self.fit_selection_parameters[2][1])
            except:
                Imax=""
            try:
                Xmin="%.2f"%(self.fit_selection_parameters[2][2])
            except:
                Xmin=""
            try:
                Xmax="%.2f"%(self.fit_selection_parameters[2][3])
            except:
                Xmax=""
            fill_layout_textbox(self.selectionLayout,["Imin :",Imin,"Imax :",Imax,"Xmin :",Xmin,"Xmax :",Xmax])
            
        index=self.experiment.active_set+1
        if index: 
            self.indexValue.setText(str(index))
        else:
            self.indexValue.setText("Raw Data")
        
#        mydata=np.array(self.experiment.get_subset_data())        
        
        if self.fit_selection_parameters[3]==2:
            mydata=np.array(self.experiment.get_subset_data())
        else:
            mydata=np.array(self.experiment.get_data())
#        print "ADW.refresh_active_set : active subset ",self.experiment.get_active_subset()
#        print mydata
#        print "analyse_data_widget.refresh_active_set: data ",self.experiment.get_subset_data()

#        here the parameters of the fit should change accordingly to the number of parameter there is in a function and their name
#
##the plot should not erase some data arbitrarily...
        myX=[]
        myY=[]
        if self.fit_func.func_name=="linear":
            
            if not fitp==[]:
#                print "analyse_data_widget.fit.linear : ",fitp
                myX=mydata[:,0]
#                print myX
                myY=self.fit_func(myX,fitp[0],fitp[1])
#                print myY
        if self.fit_func.func_name=="exp_decay":
            
            if not fitp==[]:
#                print "analyse_data_widget.fit.exp_decay : ",fitp
                myX=mydata[:,0]
#                print myX
                myY=fitp[2]+self.fit_func(myX-fitp[3],fitp[0],fitp[1])
#                print myY
            
#            mydata[:,1]=np.ones(len((mydata[:,1])))*physp['Q']
#            mydata[:,7]=fitp[2]+self.fit_func(mydata[:,0]-fitp[3],float(self.aValue.text()),float(self.bValue.text()))
#        else:
#            pass
##            [start,end]=self.experiment.data_set_bounds
#            try:
#                mydata[:,1]=np.ones(len((mydata[:,1])))*float(self.qValue.text())
#                mydata[:,7]=float(self.cValue.text())+self.fit_func(mydata[:,0]-float(self.dValue.text()),float(self.aValue.text()),float(self.bValue.text()))
#            except:
#                pass
##            print "analyse_data_widget.refresh_active_set:the indexes of the data subset ",self.experiment.get_active_subset()
##            print self.experiment
##        print np.size(np.array(self.experiment.get_subset_data()),0)
##        print np.size(np.array(self.experiment.get_subset_data()),1)
        self.emit(QtCore.SIGNAL("data_set_updated(PyQt_PyObject)"),np.array(mydata))
        self.emit(QtCore.SIGNAL("update_fit(PyQt_PyObject)"),np.array([myX,myY])) 

##        self.experiment.display()
                
    def create_phys_layout(self,physparam_list=None):
        """
           The parameters that will be displayed depend on the function to fit, one has to describe the list here.
           This function creates a layout for the physically relevant parameter extracted from fit
        """  
        if physparam_list==None:
            func_name=self.fit_func.func_name
            if func_name=="exp_decay":
                physparam_list=["Flow(mbarl/s)","P(psi)","T(K)"]
            elif func_name=="exp_decay_down":
                physparam_list=["Flow(mbarl/s)","P(psi)","T(K)"]
            elif func_name=="integrate":
                physparam_list=["Flow(mbarl/s)","PV(mbarl)","Time(s)"]
            elif func_name=="linear":
                physparam_list=["Slope"]
            else:
                physparam_list=[]
        self.physLayout = QtGui.QVBoxLayout()
        self.physLayout.setObjectName(_fromUtf8("physLayout"))        
        
        self.phys_paramLayout = QtGui.QHBoxLayout()        
        self.phys_param_labelLayout = QtGui.QHBoxLayout()
        
        for physparam in physparam_list:
            aLabel = QtGui.QLabel (self)
            aLabel.setText(physparam)
            self.aValue = QtGui.QLineEdit (self)
            self.phys_param_labelLayout.addWidget(aLabel,alignment=Qt.AlignCenter)
            self.phys_paramLayout.addWidget(self.aValue)  

        self.physLayout.addLayout(self.phys_param_labelLayout)
        self.physLayout.addLayout(self.phys_paramLayout)
        
        self.verticalLayout.addLayout(self.physLayout)
        self.setLayout(self.verticalLayout)    
    
    def remove_phys_layout(self):
        clear_layout(self.phys_paramLayout)       
        clear_layout(self.phys_param_labelLayout)
        
    def create_fit_layout(self,fparam_list=None):
        """
           The parameters that will be displayed depend on the function to fit, they are automatically extracted from the functions described in the module Fitting
        """  
        if fparam_list==None:
            fparam_list=io.get_func_variables(self.fit_func)
            #the first variable is the x axis coordinate, is it not a fit parameter
            fparam_list=fparam_list[1:]
        
        self.fitLayout = QtGui.QVBoxLayout()
        self.fitLayout.setObjectName(_fromUtf8("fitLayout"))
        self.fit_param_labelLayout = QtGui.QHBoxLayout()
        self.fit_paramLayout = QtGui.QHBoxLayout() 
        
        for fparam in fparam_list:
            aLabel = QtGui.QLabel (self)
            aLabel.setText(fparam)
            self.aValue = QtGui.QLineEdit (self)
            self.fit_param_labelLayout.addWidget(aLabel,alignment=Qt.AlignCenter)
            self.fit_paramLayout.addWidget(self.aValue)  
#           
        self.fitLayout.addLayout(self.fit_param_labelLayout)
        self.fitLayout.addLayout(self.fit_paramLayout)
        
        self.verticalLayout.addLayout(self.fitLayout)
        self.setLayout(self.verticalLayout)

    
    def remove_fit_layout(self):
        clear_layout(self.fit_paramLayout)       
        clear_layout(self.fit_param_labelLayout)

    def load_file_name(self):
        return self.loadFileLineEdit.text()

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
    ex = AnalyseDataWidget()
    ex.show()
    sys.exit(app.exec_())