# -*- coding: utf-8 -*-
"""
Created on Sun May 17 09:05:37 2015


This is a script to be used with DataTaker class within the DataManagment module, part of the LabGui.py
program. This example just loops until the thread is killed. It runs within 
the namespace of DataTaker.


    if you want to access an instrument you can do it through its port name, ie:
        
        self.instruments["you_port_name"]
        
    for example :
        
        self.instruments["GPIB0::13"] 
        
        or
        
        self.instruments["COM1"]
        
    you can then attribute that to a variable and use it to call your instrument's methods
    
    myinstr=self.instruments["GPIB0::13"]
    print(myinstr.ID_name)
    myinstr.set_current(1.0)
    myinstr.measure("Voltage")
    
    
    If you want to read the value of all the parameters of the instruments you connected to the instrument hub you can call the function
    self.read_data(), it will also save them in the output file and plot them.
    
    If you use that function make sure your instrument class defines the method "measure" which take into argument the parameter of the instrument as a string.

"""




"""
this is as simple experiment, it will measure all instruments value 
every 3 seconds until you press the button stop (or the red square) 
which will change the return value of self.isStopped() to True and stop the experiment
"""
while self.isStopped() == False:
    self.read_data()
    time.sleep(3)

    
