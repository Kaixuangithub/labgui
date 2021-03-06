#!/usr/bin/env python  
import Tool
import random


param={'V_DC':'V','V_AC':'V','I_DC':'A','I_AC':'A','R':'Ohm','READ':'?'}

class Instrument(Tool.MeasInstr):  
    def __init__(self, resource_name, debug=False): 
        super(Instrument, self).__init__(resource_name,'HP34401A',debug)  
    
    def __del__(self):
        super(Instrument, self).__del__()
            
    def identify(self,msg=''):
        if not self.debug:
            #the *IDN? is probably not working
            return msg#command for identifying
        else:
            return msg+self.ID_name      
            
    def measure(self,channel):
        if self.last_measure.has_key(channel): 
            if not self.debug:
                if channel=='V_DC': 
                    answer= self.read_voltage_DC()
                elif channel=='V_AC': 
                    answer= self.read_voltage_AC()
                elif channel=='I_DC':
                    answer= self.read_current_DC()
                elif channel=='I_AC':
                    answer=self.read_current_AC()
                elif channel=='R':
                    answer=self.read_resistance()
                elif channel=='READ':
                    answer=self.read_any()
            else: 
                answer=random.random()
            self.last_measure[channel]=answer
        else:
            print "you are trying to measure a non existent channel : " +channel
            print "existing channels :", self.channels
            answer=None
        return answer

    def read_any(self):  
        if not self.debug:
            string_data = self.ask('READ?')
            return float(string_data)
        else:
            return 123.4
            
    def read_voltage_DC(self):  
        if not self.debug:
            string_data = self.ask(':MEAS:VOLT:DC?')
            return float(string_data)
        else:
            return 123.4

    def read_voltage_AC(self):  
        if not self.debug:
            string_data = self.ask(':MEAS:VOLT:AC?')
            return float(string_data)
        else:
            return 123.4

    def read_current_DC(self):  
        if not self.debug:
            string_data = self.ask(':MEAS:CURR:DC?')
            return float(string_data)
        else:
            return 123.4

    def read_current_AC(self):  
        if not self.debug:
            string_data = self.ask(':MEAS:CURR:AC?')
            return float(string_data)
        else:
            return 123.4

    def read_resistance(self):  
        if not self.debug:
            string_data = self.ask(':MEAS:RES?')
            return float(string_data)
        else:
            return 123.4                   
            
        
    #if run as own program  
    #if (__name__ == '__main__'):  
      
     #   lockin = device('dev9')  
     #   lockin.set_ref_internal  # no averaging
     #   lockin.close()  
