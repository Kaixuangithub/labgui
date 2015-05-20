# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 21:52:15 2013

@author: Ben
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import SRS830, IPS120, LS370, HP4263B, MKS, HP34401A
import readconfigfile
import time
import numpy as np

class DataTakerThread(QThread):
    MEAS_TIME = 1      
    USING_MAGNET = True 
    
    def __init__(self, lock, parent=None):
        super(DataTakerThread, self).__init__(parent)
        self.lock = lock
        self.stopped = True
        self.mutex = QMutex()
        self.completed = False
        self.DEBUG = readconfigfile.get_debug_setting()

    def initialize(self, name_list, type_list, dev_list, param_list):     
        self.stopped = True
        self.completed = False     
        self.t_start = time.time()
   
        # tuple: lockin #, channel, subplot for display
        self.data_channels = []        
        self.instruments = {}
        self.instrument_types = {}

        for name, instr_type, dev, param in zip(name_list, type_list, dev_list, param_list):
            if name:
                # add instrument to list if not there
                if not dev in self.instruments:
                    if instr_type == 'SRS830':               
                        self.instruments[dev] = SRS830.SRS830(dev, debug=self.DEBUG)
                    elif instr_type == 'HP34401A':               
                        self.instruments[dev] = HP34401A.HP34401A(dev, debug=self.DEBUG)                        
                    elif instr_type == 'IPS120':
                        self.instruments[dev] = IPS120.IPS120(dev, debug=self.DEBUG)  
                        self.instruments[dev].ips.clear()
                    self.instrument_types[dev] = instr_type
                else:
                    if instr_type != self.instrument_types[dev]:
                        print ("Same GPIB port specified for different instruments! ")
                        print (dev + " " + instr_type + " " + self.instrument_types[dev])
                        instr_type = 'NONE'                        
    
                if instr_type == 'TIME':
                    command = lambda: time.time() - self.t_start
                elif instr_type == 'IPS120':
                    if param == 'FIELD':
                        command = lambda d=dev: self.instruments[d].read_field()
                elif instr_type == 'SRS830':
                    if param =='X':
                        command = lambda d=dev: self.instruments[d].read_input(1)
                    elif param =='Y':
                        command = lambda d=dev: self.instruments[d].read_input(2)
                    elif param =='R':
                        command = lambda d=dev: self.instruments[d].read_input(3)    
                    elif param =='PHASE':
                        command = lambda d=dev: self.instruments[d].read_input(4)
                    elif param =='AUX_1':
                        command = lambda d=dev: self.instruments[d].read_aux(1)
                    elif param =='AUX_2':
                        command = lambda d=dev: self.instruments[d].read_aux(2)
                    elif param =='AUX_3':
                        command = lambda d=dev: self.instruments[d].read_aux(3)
                    elif param =='AUX_4':
                        command = lambda d=dev: self.instruments[d].read_aux(4)
                        
                elif instr_type == 'HP34401A':
                    if param =='V_DC':
                        command = lambda d=dev: self.instruments[d].read_voltage_DC()
                    elif param =='V_AC':
                        command = lambda d=dev: self.instruments[d].read_voltage_AC()
                elif instr_type == 'None':
                    command = lambda: 0
            else:
                command = lambda: 0
                    
            self.data_channels.append(command)

        
    def run(self):
        self.stopped = False
        self.main_loop()
        self.stop()
        self.emit(SIGNAL("finished(bool)"), self.completed)        
        
    
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
    
    def main_loop(self):
        while self.isStopped() == False:
            data_set = [command() for command in self.data_channels]            
            self.emit(SIGNAL("data(PyQt_PyObject)"), np.array(data_set))              
            time.sleep(self.MEAS_TIME)            

    def main_loop_core(field, f_1, f_2, f_3, coil_voltage, sample_current):
        for sample in range(NUM_SAMPLES):
            offset = 0
            f_src.set_DC(3, offset)
    
            for phase in PHASES:
                f_src.set_phase(3, phase)
                #f_src.sync()
                time.sleep(MEAS_TIME)
                for point in range(NUM_POINTS):
                    time.sleep(MEAS_TIME)
                    data_set = [command() for command in self.data_channels]            
                    self.emit(SIGNAL("data(PyQt_PyObject)"), np.array(data_set))  
                    if self.isStopped() == True:
                        print "terminated"
                        return True, times_arr
    
        phase = 0
        f_src.set_phase(3, phase)
        for offset in OFFSETS:
            ramp_to_setpoint(field + offset)
            time.sleep(MEAS_TIME*2)
            for point in range(NUM_DC_POINTS):   
                time.sleep(MEAS_TIME)
                data_set = [command() for command in self.data_channels]            
                self.emit(SIGNAL("data(PyQt_PyObject)"), np.array(data_set))  
                if self.isStopped() == True:
                    print "terminated"
                    return True, times_arr               
        return False
                    
    def main_loop():
        if using_magnet==True:
            print "setting Amplitudes \n"
            set_amplitudes(COIL_VOLTAGE, 0)
            f_src.set_DC(3, 0)
            lockins[0].set_ref_out(SAMPLE_CURRENT)
            
            print "setting frequencies \n"
            [f_1, f_2, f_3] = set_frequencies(F1, F3, 0)
    
            
            for field in FIELD_SET:
                ramp_to_setpoint(field)
    
                print ("Thermalizing at new field.\n")
                time.sleep(REST_TIME)    
                print ("Starting data acquisition.\n")
                #run the rest of the layers of the loop
                stopped =  self.main_loop_core(field, f_1, f_2, f_3, COIL_VOLTAGE, SAMPLE_CURRENT)
                if stopped:
                    return "terminated"
        else:
            #using_magnet = False means it's a frequency sweep
            #for coil_voltage in COIL_VOLTAGE_SET:
            #for F3 in FREQ3_SET:
            for i in range (1000):
                #F1 = F3/2.0 - 2.5
                print "setting Amplitudes \n"
                set_amplitudes(COIL_VOLTAGE, 0)
                f_src.set_DC(3, 0)
                [f_1, f_2, f_3] = set_frequencies(F1, F3, 0)
                
                print "setting measurement current"
                lockins[0].set_ref_out(SAMPLE_CURRENT)
                
                time.sleep(REST_TIME)  
                stopped =  main_loop_core(0, f_1, f_2, f_3, COIL_VOLTAGE, SAMPLE_CURRENT)
                if stopped:
                    return "terminated"
            
        print "finished"

    def clean_up(self):
        for inst in self.instruments:
            inst.close()      