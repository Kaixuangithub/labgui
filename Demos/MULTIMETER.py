# -*- coding: utf-8 -*-

import random
import Tool
from sys import modules
from os.path import splitext,basename
#this will be the name of your instrument parameters
param={'I':'A','V':'V'}

class Instrument(Tool.MeasInstr):

    def __init__(self, resource_name, debug=False): 
        #find the name of this module to pass it to the init function of the parent class
        modulename = modules[self.__module__].__file__
        modulename = splitext(basename(modulename))[0]
        super(Instrument, self).__init__(resource_name,modulename,debug)
        #this will be the the name of your channels of measure
        chan_names=['current','voltage']
        self.resistance=10
        self.error=1.6
        self.my_current=-1
        
        
        #initializes the internal variables
        for chan,chan_name in zip(self.channels,chan_names):
             self.last_measure[chan]=0
             self.channels_names[chan]=chan_name
      
    def __del__(self):
        super(Instrument, self).__del__()      
             
    def set_current(self,current):
        self.my_current=current
#        print "set the current to",self.my_current
        
    def measure(self,channel):
        if self.last_measure.has_key(channel):
            if not self.debug:
                answer=0
                if channel=='I': 
                    answer=self.my_current
                elif channel=='V': 
                    answer=self.my_current*self.resistance+(random.random()-0.5)*self.error
                    
            else:
                answer=0
                if channel=='I': 
                    answer=self.my_current
                elif channel=='V': 
#                    answer=(self.my_current*self.resistance)*(1+random.random()*self.error)
                    answer=self.my_current*(self.resistance+(random.random()-0.5)*self.error)
            self.last_measure[channel]=answer
        else:
            print "you are trying to measure a non existent channel : " +channel
            print "existing channels :", self.channels
            answer=None
        return answer

if __name__=="__main__":

    i=Instrument("a",True)