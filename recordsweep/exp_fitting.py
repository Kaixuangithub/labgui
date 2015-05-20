# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 16:41:55 2013

@author: pf
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.optimize
import IOTool as io


class data_set(object):
    def __init__(self,data,labels,bkg=None):
        print "a new data set"
        print labels
        self.labels=labels
        self.data=data
        self.params=labels['param']
        if 'Time' in self.params:
            self.t=data[:,self.params.index('Time')]
        if 'FLOW' in self.params:
            self.Q=data[:,self.params.index('FLOW')]  
        if 'PRESSURE' in self.params:
            self.P=data[:,self.params.index('PRESSURE')] 
        if 'TEMPERATURE' in self.params:
            self.T=data[:,self.params.index('TEMPERATURE')] 

        self.Qfit=None
        self.fitparam=None
        if not bkg:
            self.bkg_val={}
            for p in self.params:
                self.bkg_val[p]=0
        else:
            self.bkg_val=bkg
        print "This is the BKG values of parameters",self.bkg_val
        
    def subset(self,start,end,limtype='index'):
        if limtype=='index':
            return data_set(self.data[start:end,:],self.labels)
        elif limtype=='value':
            print self.match_value2index(start)
            print self.match_value2index(end)
#            return self
            return data_set(self.data[self.match_value2index(start):self.match_value2index(end),:],self.labels)
        else:
            return None
        
    def exp_decay(self,correct_bkg=False):
        
                
        
        A,K=fit_exp_nonlinear(self.t-self.t[0],self.Q-self.Q[0])        
        
#        A, K = fit_exp_linear(self.t,self.Q,self.Q[0])
        fig = plt.figure()
        ax1 = fig.add_subplot(2,1,1)
        if correct_bkg:
            fit = model_func(self.t-self.t[0], A, K)+self.Q[0]-self.bkg_val['flow']
            plot(ax1,self.t,self.Q,fit)
            self.fitparam=[A,K,self.Q[0]-self.bkg_val['flow']]
            self.Qfit=self.Q[0]+A-self.bkg_val['flow']
        else:
            fit = model_func(self.t-self.t[0], A, K)+self.Q[0]
            plot(ax1,self.t,self.Q,fit)
            self.fitparam=[A,K,self.Q[0]]
            self.Qfit=self.Q[0]+A

        print self.Qfit
        return self.Qfit
        
    def length(self):
        return np.size(self.data)
        
    def get_params(self,exptype=None):
        if exptype=='flow':
            return [np.average(self.P),np.average(self.T),self.t,self.Q]
        else:
            return self.data
        
    def get_fit_params(self,exptype=None):
        if exptype=='flow':
            return [self.Qfit,self.fitparam]
        else:
            return self.fitparam
        
    def set_background(self,param=None,bkg_val=0):
        if param in self.params:
            self.bkg_val[param]=bkg_val
        else:
            print "the parameter "+param+" is not in the list \n"
            print self.params
    
    def match_value2index(self,val,paramtype=None):
        print "val",val
        print self.t
        if val>self.t[len(self.t)-1]:
            val=self.t[len(self.t)-1]
        if val<self.t[0]:
            val=self.t[0]

        if not paramtype:
            if val in self.t:
                index=np.where(self.t==val)[0][0]
            else:
#                dt=self.t[1]-self.t[0]
                up=np.where(self.t>val)
#                print up
                index=up[0][0]
        else:
            print "match_value2index, parameter type defined but not implemented"
            index=-1
        print index
        return index

                #for i,t in enumerate(self.t):
                
            
        
    
    def display(self):
        fig = plt.figure(1)
        ax1 = fig.add_subplot(2,1,1)
        if self.fitparam:
            fit_y = model_func(self.t-self.t[0], self.fitparam[0], self.fitparam[1])+self.fitparam[2]
        else:
            fit_y=self.Q
        
        plot(ax1,self.t,self.Q,fit_y)

class experiment():
    def __init__(self,data=None,fname=None):
        self.data_sets=[]
        self.Q_bkg=0
        self.P_bkg=0
        if data:
            self.data_sets.append(data)
            self.active_set=self.data_sets[0]
        elif fname:
            self.load_raw_data(fname)
        else:
            self.active_set=None
        
    def create_set(self,start=None,end=None,limtype='index'):
        if not start:
            start=0
        if not end:
            end=self.active_set.length()
        new_data_set=self.active_set.subset(start,end,limtype)
        self.data_sets.append(new_data_set)
        self.active_set=new_data_set
        
    def remove_set(self):
        pass
        #not if the index is 0
        
    def change_raw_data(self,data):
        try:
            sets=self.data_sets.remove(self.data_sets[0])
            doloop=True
        except:
            doloop=False
        self.data_sets=[]
        self.data_sets.append(data)
        self.active_set=self.data_sets[0]
        if doloop:
            for s in sets:
                self.data_sets.append(s)
            
    def load_raw_data(self,fname):
        [data,labels]=io.load_file_windows(fname)
        print "load raw data"
        new_data_set=data_set(data,labels)
        self.change_raw_data(new_data_set)
    
    def get_nb_sets(self):
        
        return len(self.data_sets)        
        
    def get_active_set_index(self):
        return self.data_sets.index(self.active_set)
        
    def previous_data_set(self):
        
        i=self.get_active_set_index()
#        print "previous",i
        if i==0:
            i=self.get_nb_sets()
        self.active_set=self.data_sets[i-1]

    def next_data_set(self):
        i=self.get_active_set_index()
#        print "next",i
        if i==self.get_nb_sets()-1:
            i=-1
        self.active_set=self.data_sets[i+1]  
    
    def get_active_params(self,exptype=None):
        return self.active_set.get_params(exptype)
        
    def get_active_fit_params(self,exptype=None):
        return self.active_set.get_fit_params(exptype)
        
    def fit_active_data_set(self,correct_bkg=False):
        return self.active_set.exp_decay(correct_bkg)
        
    def correct_bkg(self,sets='active'):
        if sets=='active':
            self.active_set.correct_flow_background(self.Q_bkg)
            self.active_set.correct_pressure_background(self.P_bkg)
        elif sets=='all':
            pass
        else:
            pass
        
    def set_flow_bkg(self,Q_bkg):
        self.Q_bkg=Q_bkg
        
    def set_pressure_bkg(self,P_bkg):
        self.P_bkg=P_bkg
        
    def savefile(self,of):
        sets=self.data_sets.remove(self.data_sets[0])
        for s in sets:
            try:
                of.write(str(s.Qfit) +"\t"+str(s.Pav())+"\n")
            except:
                pass
            
    def display(self):
        pass
#        self.active_set.display()

def importfile(fname):
    
    a=0
    b=740
    data=np.loadtxt(fname)
    P=data[a:b,1]
    flow=data[a:b,2]
    time=data[a:b,3]
    ds=data_set(time,77,P,flow)
    ds2=ds.subset(130,400)
#    print ds2.P
    ds2.exp_decay()
#    Ppoints=[]
#    Qpoints=[]
#    tpoints=[]
##    dP=abs(np.diff(P))
#    tempP=[]
#    tempQ=[]
#    tempt=[]
#    dp_lim=0.0005
#    previous_index=0
#    for i,dp in enumerate(P):
#        av=av_diff(P,i,5)
#        
#        #the average derivative of P is smaller than the limit
#        if av <= dp_lim:
#            tempP.append(dp)
#            tempQ.append(flow[i])
#            tempt.append(time[i])
#            if i-previous_index>9:
#                Pressure=np.array(tempP)
##                print Pressure
#                Ppoints.append(np.average(Pressure))
#                Qpoints.append(tempQ)
#                tpoints.append(tempt)
#                tempP=[]
#                tempQ=[]
#                tempt=[]
#            previous_index=i
#    
#    Pf=np.array(Ppoints)
#    Qf=np.array(Qpoints)
#    tf=np.array(tpoints)
#    print Pf
    
def av_diff(P,i,di=3):
    if di>i:
        di=i
    if i==len(P)-1:
        di=0
    p=P[i-di:i+di]
    return np.average(abs(np.diff(p)))

def main():
    # Actual parameters
    A0, K0, C0 = 2.5, -4.0, 2.0

    # Generate some data based on these
    tmin, tmax = 0, 0.5
    num = 20
    t = np.linspace(tmin, tmax, num)
    y = model_func(t, A0, K0, C0)

    # Add noise
    noisy_y = y + 0.5 * (np.random.random(num) - 0.5)

    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)

    # Non-linear Fit
    A, K, C = fit_exp_nonlinear(t, noisy_y)
    fit_y = model_func(t, A, K, C)
    plot(ax1, t, y, noisy_y, fit_y, (A0, K0, C0), (A, K, C0))
    ax1.set_title('Non-linear Fit')

    # Linear Fit (Note that we have to provide the y-offset ("C") value!!
    A, K = fit_exp_linear(t, y, C0)
    fit_y = model_func(t, A, K, C0)
    plot(ax2, t, y, noisy_y, fit_y, (A0, K0, C0), (A, K, 0))
    ax2.set_title('Linear Fit')

    plt.show()

def model_func(t, A, K):
    return A * (1-np.exp(-(K * t)))

def fit_exp_linear(t, y, C=0):
    y = y - C
    y = np.log(y)
    K, A_log = np.polyfit(t-t[0], y, 1)
    A = np.exp(A_log)
    return A, K

def fit_exp_nonlinear(t, y):
    opt_parms, parm_cov = sp.optimize.curve_fit(model_func, t, y, maxfev=1000)
    A, K = opt_parms
    return A, K

def plot(ax, t, y, fit_y):
#    A0, K0, C0 = orig_parms
#    A, K, C = fit_parms

    real_data = ax.plot(t, y, 'k--')
#    obs_data = ax.plot(t, noisy_y, 'ro')
    fit_data = ax.plot(t, fit_y, 'b-')
#    ax.legend((real_data, fit_data),
#            ['Actual Function:y = '+str(round(A0,2))+' e^{'+str(round(K0,2))+' t} + '+str(round(C0,2)), 
#             'Fitted Function:y = '+str(round(A,2))+' e^{'+str(round(K,2))+' t} + '+str(round(C,2))], 
#            bbox_to_anchor=(1.05, 1.1), fancybox=True, shadow=True)
    plt.show()
if __name__ == '__main__':
    importfile('fitdata.txt')
