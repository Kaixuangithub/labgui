# -*- coding: utf-8 -*-
"""
Created on Wed June 12 17:26:26 2014
Agilent E4400B 1GHz signal generator
@author: pfduc
"""

#!/usr/bin/env python  
import numpy as np
import time
import random
import Tool  


param={'V':'V','freq':'Hz'}

class Instrument(Tool.MeasInstr):  
    
    def __init__(self, resource_name, debug=False, V_step_limit = None): 
        super(Instrument, self).__init__(resource_name,'E4400B',debug)
        
    def __del__(self):
        super(Instrument, self).__del__()      

    def measure(self,channel='V'):
        if self.last_measure.has_key(channel):
            if not self.debug: 
                if channel=='V':
                    answer=self.ask(':READ?') #  0 #this is to be defined for record sweep
                    answer = float(answer.split(',',1)[0])
                if channel=='freq':
                    answer=self.get_frequency()
            else:
                answer=random.random()
            self.last_measure[channel]=answer
        else:
            print "you are trying to measure a non existent channel : " +channel
            print "existing channels :", self.channels
            answer=None
        return answer

    def reset(self): 
        if not self.debug:
            self.write('*RST')
            time.sleep(1)
    
    def set_frequency(self,f):
        if not self.debug:
            self.write(':FREQ '+str(f) + 'Hz')
            
    def get_frequency(self):
        f=self.ask(':FREQ?')
        answer=float(f[1:-4])*np.power(10,float(f[-3:]))
        return answer

    def sweep_frequency(self,fstart,fstop,df,dwell=2e-3):
        freq_range=np.arange(fstart,fstop+df,df)
        for freq in freq_range:
            self.set_frequency(freq)
            time.sleep(dwell)
            
if __name__=="__main__":
    
    
    i=Instrument('GPIB0::19',debug=False)
    i.set_frequency(5.07823e+8)
    f=i.measure("freq")
    print f
    print float(f[-3:])
    print float(f[1:-4])
    print float(f[1:-4])*np.power(10,float(f[-3:]))
    