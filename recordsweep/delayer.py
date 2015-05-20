# -*- coding: utf-8 -*-
"""
Created on Wed May 15 00:52:02 2013
delayer for setpoint of lakeshore340
this will run in a separate thread and will attempt to sweep in the Lakeshore
@author: Michel
"""

#import visa
import time
import numpy as np
import LS340                #driver for Lakeshore 340 temperature controller
import converter_RuOx_U02627  #calibrated conversion of resistance for RuOx U02627

#myinstrument = visa.instrument('GPIB0::12')

#myinstrument.write('SETP 2, 1668')

#********************LOOP to warm cell up incrementally************
currentTemp = 0             #temperature in Kelvin to stop iterating if I get too warm
temperatureList = np.arange(2.17,2.7,0.12)

delay = 0.9*np.ones(temperatureList.size)
delay[0]=0.01              #first point will only last this long...
# delay[2:]=0.9
tau = 3400                 #tau is the equilibration time

ls = LS340.LS340('GPIB0::12')

#**************************look for typo in temperature requested*********
is_input_correct=True

if np.amax(temperatureList)>3:  
    is_input_correct=False        #if you get here, then 
#*******************************************************************

#*******ready to start in principle, print planned setpoints and total time of sweep
print 'game is ON!!'
print 'list of temperatures'
exp_duration = 0  #initialize
for t,d in zip(temperatureList,delay):   #print list of expected resistance setPoint
    exp_duration = exp_duration + d*tau    
    print str(t) + 'K until '+ time.ctime(time.time() + exp_duration)
      
#print total time    
#print 'experiment will run for ' + str(exp_duration/3600.0) + 'hours, until '+ time.ctime(time.time()+exp_duration)


if is_input_correct:
    for T, d in zip(temperatureList,delay):
        R = converter_RuOx_U02627.T_to_R(T)
        print "\n setpoint will be %.3f"%(R) + 'Ohm = ' + str(T) + 'K'
        print 'until ' + time.ctime(time.time()+d*tau)

        ls.setPoint(R,2)  #ask to change setpoint of loop 2
        time.sleep(d*tau) #wait for (multiple times tau)

    time.sleep(1000)    
    ls.setPoint(converter_RuOx_U02627.T_to_R(temperatureList[0]),2) #return to starting point
#******************************************************************

