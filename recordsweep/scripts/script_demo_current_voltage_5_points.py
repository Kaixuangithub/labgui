# -*- coding: utf-8 -*-
"""
Created on Tue May 21 21:38:20 2013

@author: Ben

This is a script to be used with DataTakerThread.py, part of the recordsweep.py
program. This example just loops until the thread is killed. It runs within 
the namespace of DataTakerThread.
"""

channel=self.sweep_param.keys()[0]
start=self.sweep_param[channel][0]
stop=self.sweep_param[channel][1]
step=self.sweep_param[channel][2]
input_array=np.arange(start,stop+step,step)

num_loop=1

#channel=self.sweep_param.keys()[1]
#num_loop=self.sweep_param[channel]

for i in range(num_loop):
#    print "Run number %i"%(i)
    for input_val in input_array:
    #    self.instruments["GPIB0::13"].set_current(input_val)
        self.read_data()
        self.check_stopped_or_paused()
self.isStopped() == True
    
