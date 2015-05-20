#!/usr/bin/env python  
#import visa
import Tool
from collections import OrderedDict

#use an ordered dictionary so that the parameters show up in a pretty order :)
param = OrderedDict([('X','V'), ('Y', 'V'),( 'R','V'), ('PHASE', 'degrees'), 
         ('AUX_1','V'), ('AUX_2','V'), ('AUX_3','V'), ('AUX_4','V'), ('FREQ', 'Hz')])
     
class Instrument(Tool.MeasInstr):  
    def __init__(self, resource_name, debug = False):  
        super(Instrument, self).__init__(resource_name,'SRS830',debug)
        
    def __del__(self):
        super(Instrument, self).__del__()

    def measure(self,channel):
        if param.has_key(channel):
            if channel=='X':
                answer=self.read_input (1)
            elif channel=='Y':
                answer=self.read_input (2)
            elif channel=='R':
                answer=self.read_input (3)
            elif channel=='PHASE':
                answer=self.read_input (4)                    
            elif channel=='AUX_1':
                answer=self.read_aux (1)
            elif channel=='AUX_2':
                answer=self.read_aux (2)
            elif channel=='AUX_3':
                answer=self.read_aux (3)
            elif channel=='AUX_4':
                answer=self.read_aux (4)
            elif channel=='FREQ':
                answer=self.get_freq ()                    
            self.last_measure[channel]=answer
        else:
            print "you are trying to measure a non existent channel : " +channel
            print "existing channels :", self.channels
            answer=None
        return answer         
           
    def set_scale(self, scale):
            self.write('SENS ' + str(scale))
            
    def set_ref_internal(self):  
            self.write('FMOD 1')
        
    def set_ref_external(self):  
            self.write('FMOD 0')

    def set_phase(self, shift):     
            self.write ('PHAS ' + str(shift))
     
    def set_amplitude(self, amplitude):    
            self.write('SLVL' + str(amplitude))
        
    def get_amplitude(self):
        if not self.debug:
            return self.ask('SLVL?')
        else:
            return 1.0

    def set_freq(self, freq):
        self.write ('FREQ ' + str(freq))

    def get_freq(self):
        if not self.debug:
            return float(self.ask ('FREQ?'))
   
    def set_harm(self, harm):
        self.write ('HARM ' + str(harm))

    def set_ref_out(self, voltage):
        self.write ('SLVL ' + str(voltage))
        
    def get_ref_out(self, voltage):
        if not self.debug:
            self.write ('SLVL?')
            return self.read()        
        else:
            return 1.234
               
    def read_aux (self, num):
        if not self.debug:
            self.write ('OAUX? ' + str(num))
            return float(self.read())
        else:
            return 1.234     
    
    def set_aux_out(self, chan, volts):
        self.write ('AUXV ' + str(chan) + ", " + str(volts))       
    
    def read_input (self, num):
        '''
        Reads the specificed input of the lockin. 1=x, 2=y, 3=r, 4=phase
        '''
        if not self.debug:            
            return float(self.ask ('OUTP? ' + str(num)))    
        else:
            return 1.23e-4

# Plan to move to using Instrument as the name within, but for back-compatibility
# include this (so you can still use SRS830.SRS830 instead of SRS830.Instrument)
#SRS830 = Instrument

    #if run as own program  
    #if (__name__ == '__main__'):  
      
     #   lockin = device('dev9')  
     #   lockin.set_ref_internal  # no averaging
     #   lockin.close()  
