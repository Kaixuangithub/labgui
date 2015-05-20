# -*- coding: utf-8 -*-
"""
Created on Tue May 29 14:28:29 2012
Lakeshore 332 Driver
@author: Bram
"""
try:
    import usb.core
except:
    print "usb.core not available"
import random
import numpy as np
import time
import Tool
from struct import pack,unpack
import warnings
import pylab as plt

param={'SPECTRE':'I','WAVELENGTH':'nm','PROUT':'pet'}

class Instrument(object):  

 
    def __init__(self, resource_name,debug=False):
        self.debug=debug
        self.identify()
        if not self.debug:            
            self.connect()
            self.initialize()
        
    def __del__(self):
#        self.dev.close_device(self.connexion)
        pass
    
    def initialize(self):
        self.nPixels=64
        """ send command 0x01 """
        self.write(pack('<B', 0x01))
        """ this command load one spectrum in the memory, one has to read it"""
        self.read_spectrum()
        print "initialization done"
#        self.query_information(1)
#        time.sleep(1)
#        self.write(pack('<BB', 0x05, 1))
#        print self.read(0x87)
        
#        print 
        self.wl_factors = [float(self.query_information(i)) for i in range(1,5)]
        self.nl_factors = [float(self.query_information(i)) for i in range(6,14)]
        """
        lambda=C0+C1*p+C2*p^2+C3*p^3
        """
        self.wl = sum( self.wl_factors[i]*np.arange(self.nPixels*self.nPixels/2., dtype=np.float64)**i for i in range(4) )   
        
        
        print len(self.wl)
        self.integration_time=3
#        self.valid_pixels=slice(26, 2048)
#        print self.wl[self.valid_pixels]
#        print len(self.wl[self.valid_pixels])
        
        
    def identify(self):
        print "hello this is USB2000"
        if self.debug:
            print "DEBUG mode"
        
    def connect(self, model="USB2000"):

#        if model not in _OOModelConfig.keys():
#            raise _OOError('Unkown OceanOptics spectrometer model: %s' % model)

        vendorId= 9303
        productId = [4098]
        self._EPout = 0x02# _OOModelConfig[model]['EPout']
        self._EPin = 0x82#_OOModelConfig[model]['EPin0']
#        self._EPin1 = _OOModelConfig[model]['EPin1']
        self._EPin_size = 64#_OOModelConfig[model]['EPin0_size']
#        self._EPin_size = 64#_OOModelConfig[model]['EPin1_size']
        devices = usb.core.find(find_all=True,
                        custom_match=lambda d: (d.idVendor==vendorId and
                                                d.idProduct in productId))
        # FIXME: generator fix
        devices = list(devices)
        print "dev",devices

        try:
            self.connexion = devices.pop(0)
        except (AttributeError, IndexError):
            print "Could not connect USB2000"
#            raise _OOError('No OceanOptics %s spectrometer found!' % model)
        else:
            if devices:
                warnings.warn('Currently the first device matching the '
                              'Vendor/Product id is used')
      #this might be buggy, they might be a way to interface better
        self.connexion.set_configuration()
        self._USBTIMEOUT = self.connexion.default_timeout * 1e-3

    def write(self, data, epo=None):
        """ helper """
        if epo is None:
            epo = self._EPout
        self.connexion.write(epo, data)

    def read(self, epi=None, epi_size=None):
        """ helper """
        if epi is None:
            epi = self._EPin
        if epi_size is None:
            epi_size = self._EPin_size
        return self.connexion.read(epi, epi_size)

    def ask(self, data, epo=None, epi=None, epi_size=None):
        """ helper """
        self.write(data, epo)
#        time.sleep(0.5)
        return self.read(epi, epi_size) 
        
    def close(self):
        pass
#        self.connexion.close_device(self.connexion)
#        pass
        
    def query_information(self, address, raw=False):
        """ send command 0x05 """
        self.write(pack('<BB', 0x05, int(address)))
        ret=self.read(0x87)
        if bool(raw): 
            return ret
        if ret[0] != 0x05 or ret[1] != int(address)%0xFF:
            print 'query_information: Wrong answer'
        answer=ret[2:ret[2:].index(0)+2].tostring()
#        print "QI",answer
        return answer         
        
    def query_status(self):
        """send command 0xFE"""
        pass
#        self.write(pack('<I',0xFE),epo=0x02, epi=0x87,epi_size=16)
#        print ret
        
    def set_integration_time(self,t):
        if t>=3 and t<=65535:
            print "changed integration time"
            self.write(pack('<BII', 0x02, int(t),int(t)),0x07)
            self.integration_time=t
        else:
            print "please provide an integration time between 3us and 65535us, your time was of %.ius"%(t)
            
    def read_spectrum(self):
        print "Reading spectrum"
        spectrum=np.array([])
        for i in range(self.nPixels):
#            print i
            ret=self.read()
            spectrum_line =  unpack('<'+'B'*self.nPixels, ret)
#            print spectrum_line
            if np.mod(i,2)==0:
                spectrum=np.append(spectrum,spectrum_line)
            
        ret2=self.read(0x82,1)
        print ret2
        
        self.last_measure=spectrum
        return spectrum
        
    def trigger_spectrum(self):
        self.write(pack('<B', 0x09))
        
    def acquire_spectrum(self):
        self.trigger_spectrum()
        time.sleep(self.integration_time*1e-6)
        return self.read_spectrum()
        
    def plot_spectrum(self):
        plt.plot(self.wl,self.last_measure)
        plt.grid(True)
        plt.show()
    def measure(self,channel=None):
        print "execute measure"
#        if self.last_measure.has_key(channel):
#            if not self.debug:
#                if channel=='A': 
#                    answer=float(self.ask('KRDG?'+channel)) #read in kOhm
#                if channel=='B': 
#                    answer=float(self.ask('KRDG?'+channel)) #read in kOhm
#
#            else:
#                answer=random.random()
#            self.last_measure[channel]=answer
#        else:
#            print "you are trying to measure a non existent channel : " +channel
#            print "existing channels :", self.channels
#            answer=None
#        return answer

if (__name__ == '__main__'):
    i=Instrument(1,False)
#    i.plot_spectrum()
#    i.set_integration_time(1000)
#
    print i.acquire_spectrum()
    print i.acquire_spectrum()
    try:
        i.write(pack('<I',0xFE),epo=0x07)
        print i.read(epi=0x87,epi_size=16)
    except:
        print "it failed"

#        i.connexion.clear_halt(0x82)
#    i.query_status()
#    a=array('B', [105])
#    data=np.loadtxt("my_data2")
#    print ["B",data[0]]
#    print unpack("<"+"I"*16,data[0])
#    i.plot_spectrum()
#    i.identify()
#    i.measure()
#    print slice(26, 2048)
#    print "prout"