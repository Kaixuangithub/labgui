# -*- coding: utf-8 -*-
"""
Created on Thu Mar 06 14:07:29 2014
Phoenix L300 Leak Detector
@author: PF
"""

#import visa
import random
import Tool

param={'FLOW':'mbarl/s','P1':'mbar'}  

class Instrument(Tool.MeasInstr):  
    
    def __init__(self, resource_name, debug=False): 
        super(Instrument, self).__init__(resource_name,'PL300',debug,baud_rate=19200)
        
            
    def __del__(self):
        super(Instrument, self).__del__()

#------------------------------------------------------------------------------
    
    def measure(self,channel='FLOW'):
        if self.last_measure.has_key(channel): 
            if not self.debug:
                if channel=='FLOW':
                    answer=self.ask('*READ:MBAR*L/S?')
                else:
                    answer=self.ask('*MEAS:P1:MBAR?')
                answer=float(answer)
            else: 
                answer=100*random.random()
            self.last_measure[channel]=answer
        else:
            print "you are trying to measure a non existent channel : " +channel
            print "existing channels :", self.channels
            answer=None
        return answer
   
    def get_status(self):
        return self.ask('STAT?')    
  