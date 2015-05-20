"""
Copyright (C) 10th april 2015 Benjamin Schmidt & Pierre-Francois Duc
License: see LICENSE.txt file
"""

import time
import os

def open_therm_file(config_file_name="config.txt"):
    """
        open the output file and autoincrement it, if it already exists 
    """
    file_name=get_file_name(config_file_name)
    
    n = 1
    #make sure the file doesn't already exist by incrementing the number
    while os.path.exists(file_name + "_%3.3d.dat"%n):
        n +=1
 
    out_file_name = file_name + "_%3.3d"%n 
    
    print "open output file: " + out_file_name + "in write mode"
    output_file = open(out_file_name,'w')
    return output_file, out_file_name

def get_file_name(config_file_name="config.txt"):
    """
        returns the filename of output file as it is in the config file
    """
    file_name="no CONFIG file"
    try:
        config_file = open(config_file_name)
        for line in config_file:
            [left,right] = line.split("=")
            left = left.strip()
            right = right.strip()
            if left == "COOLDOWN":
                cooldown = right
    #            print "cooldown " + cooldown
            elif left == "SAMPLE":    
                sample_name = right
    #            print "sample " + sample_name
            elif left == "THERM_PATH":
                therm_path = right
            elif left == "DATA_PATH":
                data_path = right
            elif left == "FILE_FORMAT":
                 file_name=eval(right)
                 

        try :
            file_name = data_path + sample_name + "_" + cooldown +"_"+time.strftime("%m%d")
            n = 1
            #make sure the file doesn't already exist by incrementing the number
            while os.path.exists(file_name + "_%3.3d.dat"%n):
                n +=1 
            file_name = file_name + "_%3.3d.dat"%n
        except:
            file_name="No output file choosen"
        
        config_file.close()
    except IOError as e:
        print "No configuration file "+config_file_name+"  found"

    return file_name


def get_config_setting(setting,config_file_name="config.txt"):
    """
        gets a setting from the configuration file
    """
    file_name=None
    try:
        config_file = open(config_file_name)
        
        for line in config_file:
            [left,right] = line.split("=")
            left = left.strip()
            right = right.strip()
            if left == setting:
                file_name = right
        if not file_name:
            print "Configuration file does not contain a'"+setting+"=' line."
            file_name="no %s file"%(setting)
        config_file.close()
    except IOError as e:
        print "No configuration file "+config_file_name+" found"
        file_name="no CONFIG file"
    return file_name

def get_settings_name():
    return get_config_setting("SETTINGS")

def get_script_name():
    return get_config_setting("SCRIPT")
   
def get_drivers_path():
    return get_config_setting("DRIVERS")
    
def get_debug_setting():
    setting=get_config_setting("DEBUG")
    if setting=='False':
        debug = False
    else:
        debug = True
    return debug


def get_drivers(drivers_path):
    """
        Returns the drivers names, their parameters and the corresponding 
        units of all drivers modules contained in a specified folder.
        The driver module needs to contain a class "Instrument" and a 
        dictionary "param" containing the different parameters and their units.
    """
    instruments=[]
    params={}
    units={}
#    instruments.append('TIME')
    params['']=[]
#    params['TIME']=[]
    
    if not (drivers_path=="no DRIVERS file" or drivers_path=="no CONFIG file"):
        #list all the .py files in the drivers folder
        for file_name in os.listdir(drivers_path):
            if file_name.endswith(".py") and not file_name=='Tool.py':
                name=file_name.split('.py')[0]
    #            print name
                #add to instruments list
                instruments.append(name)
                #import the module of the instrument
                driver=__import__(name)
                #create an array for the parameters
                params[name]=[]
                #load the parameters and their units from the module
                try:
                    for chan,u in driver.param.items():
                        units[chan]=u
                        params[name].append(chan)
                except:
                    print "Invalid driver file: " + file_name + " (no param variable found)"
    else:
        params['TIME']=[]
        print
        print "+"*10,"ERROR","+"*10
        print "You have to specify a path to your instuments drivers folder."
        print "Currently you are unable to load any instrument."
        print "To do so, create or edit a file named config.txt that should be in the same folder as your main program,"
        print "and create a line 'DRIVERS=path_to_your_driver_folder'."
        print "+"*10,"ERROR","+"*10
        print
    return [instruments,params,units]