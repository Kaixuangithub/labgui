# -*- coding: utf-8 -*-
"""
Created on Wed May 16 16:22:26 2012
Keithley 2400
@author: Bram
"""

#!/usr/bin/env python  
import time  
      
import random
import Tool  


param={'V':'V','I':'A'}

class Instrument(Tool.MeasInstr):  
    
    def __init__(self, resource_name, debug=False): 
        super(Instrument, self).__init__(resource_name,'KT2400',debug)
        #self.standard_setup()
      
    def __del__(self):
        super(Instrument, self).__del__()      

    def measure(self,channel):
        if self.last_measure.has_key(channel):
            
            if channel == 'V':
                if not self.debug: 
                    answer=self.ask(':READ?') #  0 #this is to be defined for record sweep
                    answer = float(answer.split(',')[0])
                else:
                    answer=random.random()
                self.last_measure[channel]=answer
                
            elif channel == 'I':
                if not self.debug: 
                    answer=self.ask(':READ?') #  0 #this is to be defined for record sweep
                    answer = float(answer.split(',')[1])
                else:
                    answer=random.random()
                self.last_measure[channel]=answer 
                
        else:
            print "you are trying to measure a non existent channel : " +channel
            print "existing channels :", self.channels
            answer=None
        return answer   
        
            # Should Read KEITHLEY INSTRUMENTS INC., MODEL nnnn, xxxxxxx, yyyyy/zzzzz /a/d
        
    def reset(self): 
        if not self.debug:
            self.write('*RST')
            time.sleep(1)
        # Resets the instrument
#
#    def operation_complete(self):
#        if not self.debug:
#            self.write ('*OPC')
#        # Returns a 1 after all the commands are complete
#
    def configure_measurement(self,sensor):
        if not self.debug:
            #VOLT,CURR RES
            s = ':%s:RANG:AUTO ON' % sensor
            print(s)
            self.write (s)
#    
#    def configure_voltage_source(self):
#        if not self.debug:
#            self.write(':SOUR:FUNC:MODE VOLT')
#    
#    def set_current_compliance(self,compliance):
#        if not self.debug:
#            self.write(':SENS:CURR:PROT:LEV '+ str(compliance))
#
    def configure_output(self, source_mode = 'VOLT' , output_level = 0, compliance_level = 0.001):
        if not self.debug:
            # source_mode: VOLT, CURR
            # output_level: in Volts or Amps
            # compliance level: in Amps or Vol
            if source_mode == 'CURR':
                protection = 'VOLT'
            else:
                protection = 'CURR'
            
            s = ':SOUR:FUNC %s;:SOUR:%s %f;:%s:PROT %r;' % (source_mode, source_mode, output_level, protection, compliance_level)
            self.write(s)
#            
#    
    def enable_output(self):
        if not self.debug:
            self.write (':OUTP ON;')
#        
#    def disable_output(self):
#        if not self.debug:
#            self.write (':OUTP OFF;')        
#        
    
    def set_value(self, val): # for interferometer program
        self.set_voltage(val)    
    
    def set_voltage(self, voltage, port=0):
        if not self.debug:
            # port is a meaningless variable to ensure compatibility with DAC488
            s = ':SOUR:FUNC VOLT;:SOUR:VOLT %f' % voltage

            self.write (s)
        else:
            print "voltage set to "+str(voltage) +" on " +self.ID_name
#    def configure_multipoint(self,sample_count=1,trigger_count=1,output_mode='FIX'):
#        if not self.debug:
#            s = ':ARM:COUN %d;:TRIG:COUN %d;:SOUR:VOLT:MODE %s;:SOUR:CURR:MODE %s;' % (sample_count,trigger_count,output_mode,output_mode)
#            self.write(s)
#        
#    def configure_trigger(self,arming_source='IMM',timer_setting=0.01,trigger_source='IMM',trigger_delay=0.0):
#        if not self.debug:
#            # arming source: IMM,BUS,TIM,MAN,TLIN,NST,PST,BST  
#                # Immediate Arming
#                # Software Trigger Signal
#                # Timer (set with <B>Timer Setting</B>)
#                # Manual (pressing the TRIG button on the instrument)
#                # Rising SOT Pulse
#                # Falling SOT Pulse
#                # Any SOT Pulse
#                # trigger source: IMM,TLIN
#                # timer setting: interval of time to wait before arming the trigger
#                # trigger delay: the time to wait after the trigger has been
#                s = ':ARM:SOUR %s;:ARM:TIM %f;:TRIG:SOUR %s;:TRIG:DEL %f;' % (arming_source,timer_setting,trigger_source,trigger_delay)
#                self.write(s)
#    
#    def initiate(self):
#        if not self.debug:
#            # Clears the trigger, then initiates
#            s = ':TRIG:CLE;:INIT;'
#            self.write(s)
#            time.sleep(0.01)
#            # delay to replace OPC
#        
#    def wait_for_OPC(self):
#        if not self.debug:
#            self.write('*OPC;')
#        
#    def fetch_measurements(self):
#        if not self.debug:
#            print self.ask(':FETC')
#        
    def standard_setup(self):
        if not self.debug:
            self.reset()
            self.configure_measurement('VOLT')
            self.configure_measurement('CURR')
            self.configure_measurement('RES')
            self.configure_output('VOLT',0,0.00005)
            self.enable_output()
#        
#    def close(self):
#        if not self.debug:
#            self.disable_output()
#            self.write('*RST')
#            self.write('*CLS')
#            self.write(':*SRE 0')
#            #super(Instrument,self).close()

    def leaking(self, p_tolerance):
        # Returns 1 if the current leaking is greater than some supplied tolerance
        # Returns 0 otherwise
        if abs(self.measure('I')) > abs(p_tolerance):
            return 1
        else:
            return 0
            
    def conditional_leak_check(self, p_code, p_leak_check_list = [], p_tolerance = 1E-6):
        # Code = 0 --> do no leak check        
        if p_code == 0 or p_code == 1:
            return 0
        # Code = 2 --> Leak check ALL supplied gates, if ONE leaks, report
        elif p_code == 2:
            for gate in p_leak_check_list:
                boolean = gate[0].leaking(gate[1])
                if boolean == 1:
                    return 1
            return 0
        # Code = 1 --> Leak check only this gate
        elif p_code == 3:
            return self.leaking(p_tolerance)
            
    def move_voltage(self, p_reader, p_target_voltage, step = 0.01, wait = 0.05, p_leak_check_code = 0, p_leak_check_list = 0, p_tolerance = 1E-6):
        # Safely moves the voltage from its current value to a target voltage
        # p_leak_check_code = 0 ----> No leak checking and cannot stop with p_reader.isStopped()
        # p_leak_check_code = 1 ----> No leak checking, can be stopped
        # p_leak_check_code = 2 ----> All keithleys and tolerance list in p_leak_check_list checked (but not this keithley if not in the list)
        # p_leak_check_code = 3 ----> Only this Keithley checked for leaks
        # p_leak_check_list syntax : ([keithley_object_1, keithley_1_tolerance],[keithley_object_2, keithley_2_tolerance],etc.)
        current_voltage = self.measure('V') # Update voltage to ensure proper information
        # Parse move direction cases
        if current_voltage < p_target_voltage: # If keithley needs to move up
            # While the current_voltage is not within one increment of the target voltage
            while current_voltage < p_target_voltage:
                # Stop if it needs to
                if p_leak_check_code != 0:
                    if p_reader.isStopped():
                        print "Stopping"
                        return 0
                # Increment the current voltage by a safe amount
                current_voltage += step
                self.set_voltage(current_voltage)
                # If any gate leaking
                boolean = self.conditional_leak_check(p_leak_check_code, p_leak_check_list, p_tolerance)
                if boolean == 1:
                    # Exit with error
                    return 0
                # Wait
                time.sleep(wait)
        if current_voltage > p_target_voltage: # If keithley needs to move up
            # While the current_voltage is not within one increment of the target voltage
            while current_voltage > p_target_voltage:
                # Stop if it needs to
                if p_leak_check_code != 0:
                    if p_reader.isStopped():
                        print "Stopping"
                        return 0
                # Increment the current voltage by a safe amount 
                current_voltage -= step
                self.set_voltage(current_voltage)
                # If any gate leaking
                boolean = self.conditional_leak_check(p_leak_check_code, p_leak_check_list, p_tolerance)
                if boolean == 1:
                    # Exit with error
                    return 0
                # Wait
                time.sleep(wait)
        # Correct for offset
        self.set_voltage(p_target_voltage)
        time.sleep(1)
        # return success
        print "Done moving"
        return 1
        
        def set_compliance(self):
            # Will eventually create set_compliance function here
            if not self.debug:
                self.write(':SENS:CURR:PROT[:LIM]')
                time.sleep(1)
            
        

if __name__=="__main__":
    
    topgate=Instrument("GPIB0::24")

    topgate.configure_output('VOLT', 0, 1E-8)
    topgate.measure()
    