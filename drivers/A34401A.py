# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 15:02:46 2015

@author: pfduc
"""

#!/usr/bin/env python  

'''
class to talk to SCPI-compliant RF sources. Tested on Agilent E4400B
'''

import Tool
from numpy import power

param={'V(AC)':'V','V(DC)':'V','P':'Torr'}

class Instrument(Tool.MeasInstr):  
    def __init__(self,resource_name, debug=False):  
        super(Instrument, self).__init__(resource_name,'A34401A',debug)
        if not self.debug:        
            chan_names=['Voltage','Pressure']    
            for chan,chan_name in zip(self.channels,chan_names):
                self.last_measure[chan]=0
                self.channels_names[chan]=chan_name  
                
    def measure(self,channel='V(DC)'):
        if self.last_measure.has_key(channel):
            if not self.debug: 
                if channel=='V(AC)':
                    answer=self.get_voltage("AC")
                elif channel=='V(DC)':
                    answer=self.get_voltage("DC")                
                elif channel=='P':
                    answer=power(10,self.get_voltage()-5)
            else:
                answer=random.random()
            self.last_measure[channel]=answer
        else:
            print "you are trying to measure a non existent channel : " +channel
            print "existing channels :", self.channels
            answer=None
        return answer
        
    def get_voltage(self,volt_type="DC"):
        if not volt_type in ["AC","DC"]:
            print("You are trying to measure a voltage which is neither AC or DC")
            answer=None
        else:
            v=self.ask("MEAS:VOLT:%s?"%(volt_type))
            answer=float(v[1:-4])*power(10,float(v[-3:]))
        return answer
#    MEASure[:VOLTage][:DC]? [{<
#range
#>|AUTO|MIN|MAX|DEF} [,{<
#resolution
#>|MIN|MAX|DEF}] ] 
        
#if run as own program  
if (__name__ == '__main__'):  
      
    i = Instrument('GPIB0::1')  
    print i.identify()
    print i.get_voltage()
    print i.measure('P')
    i.close()  
