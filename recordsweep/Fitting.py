# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 17:50:48 2014

@author: pf
"""

from numpy import exp as __exp
#from numpy import cos as __cos
from numpy import float64 as __float64
from numpy import array as __array
#import numpy as np

#np.float32()
def exp_decay(t, A, K):
    t=__array(t,dtype=__float64)
    return A * (1-__exp(-(K * t),))

def exp_decay_down(t, A, K, B):
    t=__array(t,dtype=__float64)
    return -A + B*__exp(-(K * t))

def integrate(x,Y):
    pass

def linear(x,m,h):
    x=__array(x,dtype=__float64)
    return m*x+h

def linear_fit(x,m,h):
    x=__array(x,dtype=__float64)
    return m*x+h
#
#def personalfunc(x,A,omega,phi):
#    x=__array(x,dtype=__float64)
#    return A*(omega*x+phi)