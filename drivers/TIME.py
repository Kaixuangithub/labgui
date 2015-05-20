# -*- coding: utf-8 -*-
"""
Created on Tue Nov 05 05:09:37 2013

@author: pf
"""

import Tool
import time

param={'Time':'s','dt':'s'}

class Instrument(Tool.MeasInstr):  
    
    #a tag that will be initiallized with the same name than the module
    #const_label=''
    
    def __init__(self): 
        super(Instrument, self).__init__(None,'TIME',True)
        self.t_start=0
                 
    def __del__(self):
        super(Instrument, self).__del__()
#------------------------------------------------------------------------------
    

    def initialize(self):
        self.t_start=time.time()
        
    def measure(self,channel='Time'):
        if self.last_measure.has_key(channel): 

                if channel=='dt':
                    answer=round(time.time()-self.t_start,2)
                else:
                    answer=time.time()
        else:
            print "you are trying to measure a non existent channel : " +channel
            print "existing channels :", self.channels
            answer=None
        return answer