# -*- coding: utf-8 -*-
"""
Created on Mon May 18 11:40:11 2015

@author: pfduc

This script should provide you with a simple example of inheritance main features

"""

class MI_parent(object):
    name='default'
    def __init__(self,rename):
        self.name=rename;
        print("a new instrument was created it's name is "+self.name)
    
    def __del__(self):
        print(" an instrument is dead, it's name was "+self.name)


class MI_child(MI_parent):
    def __init__(self,rename):
        super(MI_child,self).__init__(rename)
        print("I am from MI_child")

class A(object):
    prop1=0
    def __init__(self):
        print("world")
        self.idn()
        self.prop1=1
    def idn(self):
        print("The ID of this object is : A")

class B(A):
    def __init__(self):
        print("hello")
        self.prop1=2
    def idn(self):
        print("The ID of this object is : B")
      
class B2(A):
    def __init__(self):
        print("hello")
        self.prop1=2.5
        super(B2,self).__init__()
    def idn(self):
        print("The ID of this object is : B2")      

class B3(A):
    def __init__(self):
        print("hello")
        super(B3,self).__init__()
        self.prop1=2.5       
      
        
class C(A):
    def __init__(self):
        print("goodbye")
        self.prop1=3
    def idn(self):
        print("The ID of this object is : C")
    
if __name__ == "__main__":
    
    tab=[]    
    
    print("@: I create a instance of class A, upon initialization it calls its method idn and attributes the value 1.0 to the attribute prop1:")
    myobj=A()
    tab.append(myobj)
    print("The value of my property is : %.1f"%(myobj.prop1))
    print("#"*10)
    print("@: I create a instance of class B, children of class A, upon initialization it doesn't calls its method idn and attributes the value 2.0 to the attribute prop1:")
    myobj=B()
    tab.append(myobj)
    print("The value of my property is : %.1f"%(myobj.prop1))
    print("#"*10)
    print("@: I create a instance of class B2, also children of A, upon initialization it attributes the value 2.5 to the attribute prop1 and then it calls its parent class __init__ method which itself call idn method :")    
    myobj=B2()
    tab.append(myobj)
    print("The value of my property is : %.1f"%(myobj.prop1))
    print("@: because I called the __init__ method of the parent after attributing a value to prop1 the parent __init__ attribute it the value 1.0 :")    
    
    print("#"*10)
    myobj=B3()
    tab.append(myobj)
    print("The value of my property is : %.1f"%(myobj.prop1))
    
    print("@: because I haven't redefined the method idn, it will take the one from the parent class, that is why the type says the object is of ID A. Note that because we attribute the value to the attribute prop1 after we call the method __init__ of the parent class it has a different value from 1.")
    
    print("#"*10)
    print("@: I filled an array which object from different classes an call their function idn:")
    tab.append(C())
    for e in tab:
        e.idn()