#!/usr/bin/env python  

'''
class to talk to SCPI-compliant RF sources. Tested on Agilent E4400B
'''

import Tool

param={'':''}

class Instrument(Tool.MeasInstr):  
    def __init__(self,resource_name, debug=False):  
        super(Instrument, self).__init__(resource_name,'RF_source',debug)
        if not self.debug:        
            self.POW_MIN = self.inst.ask(':SOUR:POW? MIN')
            self.POW_MAX = self.inst.ask(':SOUR:POW? MAX')

    def set_freq(self, freq):
        if not self.debug:
            self.write(':SOUR:FREQ:CW ' + str(freq))        

    def set_power(self, power):
        if not self.debug:
            self.write(':POW:LEV:IMM:AMPL ' + str(power))  
        
    #if run as own program  
    #if (__name__ == '__main__'):  
      
     #   lockin = device('dev9')  
     #   lockin.set_ref_internal  # no averaging
     #   lockin.close()  
