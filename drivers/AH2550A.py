# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 14:01:13 2013

@author: Lilly Tong
"""

import os, time, sys
import Tool
import random
param = {'Capacitance':'pF'}

class Instrument(Tool.MeasInstr):
    
    def __init__(self, resource_name, debug = False,**keyw):
        super(Instrument, self).__init__(resource_name,'AH2550A',debug,**keyw)
        self.identify("Hello, this is ")
        
        
    def measure(self,channel):
        if self.last_measure.has_key(channel):
            if not self.debug:
                if channel=='Capacitance': 
                    answer=self.capacitance(self.single())
            else:
                answer=random.random()
            self.last_measure[channel]=answer
        else:
            print "you are trying to measure a non existent channel : " +channel
            print "existing channels :", self.channels
            answer=None
        
        return answer
        
    def average(self, average): #4 is default, higher the number slower the measurement
        if self.debug == False:
            self.write('AVERAGE ' + str(average))
        else:
            print "average - debug mode"
            
    def capacitance(self, msg): #parses the string and only returns capacitance

        if self.debug == False:

            return float(msg[3:13])
        else:
            print "capacitance - debug mode"
            
    def continuousON(self):
        if self.debug == False:
            self.write('CONTINUOUS')
        else:
            print "continuous - debug mode"
    
    def continuousOFF(self):
        if self.debug == False:
            self.write('CONTINUOUS OFF')
        else:
            print "continuousOFF - debug mode"
    
    def frequency(self, freq): #broken function. Something wrong with capacitance bridge
        if self.debug == False:
            self.write('FREQUENCY' + str(freq))
        else:
            print "frequency - debug mode"    
            
    
    
    def showFrequency(self):
        if self.debug == False:
            return self.ask('SHOW FREQUENCY')
        else:
            print "show frequency - debug mode"    

    
    def single(self):
        if self.debug == False:
            return self.ask('SINGLE')
        else:
            print "single - debug mode"
    


#following code has been tested and known to work. 
if (__name__ == '__main__'):
   myinst=Instrument('GPIB::28') 
   myinst.average(8)
   myinst.continuousON()
   for i in range(10):
        capacitance=myinst.capacitance(myinst.read()) #a float, displays in pF
        print capacitance
        time.sleep(3)
   myinst.continuousOFF()
    
    

