# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 17:19:35 2013

@author: pfduc
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *
try:
    from PyQt4.QtCore import QString
except ImportError:
    QString = str

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    

try:
    import visa
except:
    print "you will need visa to use our drivers"

try:
    import serial
except:
    print "pyserial not available"

import numpy as np
    
import alarm_toolbox as alarm

import readconfigfile


old_visa = True
try:
    #soemthing that only exists in older versions of visa, as a probe for the version
    visa.term_chars_end_input
except:
    old_visa = False


 #Tobe moved into InstrumentHub class as this class should only be GUI
def refresh_device_port_list(): 
    """ Load hardware port list for use in combo boxes """       
    try:
        if old_visa:
            available_ports = visa.get_instruments_list()
        else:
            rm = visa.ResourceManager()
            available_ports = rm.list_resources()
    except:# visa.VisaIOError as e:
        #if e.error_code == -1073807343:
        
        available_ports = ["GPIB0::" +str(i) for i in range(30)]
    return available_ports

class MeasInstr(object):
    """
        this class defines a generic instrument to avoid having to redefine methods used in more than one instrument class.
        Any Instrument class of an instrument module driver should inherit from MeasInstr
        and the connectic should be defined only in MeasInstr.
        
        An MeasInstr has different channels or parameters one could measure or set
    """    
    
    
    #sould identify the instrument in a unique way        
    ID_name=None
    #store the pyvisa object connecting to the hardware
    connexion=None
    #debug mode trigger
    debug=None
    #contains the different channels availiable
    channels=[]
    #store the instrument last measure in the different channels
    last_measure={}
    #contains the units of the different channels
    units={}
    #contains the name of the different channels if the channels do not have explicit names
    channels_names={}
    
    
    #**keyw can be any of the following param "timeout", "term_chars","chunk_size", "lock","delay", "send_end","values_format","communication_protocole"
    #example inst=MeasInstr('GPIB0::0','Inst_name',True,timeout=12,term_char='\n')
    #other exemple inst=MeasInstr('GPIB0::0',timeout=12,term_char='\n')
    #"communication_protocole" can only take two values : "pyvisa" or "serial"
    def __init__(self,resource_name,name='default',debug_value=False,**keyw):
       
        self.ID_name=name
        self.debug=debug_value
        self.resource_name = resource_name

        if not old_visa:
            self.resource_manager = visa.ResourceManager()

        self.term_chars=""
        if keyw.has_key("communication_protocole"):
            self.communication_protocole=keyw["communication_protocole"]
            keyw.pop("communication_protocole")
        else:
            self.communication_protocole="pyvisa"
        #load the parameters and their unit for an instrument from the values contained in the global variable of the latter's module
        if name != 'default':
            module_name=__import__(name)
            self.channels=[]
            for chan,u in module_name.param.items():
        #initializes the first measured value to 0 and the channels' names 
                self.channels.append(chan)
                self.units[chan]=u
                self.last_measure[chan]=0
                self.channels_names[chan]=chan

        #establishs a connexion with the instrument
        self.connect(resource_name,**keyw)
#        print self.identify()

            
    def __del__(self):
        pass
        if not self.debug:
            self.close()
        # print "an instrument is dead, it's name was "+self.ID_name

    
    def identify(self,msg=''):
        """
            a function which calls the visa most common command to get back the instrument name
        """
        if not self.debug:
            return msg+self.ask('*IDN?')
        else:
            return msg+self.ID_name 

    def read(self,num_bytes=None):
        # Reads data available on the port (up to a term. char)
        if not self.debug:
            if self.communication_protocole=="pyvisa":
                answer=self.connexion.read()
            elif self.communication_protocole=="serial":
                if not num_bytes==None:
                    answer=self.connexion.read(num_bytes)
                else:
                    answer=self.connexion.readline()
                if answer[-1:]=='\n':
                    answer=answer[:-1]
        else:
            answer=None
        return answer

    def write(self,msg):
        # Writes a message but does not check for a response (non-query command)
        if not self.debug:      
            answer=self.connexion.write(msg+self.term_chars)
        else:
            answer=msg
        return answer
            
    def ask(self,msg):
        # Writes a message and reads the reply
        if not self.debug:
            if self.communication_protocole=="pyvisa":
                answer=self.connexion.ask(msg)
            elif self.communication_protocole=="serial":
                self.write(msg)
                answer=self.read()
        else:
            answer=msg
        return answer

    def connect(self,resource_name,**keyw):
        """
            this method establish the actual connexion with the instrument
        """
        for a in keyw:
            print a
        if not self.debug:    
            #if the instrument was already connected
            self.close();
            
            try:

                if self.communication_protocole=="pyvisa":
                    if old_visa:
                        self.connexion=visa.instrument(resource_name,**keyw)
                    else:
                        print "using new PyVisa > 1.4"
                        self.connexion=self.resource_manager.get_instrument(resource_name,**keyw)
                elif self.communication_protocole=="serial":
                    
                    #get rid of keyw who are not recongnized in serial
                    """
                    this part of the code was not tried for all possible combinaisons and they might be bugs if your situation is different than ours
                    """
                    if keyw.has_key("term_chars"):
                        self.term_chars=keyw["term_chars"]
                        keyw.pop("term_chars")
                    if keyw.has_key("baud_rate"):
                        baud_rate=keyw["baud_rate"]
                        keyw.pop("baud_rate")
                        self.connexion=serial.Serial(resource_name,baud_rate,**keyw)
                    else:
                        self.connexion=serial.Serial(resource_name)
                print "connected to "+str(resource_name)

            except:
                print self.ID_name +" is unable to connect to "+str(resource_name)
               
        
    def close(self):
        """
            close the connexion with the instrument
        """
        if not self.connexion==None:
            try:
                self.connexion.close()
#                print "disconnect "+self.ID_name
            except:
                pass
#                print "unable to disconnect  "+self.ID_name
        
    def clear(self):
        """
            clear the buffer of communication with the instrument
        """
        if not self.connexion==None:
            try:
                if self.communication_protocole=="pyvisa":
                    self.connexion.clear()
                    print "cleared "+self.ID_name
            except:
                print "unable to clear  "+self.ID_name
        
        
    def measure(self,channel):
        """
            define this method so any instrument has a defined method measure()
            and we can use polymorphisme : calling the method measure() will always
            work for a child instance of MeasInstr. Each child class should then redifine
            the method to send the commands to measure the different quantities of interest.
        """
        return None
        
    def query_alarm(self):
        """
            This method is a trial to implement an alarm scheme. For example if the reading of an instrument goes too high or too low
            you might want to be notified or take an action on the system. It worked for one case maybe it is worth going again through the code
            to pythonify it or simplify it more.
        """
        #the meaning of the values in bound is to be checked in the file in the function get_settings()
        #one might change that and feed the fname directely to the constructor... or to the query_alarm function     
        bounds=alarm.get_settings(self.ID_name)
        #if the bounds are empty there are no alarm to be set for this instrument
        if len(bounds)==0:
            return [alarm.alarm_handle(0,self.ID_name,"NoAlarmSet")]
        else:
            #store the different alarms output
            alarm_stack=[]        
            #go over each channel and compare the minand max value with the measured value
            for i,chan in enumerate(self.channels):
                #measured value
                value=self.last_measure[chan]
                #upper and lower bonds
                min_val=bounds[2*i];max_val=bounds[2*i+1]
                if min_val==None:min_val=-np.inf
                if max_val==None:max_val=np.inf
                #Channel name
                chan_name=self.channels_names[chan]

                if value>=min_val and value<=max_val:
                    alarm_record=alarm.alarm_handle(0,self.ID_name+"_"+chan_name,chan_name+" "+str(value)+self.units[chan])
                else:
                    if value<min_val:
                        alarm_record=alarm.alarm_handle(1,self.ID_name+"_"+chan_name,chan_name +" is below "+ str(min_val) + " : "+str(value)+self.units[chan]) 
                    if value>max_val:
                        alarm_record=alarm.alarm_handle(1,self.ID_name+"_"+chan_name,chan_name +" is above " + str(max_val) + " : "+str(value)+self.units[chan])
                alarm_stack.append(alarm_record)
            return alarm_stack        

class Spectroscope(MeasInstr):  
    """
        The reason this class is created is because spectroscope usually involve different
        schemes to retrieve data and they should be connected to a pyqtplot window (much higher refreshing speed than matplotlib)
        We haven't the use of that in our lab as we don't use much oscilloscope signals or CCD signals.
    """
    def __init__(self, resource_name,name, debug=False,**keyw): 
        super(Spectroscope, self).__init__(resource_name,name,debug,**keyw)
        
            
    def __del__(self):
        super(Spectroscope, self).__del__()

#------------------------------------------------------------------------------
    
    def acquire_spectrum(self,channel='FLOW'):
        print "aquire_spectrum"
#        if self.last_measure.has_key(channel): 
#            if not self.debug:
#                if channel=='FLOW':
#                    answer=self.ask('*READ:MBAR*L/S?')
#                else:
#                    answer=self.ask('*MEAS:P1:MBAR?')
#                answer=float(answer)
#            else: 
#                answer=100*random.random()
#            self.last_measure[channel]=answer
#        else:
#            print "you are trying to measure a non existent channel : " +channel
#            print "existing channels :", self.channels
#            answer=None
#        return answer



class InstrumentHub(QObject):
    """
        this class contains the list of instruments, their parameters and their port name for the connexion
    """
    def __init__(self,parent=None):
        super(InstrumentHub, self).__init__(parent)
        print "InstrumentHub created"
        
 
        self.debug=readconfigfile.get_debug_setting()

        # this will be the list of [GPIB address, parameter name] pairs        
        self.port_param_pairs = []

        self.instrument_list={}
        self.parameter_list=[]
        
    def __del__(self):
        self.clean_up()
        print "InstrumentHub deleted"
    
    def connect_hub(self,type_list, dev_list, param_list):
        """
            go through 3 lists (instrument type, port name, instrument parameter)
            and connect the instrument to the corresponding port name to measure the
            corresponding parameter.
        """
        #first close the connections and clear the lists
        self.clean_up()
        none_counter = 0
        
        for instr_name, device_port, param in zip(type_list, dev_list, param_list):
            self.connect_instrument(instr_name,device_port,param,False)
            self.emit(SIGNAL("changed_list()"))
#            if device_port in self.instrument_list:
#                # Another data channel already used this instrument - make
#                # sure it's the same type!!!
#                if instr_name != self.instrument_list[device_port].ID_name:
#                    print ("Same GPIB device_port specified for different instruments! ")
#                    print (device_port + " " + instr_name + " " + self.instrument_list[device_port].ID_name)
#                    instr_name = 'NONE'  
#            else:
#                if instr_name!='' and instr_name!= 'NONE':
#                    self.instrument_list[device_port] = self.connect_instrument(instr_name,device_port,self.debug)
#            
#            if instr_name!='' and instr_name!= 'NONE':
#                self.port_param_pairs.append([device_port, param])
#            else:
#                self.port_param_pairs.append([None, None])
#        print self.port_param_pairs
#
#        
#        self.emit(SIGNAL("changed_list()"))
        
    def connect_instrument(self,instr_name,device_port,param,send_signal=True):
        """
            connect the instrument to a port name to measure the a choosen parameter
        """
        #device_port should contain the name of the GPIB or the COM port
        class_inst=__import__(instr_name)
        if device_port in self.instrument_list:
            # Another data channel already use this instrument - make
            # sure it's the same type!!!
            if instr_name != self.instrument_list[device_port].ID_name:
                print ("You are trying to connect "+instr_name+" to the port "+ device_port)
                print ("But " + self.instrument_list[device_port].ID_name+ " is already connected to "+ device_port )
                instr_name = 'NONE'  
                send_signal=False
        else:
            if instr_name!='' and instr_name!= 'NONE':
                if instr_name=="TIME":
                    #TIME is a special type of instrument as no external connection is required because
                    #we use the computer clock to "measure" the time
                    obj=class_inst.Instrument()
                else:
                    obj=class_inst.Instrument(device_port,self.debug)
                self.instrument_list[device_port] = obj
        
        #I should have commented why I did this, I don't remember...
        #I think without that it was not working well
        if instr_name!='' and instr_name!= 'NONE':
            self.port_param_pairs.append([device_port, param])
        else:
            self.port_param_pairs.append([None, None])    
            
        #sends a signal to notify that the instrument hub list was modified
        if send_signal:
#            print "sending the signal"
            self.emit(SIGNAL("changed_list()"))
        

        
    """
    this is not pythonic and should be changed throughout the code where InstrumentHub is used
    """
    def get_instrument_list(self):
#        print "get_instrument_list",self.instrument_list
        return self.instrument_list      
   
    def get_parameter_list(self):
        return self.parameter_list    

    def get_port_param_pairs(self):
        return self.port_param_pairs 
    
    def get_instrument_nb(self):
        return len(self.port_param_pairs)
        
    def clean_up(self):
        """
            go through the connected instrument list and disconnect them,
            then reinitialize the lists
        """
        for key, inst in self.instrument_list.items():
            if key:
                inst.close()    
        self.instrument_list={}
        self.port_param_pairs=[]
        self.instrument_list[None] = None
    
#try to connect to all ports availiable and send *IDN? command
#this is something than can take some time
def whoisthere():
    if old_visa:
        port_addresses=visa.get_instruments_list()
    else:
        port_addresses=rm.list_resources()
        
    connexion_list={}
    for port in port_addresses:
        try:
            print port
            device=Tool.MeasInstr(port)
            device.connexion.timeout=0.5
#            print port +" OK"
            try:
                name=device.identify()
                connexion_list[port]=name
            except:
                pass

        except:
            pass
    return connexion_list
#    import types
#
#def str_to_class(field):
#    try:
#        identifier = getattr(sys.modules[__name__], field)
#    except AttributeError:
#        raise NameError("%s doesn't exist." % field)
#    if isinstance(identifier, (types.ClassType, types.TypeType)):
#        return identifier
#    raise TypeError("%s is not a class." % field)
        
if __name__=="__main__":
    
    pass
#DEBUGGING/UNDERSTANDING INHERITAGE CODE
#class MI_parent(object):
#    name='default'
#    def __init__(self,rename):
#        self.name=rename;
#        print "a new instrument was created it's name is "+self.name
#    
#    def __del__(self):
#        print " an instrument is dead, it's name was "+self.name
#
#
#class MI_child(MI_parent):
#    def __init__(self,rename):
#        super(MI_child,self).__init__(rename)
#        print "I am from MI_child"
#
#class A(object):
#    prop1=0
#    def __init__(self):
#        print "world"
#        self.idn()
#        self.prop1=1
#    def idn(self):
#        print "A"
#
#class B(A):
#    def __init__(self):
#        print "hello"
#        self.prop1=2
##        super(B,self).__init__()
#    def idn(self):
#        print "B"