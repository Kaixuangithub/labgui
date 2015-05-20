import time
try:
    import serial
except:
    pass
import Tool
import random
#!/usr/bin/env python  
#import string, os, sys, time  
#import io
param={'1':'eV','2':'K'}

class Instrument(Tool.MeasInstr):  
    def __init__(self, port='/dev/ttyUSB0', debug=False):  
        self.debug = debug
        self.ID_name='MKS_gauge'
        if not self.debug:
            #I managed to use visa to talk to HLT560  which has a rs232 cable I plugged into a rs232 to usb converter. -PF
            self.connexion = serial.Serial(
                port,
                baudrate=9600,
                parity=serial.PARITY_EVEN,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.SEVENBITS,
                timeout=1 )
            #self.sio = io.TextIOWrapper(io.BufferedRWPair(self.connexion,self.connexion))
            self.sio = self.connexion
            self.channels=[]
            self.units=[]
            for p,unit in param.items():
                self.channels.append(p)
                self.units.append(unit)
        
            #initializes the first measured value to 0 and the channels' names 
            for chan in self.channels:
                self.last_measure[chan]=0
                self.channels_names[chan]=chan

    def measure(self,channel):
        if self.last_measure.has_key(channel):
            if not self.debug: 
                answer=self.get_pressure(channel)
            else:
                print "the channel " +channel
                answer=random.random()
            self.last_measure[channel]=answer
        else:
            print "you are trying to measure a non existent channel : " +channel
            print "existing channels :", self.channels
            answer=None
        return answer  
  
    def get_pressure(self, chan):
        chan=float(chan)
        if not self.debug:
            if chan==1:
                self.write('@6011?')
            elif chan==2:
                self.write('@6012?')
            else:
                return None        
            return self.sio.read(13)
        else:
            return 1.23e-3
            
    def write(self, stri):
        if not self.debug:     
            self.sio.write(stri + '\r\n')            

    def readline(self):
        if not self.debug:     
            return self.sio.readline()
    
    def read2(self):
         if not self.debug:     
             sio = self.sio
             time.sleep(0.1)
             out=''
             while sio.inWaiting() > 0:
                 out += sio.read(1)
             return (out)

    #initialization should open it already    
    def reopen(self):
         if not self.debug:
             self.connexion.open()
        
    def close(self):  
         if not self.debug:
             self.sio.close() 
