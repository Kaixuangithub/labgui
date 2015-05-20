# -*- coding: utf-8 -*-
"""
Created on Tue Nov 05 04:59:28 2013

Copyright (C) 10th april 2015 Benjamin Schmidt & Pierre-Francois Duc
License: see LICENSE.txt file
"""

import numpy as np
import scipy.io
from importlib import import_module


def load_file_linux(fname,splitchar='\t'):
    """
    This one is for Linux
    """
    instr=open(fname,'r')
    data=[]
    for dat in instr:
        if dat[0]!="#":
            lines=dat.split(splitchar)
            nrow=0
            row=[]
            for el in lines:
                nrow=nrow+1
#                print el
                row.append(float(el))

            data.append(row)
    data=np.array(data)
#    data.reshape(nrow,ncolumn)#,nrow)
    return data

def load_file_windows(fname,splitchar=' ',headers=True):
    """
    This one is for Window
    """
    str(fname)
    instr=open(fname,'r')
    data=[]
    label={}
    row_length=0
    for i,dat in enumerate(instr):
#        print dat
        if dat[0]!="#":
            lines=dat.split('\r')
            nrow=0
            
            for el in lines:
#                print el
                nrow=nrow+1
                mes=el.split(splitchar)
                ncolumn=0
                row=[]
                for p in mes:
#                    print p
#                    print p
                    ncolumn=ncolumn+1
                    try:
                        row.append(float(p))
                    except:
                        pass
                if row_length==0:
                    row_length=len(row)
                if len(row)==row_length:
                    data.append(row)
                else:
                    print "IOTools.load_file_windows : line",i," skipped"
        else:
            label_id=dat[1:2]
            
            dat=dat[2:len(dat)].replace("'","")
            dat=dat.strip("\n")
            print "IOTools.load_file_windows : labels",dat
            if label_id=='P':
                if splitchar=='\t':
                    dat=dat.strip('\t')
                    print "IOTools.load_file_windows : labels",dat
                    label['param']=dat.split(splitchar)
                else:
                    label['param']=dat.split(', ')
            elif label_id=='I':
                label['instr']=dat.split(', ')
            
    data=np.array(data)
#    data.reshape(nrow,ncolumn)#,nrow)

    if headers:
        if len(label)==0:
            print "IOTools.load_file_windows : #P or #I headers are missing, all lines starting with # will be ignored"  
        return data,label
    else:
        return data

def load_pset_file(fname,labels=None,splitchar=' '):
    """
        gets the channels ticks for a plot
    """
    fname=str(fname)
    if not fname.find('.')==-1:
        fname=fname[0:fname.find('.')]+'.pset'
    
    all_ticks=[]
    for setting in ['X','YL','YR']:
#        print "set",setting
        ticks=[]
        try:
            pset_file = open(fname)
            for line in pset_file:
                [left,right] = line.split("=")
                left = left.strip()
                right = right.strip()
#                print left
                if left == setting:
#                    print right
                    ticks=(right.split(','))
                    
            pset_file.close()
        except IOError as e:
            print "IOTool.load_pset_file : No file "+fname+"  found"
            
        if labels:
            for i,t in enumerate(ticks):
                if t in labels:
                   ticks[i]=labels.index(t)
                else:
                    print "\n the tick "+" does not correspond to a label in the list"
                    print labels
                    print "\n"
        if setting=='X':
            if len(ticks):
                ticks=ticks[0]
            else:
                ticks=''
        all_ticks.append(ticks)
        
    
    return all_ticks

def load_aset_file(fname,splitchar=':'):
    """
    This one is for Window
    """
    instr=open(fname,'r')
    bounds=[]
    physparam=[]
    fitparam=[]
    physparam_val=[]
    fitparam_val=[]
#    label={}
    for dat in instr:
#        print dat
        if dat[0]!="#":
#            print dat
            
            lines=dat.strip('\n')
            lines=lines.split(splitchar)
#            print lines
            bounds.append(lines[0].split(','))
            physparam_val.append(lines[1].strip('\t').split('\t'))
            fitparam_val.append(lines[2].strip('\t').split('\t'))
        else:
            lines=dat[1:len(dat)-1].strip('\n')
            lines=lines.split(splitchar)
            physparam.append(lines[0].strip('\t').split('\t'))
            fitparam.append(lines[1].strip('\t').split('\t'))
#            for i,el in enumerate(lines):
#                if not el=='':
#                    lines[i]=float(el)
#            lines=lines[0:len(lines)-1]
#            print lines
#            nrow=0
#    print bounds,physparam_val,fitparam
    return bounds,physparam_val,fitparam_val,physparam,fitparam

def load_adat_file(fname,splitchar=' '):
    """
    This one is for Window
    """
    instr=open(fname,'r')
    data=[]
#    label={}
    for dat in instr:
#        print dat
        if dat[0]!="#":
#            print dat
            
            lines=dat.strip('\n')
            lines=lines.split('\t')
            
            for i,el in enumerate(lines):
                if not el=='':
                    lines[i]=float(el)
            lines=lines[0:len(lines)-1]
            print lines
#            nrow=0
            
#            for el in lines:
##                print el
#                nrow=nrow+1
#                mes=el.split(splitchar)
#                ncolumn=0
#                row=[]
#                for p in mes:
##                    print p
##                    print p
#                    ncolumn=ncolumn+1
#                    try:
#                        row.append(float(p))
#                    except:
#                        pass
            data.append(lines)
        else:
            dat=dat[1:len(dat)].replace("'","")
            dat=dat.strip("\n")
            line=dat.split(' ')
#            print line
            param_id=line[0]
            
            if param_id=='BKG_P':
                B_P=line[1].split('\t')
            elif param_id=='BKG_V':
                B_V=line[1].split('\t')
            elif param_id=='P':
                P=line[1].split('\t')
    
    parameters={}
    for bp,bv,p in zip(B_P,B_V,P):
        if not bp=='':
            parameters[bp]=bv
    print parameters        
    data=np.array(data)
    data[:,0]=data[:,0]-float(B_V[0])
    data[:,1]=data[:,1]-float(B_V[1])
    print "the background values are substracted"
    return data
#    data.reshape(nrow,ncolumn)#,nrow)

def list_module_func(module_name):
    my_module=import_module(module_name)
    all_funcs=dir(my_module)
    my_funcs=[]
    for func in all_funcs:
#        print func
#        print func[0:2]
        #discriminate the function that have __ in front of them
        if not func[0:2]=="__":
            my_funcs.append(func)
    return my_funcs

def import_module_func(module_name,func_name):
    my_module=import_module(module_name)
    return getattr(my_module,func_name)
    
def get_func_variables(my_func):
#    print my_func.func_code.co_varnames
    return my_func.func_code.co_varnames

def save_matrix(M):
    np.savetxt('matrix.dat',M)
#    scipy.io.savemat('matrix.mat',mdict={'out': M},oned_as='row')

def match_value2index(array1D,val):
    """
    this function will find the index of a value in an array
    if there is no match it will return the index of the closest value
    """

    my_array=array1D
    Nmax=len(my_array)-1
    
    if val>my_array[Nmax]:
        index=Nmax
    elif val<my_array[0]:
        index=0
    else:
        if val in my_array:
            index=np.where(my_array==val)[0][0]
        else:
            index=np.where(my_array>val)[0][0]
            if not index:
                index=max(np.where(my_array<val)[0])
    return index
    
    
if __name__=="__main__":
    
    [data,l]=load_file_windows("fitdata.txt")    
    print data
#    print l['param']
#    print load_pset_file('fitdata.pset')#,['dt','e','Flow','T','Ta','r','Tb','M','ert'])
#    print load_aset_file('140212_B22_B2_LHe_cell_77K_Knusden_descente.aset')
#    Qv=[1,2,3,4]
#    P=[-1,-2,-3]    
#    
#    M=[]
#    for i,q in enumerate(Qv):
#        N=[]
#        for j,p in enumerate(P):
##            dp=data_point(q,p,T,298,A)
#            N.append(q*p)
##        N=np.array(N)
#        M.append(N)
##    M=np.array(N)
#    print M
#    
#    save_matrix(M)
    
#    E = scipy.io.loadmat('matrix.mat')
#    print E