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
        self.experiment=ad.live_experiment()      
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
        self.fitCombo= QtGui.QComboBox(self)
        self.fitCombo.setObjectName(_fromUtf8("fit_comboBox"))
        self.fitCombo.addItems(self.fit_funcs_names)
        self.fitCombo.setCurrentIndex(4)
        self.fit_func=io.import_module_func("Fitting",str(self.fitCombo.currentText()))
        self.liveFitCheckBox=QtGui.QCheckBox(self)
        self.liveFitCheckBox.setObjectName(_fromUtf8("livefit_checkBox"))
        self.liveFitCheckBox.setText("Fit On")
        self.commandLayout.addWidget(self.fitCombo)
        
        
        
        
        self.commandLayout.addWidget(self.liveFitCheckBox)
        
        self.verticalLayout.addLayout(self.commandLayout)


        
        
        """
        here will be displayed the x-axis boundaries over which the plot is made
        """
        self.selectionLayout = QtGui.QHBoxLayout()
        
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
        
        self.create_fit_layout()
        
        self.setLayout(self.verticalLayout)
        
        self.connect(self.fitCombo, QtCore.SIGNAL("currentIndexChanged(int)"), self.fit_func_changed)
        self.connect(self.liveFitCheckBox, QtCore.SIGNAL("stateChanged(int)"), self.livefit_check_box_handler) 
      
        

        
    def fit_func_changed(self):
        self.fit_func=io.import_module_func("Fitting",str(self.fitCombo.currentText()))
#        print io.get_func_variables(self.fit_func)
        self.remove_fit_layout()
#        self.remove_phys_layout()
#        self.create_phys_layout()
        self.create_fit_layout()
        

    def fit_status(self):
        return self.liveFitCheckBox.isChecked()
        
    def livefit_check_box_handler(self,index):
        isChecked=self.liveFitCheckBox.isChecked()

        
        if isChecked:
            pass
#            print "ADW.livefit_check_box_handler : Fit on"
            
        else:
            self.fit_func_changed()
#            print "ADW.livefit_check_box_handler : Fit off"
        self.refresh_active_set()
        return self.liveFitCheckBox.isChecked()
    

    """
    might be buggy
    """
    def update_experiment(self,data):
#        print "ADW.update_experiment : data"
#        if self.fit_status():
        try:
            self.experiment.update_data_set(data,self.fit_func,self.fit_selection_parameters)
        except:
            "demo_fit_widget.update_experiment : buggy feature"
        self.refresh_active_set()
    
    def update_selection_limits(self,limits,paramX,paramY,mode):
#        print "analyse_data_widget.update_selection_limits\n"
        fill_layout_textbox(self.selectionLayout,["Imin :","%i"%(limits[0]),"Imax :","%i"%(limits[1]),"Xmin :","%.2f"%(limits[2]),"Xmax :","%.2f"%(limits[3])])
        self.fit_selection_parameters=[paramX,paramY,limits,mode]
    
    def refresh_active_set(self,exptype='flow'):

        fitp=self.experiment.get_active_fit_params()
        limp=self.experiment.get_active_lim_params()
        
        if self.fit_status():
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
            
        
        if self.fit_selection_parameters[3]==2:
            mydata=np.array(self.experiment.get_subset_data())
        else:
            mydata=np.array(self.experiment.get_data())
            
            
        myX=[]
        myY=[]
        if self.fit_status():
#            print "the status is on"

            if self.fit_func.func_name=="linear":
                
                if not fitp==[]:
    #                print "analyse_data_widget.fit.linear : ",fitp
                    try:
                        myX=mydata[:,0]
        #                print myX
                        myY=self.fit_func(myX,fitp[0],fitp[1])
                    except:
                        pass
    #                print myY
            if self.fit_func.func_name=="exp_decay":
                
                if not fitp==[]:
    #                print "analyse_data_widget.fit.exp_decay : ",fitp
                    try:
                        myX=mydata[:,0]
                        myY=fitp[2]+self.fit_func(myX-fitp[3],fitp[0],fitp[1])
                    except:
                        pass
            else:
                if not fitp==[]:
#                    print "myY=self.fit_func(myX,"+io.enumerate_arg_func("fitp",fitp[:-1])+")"
                    try:
                        myX=mydata[:,0]
            #                print myX
#                        print "myY=self.fit_func(myX,"+io.enumerate_arg_func("fitp",fitp[:-1])+")"
                        exec("myY=self.fit_func(myX,"+io.enumerate_arg_func("fitp",fitp[:-1])+")")
                    except:
                        pass    
#                    print self.fit_func(myX,fitp[0],fitp[1])
#            print "oeriereiui",myX,myY
            
            self.emit(QtCore.SIGNAL("data_set_updated(PyQt_PyObject)"),np.array(mydata))
        self.emit(QtCore.SIGNAL("update_fit(PyQt_PyObject)"),np.array([myX,myY])) 

        
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