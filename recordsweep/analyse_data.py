# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 16:07:25 2013

Copyright (C) 10th april 2015  Pierre-Francois Duc
License: see LICENSE.txt file
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.optimize
import IOTool as io
from Fitting import *

class DataSet(object):
    def __init__(self,data,labels,bkg=None):
#        print "a new data set"
#        print labels
        self.labels=labels
        self.data=data
        self.params=labels['param']   
        self.length= np.size(self.data,0)
        self.MAXINDEX=self.length-1

    def length(self):
        return np.size(self.data)
        
    def get_data(self,param=None):
        if param==None:
            return self.data
        else:
            if param in self.params:
                return self.data[:,self.params.index(param)]
            else:
#                print "analyse_data.DataSet.get_data the parameter you choosed is ",self.params[param], "\n"
                return self.data[:,param]
                
                
    def subset(self,start,end,param=None):
        
        if not start:
            start=0
        if not end:
            end=self.MAXINDEX

        if start>end:
            temp=end
            end=start
            start=temp
        
        if start<0:
            start=0
        if start>self.MAXINDEX:
            start=self.MAXINDEX
            
        if end<0:
            end=0
        if end>self.MAXINDEX:
            end=self.MAXINDEX   
            
        if param==None:
            return self.data[start:end,:]
        else:
            if param in self.params:
                return self.data[start:end,self.params.index(param)]
            else:
#                print "analyse_data.DataSet.subset the parameter you choosed is ",self.params[param], "\n"
                return self.data[start:end,param]

            
            
#        elif limtype=='value':
#            print self.match_value2index(start)
#            print self.match_value2index(end)
##            return self
#            return data_set(self.data[self.match_value2index(start):self.match_value2index(end),:],self.labels)
#        else:
#            return None

class DataSubset():
    """
    this class is defined to hold the information attached to a subset
    such as the indexes defining the subset from the set,the physical parameter
    and the fitting parameter.
    it prevents duplicating the data to each subsets
    """
    def __init__(self,indexes=None,fitparam=None,physparam=None,limparam=None):
        self.bounds=indexes
        if not fitparam==None:
            self.fitparam=fitparam
        else:
            self.fitparam=[]
        if not physparam==None:
            self.physparam=physparam
        else:
            self.physparam=[]
        if not limparam==None:
            self.limparam=limparam
        else:
            self.limparam=[]

    
def fit_exp_linear(t, y, C=0):
    y = y - C
    y = np.log(y)
    K, A_log = np.polyfit(t-t[0], y, 1)
    A = np.exp(A_log)
    return A, K

def fit_nonlinear(t, y,func_name=exp_decay,guess_param=None):
#    print "analyse_data.fit_nonlinear: function ",func_name.__name__
#    opt_parms, parm_cov = sp.optimize.curve_fit(func_name, t, y, maxfev=2000)
    return sp.optimize.curve_fit(func_name, t, y,p0=guess_param, maxfev=2000)
#    
#    if func_name.__name__=="exp_decay":
#        A, K =opt_parms
#        return opt_parms parm_cov
#    elif func_name.__name__=="exp_decay_down":
#        A, K, B =opt_parms
#        return A,K,parm_cov

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

#this IS actually a data set... I should make it inheritate

class live_experiment():
    def __init__(self):
        
        self.data_set=[]
        #the original data is stored in the index 0 of the array self.data_subset and have the value self.active_set set to -1
        self.data_subsets=[]        
        self.data_subsets.append(DataSubset(None))
        self.active_set=-1
        #this would be use to know when the fit is converging towards a stable value (especially useful for exponentials)
        self.main_fit_param=[]
#        print "LIVE_EXPERIMENT"
#    def __del__(self):
#        print "LIVE_EXPERIMENT DEAD"
    def update_data_set(self,data_set=None,fit_func=None,fit_params=None):
        """
        This method recieve the data stream and performs a fit on it based on the bounds given
        fit_params contains the information about which column is x and which one is y as well 
        as the x bounds.
        """
        if not data_set==None:
            self.data_set=data_set
            if not fit_func==None:
                x_bounds=[int(fit_params[2][0]),int(fit_params[2][1])]
                self.fit(fit_params[0],fit_params[1],fit_func,x_bounds)
        else:
            print "analyse_data.update_data_set() : there is no data set to change"

    def get_data(self):
        return self.data_set
        
    def get_subset_data(self,param=None,bounds=None):

        if not param==None:
            if not bounds==None:
                start=bounds[0]
                end=bounds[1]-1
                answer=np.array(self.data_set[start:end,param])
#                print answer
            else:
                answer=np.array(self.data_set[:,param])
        else:
            print "analyse_data.get_subset_data : the column of the data to select is not correct : ",param
            
        return answer
    
#to make this more robust to change we should inheritate from experiment and more specific experiment which will all have their specific way of dealing with this function
    def fit(self,paramX,paramY,fit_func,x_bounds=None):
        
        #Store for display on the widget
#        print "live_exp.fit: ", paramX,paramY,fit_func.func_name,x_bounds
        
#        print "live_exp.analyse_data.fit:",fit_func.func_name
        if fit_func.func_name=="exp_decay":
#            print "analyse_data.fit : active set :",self.active_set
            X=self.get_subset_data(paramX,x_bounds)
            Y=self.get_subset_data(paramY,x_bounds)
#            print X,Y
            guess_param=[(Y[len(Y)-1]-Y[0]),2./(np.max(X)-np.min(X))]
#            print "analyse_data.fit: guess parame ",guess_param
            [deltaY,tau],cov=fit_nonlinear(X-X[0],Y-Y[0],fit_func,guess_param)  
#            print "analyse_data.fit: variables ",deltaY,tau
#            print "analyse_data.live_exp.fit: covariant ",cov
            
            Q=Y[0]+deltaY
            
            try:
                T=np.average(self.get_subset_data('TEMPERATURE'))
            except:
                T=-1
#                print "analyse_data.fit:could not get average temperature for set number "+str(self.active_set)
            try:
                P=np.average(self.get_subset_data('PRESSURE'))                
            except:
                P=-1
#                print "analyse_data.fit:could not get average pressure for set number "+str(self.active_set)
          
            #Store for display and save later
            self.data_subsets[0].fitparam=[deltaY,tau,Y[0],X[0],cov[0,0]]
            self.data_subsets[0].physparam=[str(round(Q,12)),str(round(P,3)),str(round(T,2))]
            self.add_main_fit(Q)
#        elif fit_func.func_name=="integrate":
#            pass
        
        elif fit_func.func_name=="linear":
            X=self.get_subset_data(paramX)
            Y=self.get_subset_data(paramY)
            [m,h],cov=fit_nonlinear(X,Y,fit_func)  
#            print "analyse_data.fit: variables ",m,h
#            print "analyse_data.fit: covariant ",cov

            #Store for display and save later
            self.data_subsets[0].fitparam=[m,h,cov[0,0]]
            self.data_subsets[0].physparam=[m]
        else:
            
            X=self.get_subset_data(paramX)
            Y=self.get_subset_data(paramY)
#            print "I am in the else"
            fitp=fit_nonlinear(X,Y,fit_func)
#            print fitp
#            fparam_list=io.get_func_variables(self.fit_func)
#            fparam_list=fparam_list[1:]
#            print fitp[0],fitp[1]
            cov=fitp[1]
#            print cov
#            cov=cov[0][0]
            fitp=fitp[0]
#            print "analyse_data.fit: variables ",m,h
#            print "analyse_data.fit: covariant ",cov

            #Store for display and save later
#            print "self.data_subsets[0].fitparam=["+io.enumerate_arg_func("fitp",fitp)+",cov[0,0]]"
            exec("self.data_subsets[0].fitparam=["+io.enumerate_arg_func("fitp",fitp)+",cov[0,0]]")
            self.data_subsets[0].physparam=None
            
        #Store for display and save later   
        self.data_subsets[0].limparam=[x_bounds,X[0],X[-1]]
    def add_main_fit(self,main_fit):
        self.main_fit_param.append(main_fit)
        try:
            residual=(abs(self.main_fit_param[-1]-self.main_fit_param[-2]))/self.main_fit_param[-1]
            if residual<0.001:
                print "NOW the residual is low",residual
        except:
            pass
        
        
    def get_active_physparams(self):
            return self.data_subsets[0].physparam
#        
    def get_active_fit_params(self):
            return self.data_subsets[0].fitparam

    def get_active_lim_params(self):
            return self.data_subsets[0].limparam
                

class experiment():
    def __init__(self,fname=None,data=None,bkg=None):
        
#        self.bkg_val={}
#        self.has_bkg=False
        if data:
            self.data_set=data
#            self.data_set_bounds=[0,self.data_set.length]
            self.params=data.params
        elif fname:
            self.load_data_set(fname)
        else:
            self.data_set=None
#            self.data_set_bounds=None
            self.params=None
        
        #the original data is stored in the index 0 of the array self.data_subset and have the value self.active_set set to -1
        self.data_subsets=[]
        self.active_set=-1
        
#        if not bkg:
#            if self.params:
#                for p in self.params:
#                    self.bkg_val[p]=0
#        else:
#            self.bkg_val=bkg
#            self.has_bkg=True
#        print "This is the BKG values of parameters",self.bkg_val
#        print "LIVE_EXPERIMENT"
#    def __del__(self): 
#        print "EXPERIMENT DEAD"
    def load_data_set(self,fname):
        extension=fname.rsplit('.')[len(fname.rsplit('.'))-1]
        if extension=="adat":
            [data,labels]=io.load_file_windows(fname,'\t')
        elif extension=="adat2":
            [data,labels]=io.load_file_windows(fname)
        else:
            [data,labels]=io.load_file_windows(fname)
#        print "load data set "+fname
        new_data_set=DataSet(data,labels)
        self.change_data_set(new_data_set)  
    
    def load_data_subsets(self,fname):
        extension=fname.rsplit('.')[len(fname.rsplit('.'))-1]
        if extension=="aset":
            [data,labels]=io.load_aset_file(fname)
        else:
            print "analyse_data.load_data_subsets: wrong extensionfor the file ",fname,", should be '.aset' but it is '",extension,"'"
#        print "load data set "+fname
        new_data_set=data_set(data,labels)
        self.change_data_set(new_data_set)  
    
    def change_data_set(self,data=None):
#        print "analyse_data.change_data_set :",data.params
        if data:
            self.data_set=data
#            self.data_set_bounds=[0,self.data_set.length]
            self.params=data.params
#            for p in self.params:
#                    self.bkg_val[p]=0
            self.data_subsets=[]
            self.active_set=-1
        else:
            print "analyse_data.change_data_set() : there is no data set to change"
            
    def update_data_set(self,data_set=None):
        
        if not data_set==None:
            print "update data in experiment"
            self.data_set=data_set
#            self.data_set_bounds=[0,self.data_set.length]
        else:
            print "analyse_data.update_data_set() : there is no data set to change"
            
    def change_data_subsets(self,subsets=[]):
        self.data_subsets=subsets
        self.active_set=-1
    
    def create_subset(self,start=None,end=None,param=None):
        print "analyse_data.create_subset\n"
        if param==None:
            print "analyse_data.create_subset: you want to create a subset knowing the indexes"
            print "if not, you should specifiy a parameter in the list"
            print self.params
#        else:
#            start=self.match_value2index(start,param)
#            end=self.match_value2index(end,param)
        print "analyse_data.create_subset : start, end",start,", ",end    
        self.data_subsets.append(DataSubset([start,end]))
        self.active_set=len(self.data_subsets)-1
#        return [start,end]

    def remove_subset(self):
        if self.active_set==-1:
            pass
        else:
            self.data_subsets.remove(self.get_active_subset())
            self.active_set=self.active_set-1
        
    def get_data(self):        
        return self.data_set.get_data()
        
    def get_subset_data(self,param=None):
        if self.active_set==-1:
            return self.data_set.get_data(param)
        else:
            [start,end]=self.data_subsets[self.active_set].bounds
#            print "analyse_data.Experiment.get_subset_data", start,end
            return self.data_set.subset(start,end,param)
            
    def get_active_subset(self):
        if self.active_set==-1:
            return None
        else:
            return self.data_subsets[self.active_set]

    def previous_data_set(self):
        if self.active_set==-1:
            self.active_set=len(self.data_subsets)-1
        else:
            self.active_set=self.active_set-1

    def next_data_set(self):
        if self.active_set==len(self.data_subsets)-1:
            self.active_set=-1
        else:
            self.active_set=self.active_set+1
    
#to make this more robust to change we should inheritate from experiment and more specific experiment which will all have their specific way of dealing with this function
    def fit(self,paramX,paramY,fit_func,x_bounds=None):
    
        print "fit: ", paramX,paramY,fit_func.func_name,x_bounds
        
        if self.active_set==-1:
            print "analyse_data.fit: you cannot fit when you are in the raw data"
        else:
            print "analyse_data.fit:",fit_func.func_name
            if fit_func.func_name=="exp_decay":
                print "analyse_data.fit : active set :",self.active_set
                X=self.get_subset_data(paramX)
                Y=self.get_subset_data(paramY)
                guess_param=[(Y[len(Y)-1]-Y[0]),2./(np.max(X)-np.min(X))]
                print "analyse_data.fit: guess parame ",guess_param
                [deltaY,tau],cov=fit_nonlinear(X-X[0],Y-Y[0],fit_func,guess_param)  
                print "analyse_data.fit: variables ",deltaY,tau
                print "analyse_data.fit: covariant ",cov
                self.data_subsets[self.active_set].fitparam=[deltaY,tau,Y[0],X[0],cov[0,0]]
                Yfit=Y[0]+deltaY
                
                try:
                    T=np.average(self.get_subset_data('TEMPERATURE'))
                except:
                    T=-1
                    print "analyse_data.fit:could not get average temperature for set number "+str(self.active_set)
                try:
#                    if correct_bkg:
#                        P=np.average(self.get_subset_data('PRESSURE'))-self.bkg_val['PRESSURE']
#                    else:
                    P=np.average(self.get_subset_data('PRESSURE'))
                    
                except:
                    P=-1
                    print "analyse_data.fit:could not get average pressure for set number "+str(self.active_set)
                
                Q=Yfit
                self.data_subsets[self.active_set].physparam=[str(round(Q,12)),str(round(P,3)),str(round(T,2))]
            elif fit_func.func_name=="integrate":
                pass
            elif fit_func.func_name=="linear":
                X=self.get_subset_data(paramX)
                Y=self.get_subset_data(paramY)
                [m,h],cov=fit_nonlinear(X,Y,fit_func)  
                print "analyse_data.fit: variables ",m,h
                print "analyse_data.fit: covariant ",cov
                self.data_subsets[self.active_set].fitparam=[m,h,cov[0,0]]
                self.data_subsets[self.active_set].physparam=[m]
            self.data_subsets[self.active_set].limparam=[self.data_subsets[self.active_set].bounds,X[0],X[-1]]
                

        
        
    def get_active_physparams(self):
        if self.active_set==-1:
            return []
        else:
            return self.data_subsets[self.active_set].physparam
#        
    def get_active_fit_params(self):
        if self.active_set==-1:
            return []
        else:
            return self.data_subsets[self.active_set].fitparam
    
    def get_active_lim_params(self):
        if self.active_set==-1:
            return []
        else:
            return self.data_subsets[self.active_set].limparam
#    def correct_bkg(self,param=None,val=0):
#        self.has_bkg=True
#        if not param:
#            print "you should specifiy a parameter in the list"
#            print self.params 
#        else:
#            if param in self.params:
#                self.bkg_val[param]=val
#            else:
#                print "you should specifiy a parameter in the list"
#                print self.params 
                
    def savefile(self,of,save_subsets=False):
        print "saving"
  
        physp=self.data_subsets[0].physparam
        of.write("#P ")
        for p in physp:
            of.write(p+"\t")
        of.write("\n")
        for s in self.data_subsets:
            try:
                for p in s.physparam:
                    of.write(str(s.physparam[p])+"\t")
                of.write("\n")
                if save_subsets:
                    of.write(str(s.bounds).strip('[]')+"\n")
            except:
                pass     
            
    def saveset(self,of):
        print "saving sets"
  #here I should define the different parameters and the fit parameters
#        physp=self.data_subsets[0].physparam
#        of.write("#P ")
#        for p in physp:
#            of.write(p+"\t")
#        of.write("\n")
        for i,s in enumerate(self.data_subsets):
            try:
                of.write(str(s.bounds).strip('[]')+":")
                for p in s.physparam:
                    of.write(str(s.physparam[p])+"\t")
                of.write(":")
                print s.fitparam
                for p in s.fitparam:
                    of.write(str(p)+"\t")
                of.write("\n")
                
            except:
                pass     