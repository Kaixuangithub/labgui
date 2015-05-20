# -*- coding: utf-8 -*-
"""
Created on Wed May 08 13:31:59 2013
Paroscientific Digiquartz Pressure sensor 1000 Driver
@author: PF
"""

import random
import Tool
      
param={'PRESSURE':'psi','TEMPERATURE':'C'}      
      
class Instrument(Tool.MeasInstr):  
    def __init__(self, resource_name, debug=False,**keyw): 
#        keyw[term_chars]='\r\n'
        super(Instrument, self).__init__(resource_name,'PARO1000',debug,term_chars='\r\n',**keyw)
        print self.identify("Hello, this is ")
            
    def __del__(self):
        super(Instrument, self).__del__()
        
    def measure(self,channel='PRESSURE'):
        if self.last_measure.has_key(channel):
            if not self.debug:
                if channel=='PRESSURE':
                    command='*0100P3'
                elif channel=='TEMPERATURE':
                    command = '*0100Q3'
                answer=self.ask(command)
                answer=float(answer[5:]) #remove the first 5 characters
            else:
                answer=random.random()
            self.last_measure[channel]=answer
        else:
            print "you are trying to measure a non existent channel : " +channel
            print "existing channels :", self.channels
            answer=None
        return answer
        
    def identify(self,msg=''):
        if not self.debug:
            answer=self.ask('*0100MN')
            answer="PARO"+answer[8:]
        else:
            answer=self.ID_name 
            
        return msg+answer