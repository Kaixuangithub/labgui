# -*- coding: utf-8 -*-
"""
Created on Tue May 29 14:28:29 2012
Lakeshore 340 Driver
@author: Bram
issues:
   - need to hardcode limits of valid setPoint() resistance input
"""
#import visa
import random
#import alarm_toolbox as alarm
import Tool
import converter_RuOx_U02627 as convT
#import numpy as np

param={'A':'K','B':'K','C':'kOhm','D':'kOhm','C(T)':'kOhm_to_K','D(T)':'kOhm_to_K'}
   
class Instrument(Tool.MeasInstr):

    def __init__(self, resource_name, debug=False): 
        super(Instrument, self).__init__(resource_name,'LS340',debug)
        chan_names=['Charcoal','1Kpot','He3Pot','Cell']    
        for chan,chan_name in zip(self.channels,chan_names):
             self.last_measure[chan]=0
             self.channels_names[chan]=chan_name
      
    def __del__(self):
        super(Instrument, self).__del__()      
              
    def measure(self,channel):
        if self.last_measure.has_key(channel):
            if not self.debug:
                answer=0
                if param[channel]=='K': 
                    answer=float(self.ask('KRDG?'+channel)) #read in Kelvin thrithy 
                elif param[channel]=='kOhm': 
                    answer=float(self.ask('SRDG?'+channel)) #read in kOhm  
                elif param[channel]=='kOhm_to_K':
                    answer=round(convT.R_to_T(float(self.ask('SRDG?'+channel))),4)
            else:
                answer=random.random()
            self.last_measure[channel]=answer
        else:
            print "you are trying to measure a non existent channel : " +channel
            print "existing channels :", self.channels
            answer=None
        
        return answer
        
        #SETP Configure Control Loop Setpoint
#Input: SETP <loop>, <value>
#Returned: Nothing
#Remarks: Configures the control loop setpoint.
#<loop> Specifies which loop to configure.
#<value> The value for the setpoint (in whatever units the setpoint is using).
#Example: SETP 1, 122.5[term] - Control Loop 1 setpoint is now 122.5 (based on its units).
   
                    
    def setPoint(self, resistance, loop):  #float value of resistance in Ohm, loop 1 or 2
        if not self.debug:
            if resistance > 1050:
                self.connexion.write('SETP '+ str(loop) + ', ' + "%.3f"%(resistance))
            else:
                print 'invalid setpoint for the Lakeshore'
 
    def setTemp(self, resistance, loop):  #float value of resistance in Ohm, loop 1 or 2
        if not self.debug:
            if resistance < 40:
                self.connexion.write('SETP '+ str(loop) + ', ' + "%.3f"%(resistance))
            else:
                print 'invalid setpoint for the Lakeshore'                   
        
    #set an alarm that will actually ring from the instrument, this is to be desactivated when the experimentalist is not him self in the lab for the sake of others   
    def set_alarm(self,value_channel,on_off,value_source,value_high,value_low,beep_on_off):
        sep=', '        
        self.write('ALARM '+ value_channel + sep + str(on_off) + sep + str(value_source) +sep +str(value_high) + sep+str(value_low)+';BEEP '+str(beep_on_off) )
        
    #this shouldbe changed into self.ask once this function will be changed
    def get_alarm_status(self):
        return self.ask('ALARMST?')
    
    #MM,DD,YYY,HH,mm,SS,sss
    def get_datetime(self):
        return self.ask('DATETIME?')

    def get_PID(self):
        return self.ask('PID?')
        
    def set_PID(self,value_loop,value_P,value_I,value_D):
        sep=', ' 
        self.write('PID '+value_loop+sep+str(value_P)+sep+str(value_I)+sep+str(value_D))
        
    def set_heater_range(self,value_range):
        return self.ask('RANGE '+str(value_range) +';RANGE?')