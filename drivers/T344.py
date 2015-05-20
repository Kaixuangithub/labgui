import time
try: 
    import serial
except:
    pass
#!/usr/bin/env python  
import Tool 

param={'':''}
      
class Instrument(Tool.MeasInstr):
    """
    class to communicate with Highland Technologies T344 signal generator through RS-232
    
    Parameters
    ----------    
    Name of the port (ie. COM1)

    """     
    def __init__(self, port='COM1', debug=False):  
        self.debug = debug
        self.ID_name='T344'
        if not self.debug:
            #I managed to use visa to talk to HLT560  which has a rs232 cable I plugged into a rs232 to usb converter. -PF
            self.connexion = serial.Serial(
                port='COM1',
                baudrate=38400,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
                ) 

            self.connexion.isOpen()
            # send the character to the device
            # (note that I append a \r\n carriage return and line feed to the characters - this is requested by my device)
            self.write(' ')
            out = ''
            # let's wait one second before reading output (let's give device time to answer)
            time.sleep(1)
            while self.connexion.inWaiting() > 0:
                out += self.connexion.read(1)
            if out != '':
                print ">>" + out 

    def get_status(self):
        if self.debug==False:     
            self.write('ST')
            return self.readline()

    def sync(self):
        if self.debug==False:  
            self.write('SYNC')
            return self.readline()

    def set_freq(self, chan, val):
        if self.debug==False: 
            self.write(str(chan) + 'FREQ ' + str(val))
            return self.readline()

    def set_freq_raw(self, chan, val):
        if self.debug==False: 
            self.write(str(chan) + 'RAW ' + str(val))
            return self.readline()

    def set_amp(self, chan, val):
        if self.debug==False: 
            self.write(str(chan) + 'AMP ' + str(val))
            return self.readline()

    def set_phase(self, chan, val):
        if self.debug==False: 
            self.write(str(chan) + 'PHASE ' + str(val))
            return self.readline()

    def set_DC(self, chan, val):
        if self.debug==False:  
            self.write(str(chan) + 'DC ' + str(val))
            return self.readline()  
    
    def write(self, stri):
        if self.debug == False:
            self.connexion.write(stri + '\r\n')            

    def readline(self):
        if self.debug==False:         

            return self.connexion.readline()
        
    def write_waveform(self, chan, wave):
        if self.debug == False:
            self.write(str(chan) + "K -32000")
            print (self.read2())
            addr = 0
            self.ser.flush()
            self.ser.flushInput()
            self.ser.flushOutput()
        
            while addr < 4096:
                piece = str(chan) + "B " + str(addr) + " "
                
                while addr < 4096 and len(piece + " " + hex(wave[addr])) < 1022 :
                    piece = piece + " " + hex(int(wave[addr]))
                    addr = addr + 1
                print piece    
                self.ser.flushInput()
                self.ser.flushOutput()
                self.write(piece)
                self.ser.flush()
                print (self.read2())
            
    
    def read2(self):
        if self.debug == False:
            ser = self.connexion
            time.sleep(0.5)
            out=''
            while ser.inWaiting() > 0:
                out += ser.read(1)
            return (out)

    #initialization should open it already    
    def reopen(self):
        if self.debug == False:
            self.ser.open()
        
