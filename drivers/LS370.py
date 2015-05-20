#!/usr/bin/env python  
import random
import Tool  


param={'':''}

class Instrument(Tool.MeasInstr):  
    
    def __init__(self, resource_name, debug=False): 
        super(Instrument, self).__init__(resource_name,'LS370',debug)
        print self.identify()
      
    def __del__(self):
        super(Instrument, self).__del__()      

    def measure(self,channel):
        if self.last_measure.has_key(channel):
            if not self.debug: 
                answer=self.read_channel(channel)
            else:
                answer=random.random()
            self.last_measure[channel]=answer
        else:
            print "you are trying to measure a non existent channel : " +channel
            print "existing channels :", self.channels
            answer=None
        return answer


    def read_channel (self, chan):
        if not self.debug:        
            self.write ('RDGR? ' + str(chan))      
            data = self.read()
            if data =="":
                return 0
            else:
                return float(data)
        else:
            return 1337.0
    
    def set_heater_range(self, htr_range):
        if not self.debug:    
            if htr_range >= 0 and htr_range < 9:
                self.write('HTRRNG %d'%htr_range)
    
    def set_heater_output(self, percent):
        if not self.debug:          
            if percent >= 0 and percent <= 100:
                self.write('MOUT %.3f'%percent)
    
    def auto_scan (self):
        if not self.debug:        
            self.write('SCAN 1,1')

    def scanner_to_channel(self, chan):
        if not self.debug:
            self.write('SCAN %d,0'%chan)

        


    #if run as own program  
    #if (__name__ == '__main__'):  
      
     #   lockin = device('dev9')  
     #   lockin.set_ref_internal  # no averaging
     #   lockin.close()  
