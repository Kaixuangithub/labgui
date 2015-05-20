#!/usr/bin/env python  
#import visa 
import Tool
import string
import random


param={'':''}

class Instrument(Tool.MeasInstr):  
    def __init__(self, resource_name, debug=False): 
        super(Instrument, self).__init__(resource_name,'HP4263B',debug)  
    
    def __del__(self):
        super(Instrument, self).__del__()
            
    def identify(self,msg=''):
        if not self.debug:
            #the *IDN? is probably not working
            return msg#command for identifying
        else:
            return msg+self.ID_name      

    def measure(self,channel):
        if self.last_measure.has_key(channel): 
            if not self.debug:
                #to be changed to measure wanted quantities
                answer=self.read_data()
            else: 
                answer=random.random()
            self.last_measure[channel]=answer
        else:
            print "you are trying to measure a non existent channel : " +channel
            print "existing channels :", self.channels
            answer=None
        return answer
    
    def trigger(self):  
        if not self.debug:
            self.write(':TRIG:IMM')

    def read_data(self):  
        if not self.debug:
            string_data = self.ask(':FETC?')
            list_data = string.split(string_data, ',')
            return float(list_data[2])
        else:
            return 123.4
                
    def set_trigger_bus(self):
        if not self.debug:
            self.write (':TRIG:SOUR BUS')
  
    def set_comparator(self, state):
        if not self.debug:
            if state==True:         
                self.write(':CALC1:LIM:STAT ON')
                self.write(':CALC2:LIM:STAT ON')
            else:
                self.write(':CALC1:LIM:STAT OFF')
                self.write(':CALC2:LIM:STAT OFF') 

    def raw_to_mK(self,raw_value):
        return -4.36894/(-raw_value*1000+2.93629)
        
    #if run as own program  
    #if (__name__ == '__main__'):  
      
     #   lockin = device('dev9')  
     #   lockin.set_ref_internal  # no averaging
     #   lockin.close()  
