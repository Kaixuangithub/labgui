#!/usr/bin/env python  

import Tool
import time
import random

param={'Field':'T'}
      
class Instrument(Tool.MeasInstr): 
    def __init__(self, resource_name, debug=False,read_only=False): 
        super(Instrument, self).__init__(resource_name,'IPS120',debug,term_chars = '\r')
        
        self.read_only = read_only

        if self.read_only == False:
            self.set_extended()
            
            print (self.read_status())
        self.clear()
        
            
    def __del__(self):
        super(Instrument, self).__del__() 
            
    def measure(self,channel):
        if self.last_measure.has_key(channel):
            if not self.debug:
                if channel=='Field': 
                    answer=self.read_field()
            else:
                answer=random.random()
            self.last_measure[channel]=answer
        else:
            print "you are trying to measure a non existent channel : " +channel
            print "existing channels :", self.channels
            answer=None
        
        return answer
        
    def clear_buffer(self):
        if not self.debug:
            self.clear()
        
    def unlock(self):
        if not self.debug:
            return self.ask('@0C3\r')

    def set_field_sweep_rate(self, rate):
        if not self.debug:        
            if rate <= 0.20 and rate >0:        
                return self.ask('@0T%.4f\r' % rate)
            else:
                return "set rate too fast"
                
    def set_point_field(self, val):
        if not self.debug:      
            if val >=-9 and val <=9:
                return self.ask('@0J%.4f\r'%val)
            
    def hold(self):
        if not self.debug:      
            return self.ask('@0A0\r')

    def goto_set(self):
        if not self.debug:      
            return self.ask('@0A1\r')

    def goto_zero(self):
        if not self.debug:      
            return self.ask('@0A2\r')
                                   
    def read_param(self, param):
        if not self.debug:      
            return self.ask ('@0R' + str(param) + '\r')  
        
    def read_field(self):
        if not self.debug:      
            return float(self.ask('@0R7\r').lstrip('R')) 
        else:
            return 0

    def read_status(self):
        if not self.debug:      
            return self.ask ('@0X\r')  

    def set_extended(self):
        if not self.debug:      
            return self.write ('@0Q4\r')
    
    # waits until a setpoint is reached. Can't be interrupted.        
    def ramp_to_setpoint(self,field):
        self.set_point_field(field)
        self.goto_set()
    
        still_ramping = True
        print ("Ramping field...")
        while still_ramping:   
            actual_field = self.read_field()
            # floating point numbers may be close enough but not "pre
            still_ramping = abs (actual_field - field) > 0.00001
            time.sleep(1)    

    #if run as own program  
    #if (__name__ == '__main__'):  
      