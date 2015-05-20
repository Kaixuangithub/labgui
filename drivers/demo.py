# -*- coding: utf-8 -*-

import random
import Tool
from sys import modules
from os.path import splitext,basename

"""
    this will be the name of your instrument parameters and their units (units are not essential, they are only here for user information)
    you have to define those if you want to select a parameter to measure in LabGui's "Instrument setup" widget
"""
param={'speed':'m/s','T':'K','U':'V'}
   
class Instrument(Tool.MeasInstr):
    """
        This is the minimum number of methods that any Instrument class should have
    """

    def __init__(self, resource_name, debug=False): 
        #find the name of this module to pass it to the init function of the parent class
        modulename = modules[self.__module__].__file__
        modulename = splitext(basename(modulename))[0]
        super(Instrument, self).__init__(resource_name,modulename,debug)
        #this will be the the name of your channels of measure
        chan_names=['speed','temperature','voltage']    
        
        #initializes the internal variables
        for chan,chan_name in zip(self.channels,chan_names):
             self.last_measure[chan]=0
             self.channels_names[chan]=chan_name
      
    def __del__(self):
        super(Instrument, self).__del__()      
              
    def measure(self,channel):
        if self.last_measure.has_key(channel):
            if not self.debug:
                answer=0
                if channel=='speed': 
                    #modify here according to what you want your instrument to do
                    print "measuring the speed"
                    answer=1
                elif param[channel]=='V': 
                    #modify here according to what you want your instrument to do
                    print "measuring some voltage"
                    answer=2
                    
            else:
                answer=random.random()
            self.last_measure[channel]=answer
        else:
            print "you are trying to measure a non existent channel : " +channel
            print "existing channels :", self.channels
            answer=None
        return answer

if __name__=="__main__":

    i=Instrument("a",True)