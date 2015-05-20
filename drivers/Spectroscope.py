# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 18:53:58 2015

@author: pfduc
"""


#import visa
import random
import Tool

class Spectroscope(Tool.MeasInstr):  
    
    def __init__(self, resource_name,name, debug=False,**keyw): 
        super(Spectroscope, self).__init__(resource_name,name,debug,baud_rate=19200)
        
            
    def __del__(self):
        super(Spectroscope, self).__del__()

#------------------------------------------------------------------------------
    
    def acquire_spectrum(self,channel='FLOW'):
        print "prout"
#        if self.last_measure.has_key(channel): 
#            if not self.debug:
#                if channel=='FLOW':
#                    answer=self.ask('*READ:MBAR*L/S?')
#                else:
#                    answer=self.ask('*MEAS:P1:MBAR?')
#                answer=float(answer)
#            else: 
#                answer=100*random.random()
#            self.last_measure[channel]=answer
#        else:
#            print "you are trying to measure a non existent channel : " +channel
#            print "existing channels :", self.channels
#            answer=None
#        return answer
 
  