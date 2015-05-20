# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 21:52:15 2013

@author: Ben
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#import SRS830, IPS120, LS370, HP4263B, HP34401A, LS340, PARO1000, CG500, HLT560
import readconfigfile
import time
#from datetime import datetime, timedelta 
import numpy as np
#import Tool

class DataTakerThread(QThread):
    MEAS_TIME = 1.5      
    USING_MAGNET = True 
    MAX_CHANNELS = 10
    
    def __init__(self, lock, parent=None):
        super(DataTakerThread, self).__init__(parent)
        self.lock = lock
        self.stopped = True
        self.mutex = QMutex()
        self.completed = False
        self.DEBUG = readconfigfile.get_debug_setting()
        self.exited_main_running = False  
        self.output_file_name = ''
        self.script_file_name = ''
        self.t_start = None
        
        # tuple: lockin #, channel, subplot for display
        self.data_channels = []        
        self.instruments = {}
        self.instrument_types = {}      

        
    def initialize(self, name_list, type_list, dev_list, param_list):     
        self.stopped = True
        self.completed = False    
        
        if not self.t_start:
            self.t_start = time.time()
#            self.today=datetime.now()
            
        #open file, write header
        self.out_file = open(self.output_file_name, 'a')
        self.log_file = open(self.output_file_name.rstrip('.dat') + ".log", 'a')
        
        self.log_file.write('Starting time: ' + str(self.t_start) + ' = ' + time.ctime() +'\n\n')

        # print list of names to the terminal and to the file as headers
        stri = str(name_list).strip('[]')           
#        print stri
        #print self.out_file.name
        self.out_file.write(stri + '\n')  
   

        w = 15
        self.log_file.write("Instrument Configuration:\n\n")
        self.log_file.write("%s %s %s %s\n\n"%("Name".center(w), 
                                               "Type".center(w), "Device".center(w), "Param".center(w)))

        # tuple: lockin #, channel, subplot for display
#        self.data_channels = [];
        #port->instrument object;ID->port;list of instrument objects;list of parameters
        self.instruments = {};self.instrument_types = {};self.active_instruments=[];self.active_parameters=[]
                                         
        for name, instr_type, dev, param in zip(name_list, type_list, dev_list, param_list):
            self.log_file.write("%s %s %s %s\n\n"%(name.center(w), 
                                                   instr_type.center(w), dev.center(w), param.center(w)))
            #print name,instr_type,dev,param
            # if the text box wasn't blank...
            if name:
                # add instrument to list if not there. 'dev' is the GPIB address
                # and since it's unique to the instrument, we use it as the key
                # in the dictionaries self.instruments and self.instrument_types
                if not dev in self.instruments:
                    
                    if instr_type !='TIME' and instr_type!='':
                        self.instruments[dev]=self.connect_instrument(instr_type,dev,self.DEBUG)                 
                    
                    # instrument on device port "dev" is of type "instr_type"    
                    self.instrument_types[dev] = instr_type

                else:
                    # Another data channel already used this instrument - make
                    # sure it's the same type!!!
                    if instr_type != self.instrument_types[dev]:
                        print ("Same GPIB port specified for different instruments! ")
                        print (dev + " " + instr_type + " " + self.instrument_types[dev])
                        instr_type = 'NONE'  
                        
                if instr_type !='TIME' and instr_type!='' and instr_type!= 'NONE':
                    self.active_instruments.append(self.get_instrument(instr_type))
                    self.active_parameters.append(param)
                elif instr_type =='TIME':
                    self.active_instruments.append('TIME')
                    self.active_parameters.append(param)
                else:
                    self.active_instruments.append(None)
                    self.active_parameters.append(None)
                    
                   
#        print "init done"
#        print self.instruments
#        print self.instrument_types
#        print self.active_instruments
#        print self.active_parameters
        
    def run(self):
        self.stopped = False

        # open another file which contains the script to follow for this
        # particular measurement
        script = open(self.script_file_name)
        print "open script "+self.script_file_name
        exec (script)
        script.close()   
        
        self.out_file.close()    
        self.log_file.close() 
        self.emit(SIGNAL("script_finished(bool)"), self.completed)        
        self.stopped = True        
    
    def stop(self):
        
        try:
            self.mutex.lock()
            self.stopped = True
        finally:
            self.mutex.unlock()

    def isStopped(self):
        try:
            self.mutex.lock()
            return self.stopped
        finally:
            self.mutex.unlock()    

            
    def read_data(self):
        #iterate through list of commands to get data from instruments               
        param_set=[]        
        data_set=[]

#        t_meas= self.today + timedelta(seconds=(time.time() - self.t_start))
        t_meas=time.time() - self.t_start
        for param,inst in zip(self.active_parameters,self.active_instruments):
            if inst !='TIME' and inst!='' and inst!= None:
                data_set.append(inst.measure(param))
                param_set.append(inst.channels_names[param])
            elif inst =='TIME':
                data_set.append(round(t_meas,2))
                param_set.append('TIME')
            else:
                data_set.append(0)
                param_set.append('')
        #send data back to the mother ship as an array of floats, but only
        # if the thread is still supposed to be running
        if not self.isStopped():
            # a quick way to make a comma separated list of the values
            stri = str(data_set).strip('[]\n\r') 
            #numpy arrays include newlines in their strings, get rid of them.
            stri = stri.replace('\n', '') 
            stri = stri.replace(',', ' ')
            
            # print exactly the string which is going to be written in the file
            print '>>' + stri
            self.out_file.write(stri + '\n')                    
            
            self.emit(SIGNAL("data(PyQt_PyObject)"), np.array(data_set))         

    def get_instrument(self,instr_ID,isport=False):
        instr=''
        if isport:
           instr=self.instruments[instr_ID]
        else:
            for port,id_name in self.instrument_types.items():
                if id_name==instr_ID:
                    instr=self.instruments[port]
        return instr
        
    def connect_instrument(self,inst_name,device_port,debug=False):
#        [INSTRUMENT_TYPES,AVAILABLE_PARAMS,UNITS]=get_instr_list()
#        print INSTRUMENT_TYPES
#        instruments=[]
#        for inst_name in INSTRUMENT_TYPES:
        class_inst=__import__(inst_name)
            #port should contain the name of the GPIB
        obj=class_inst.Instrument(device_port,debug)
            #print obj.identify("REHello, this is ")
#            instruments.append(obj)
        return obj #instruments
        
    def clean_up(self):
        for inst in self.instruments:
            inst.close()      
            