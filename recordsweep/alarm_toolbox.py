# -*- coding: utf-8 -*-
"""
Created on Tue May 29 14:28:29 2012
read alarmfile
@author: PF

"""
import smtplib
    


class alarm_handle():
    error_code=0
    tag=''
    msg=''
    __mailinglist=''
    
    def __init__(self,e=0,t='unknown_instrument',m='NoAlarmSet'):
#        print "handle born"
        self.error_code=e
        self.tag=t
        self.msg=m
  
    def __del__(self):
        pass
        #print "handle dead"
    
    def get(self):
        return [self.error_code,self.tag,self.msg]
    
    def set_mailing_list(self,mailinglist=None):
        if mailinglist==None:
            self.__mailinglist=get_settings('MAILING_LIST')
        else:
            self.__mailinglist=mailinglist
        
    def get_mailing_list(self):
        return self.__mailinglist
        
    def manage(self,activated=False,mailinglist=None):
        if activated:
#            print "alarm activated"
            if self.error_code:
                self.set_mailing_list(mailinglist)
                print "ALAAAAAAARM "+self.tag +" "+ self.msg
                send_email(self.msg,self.__mailinglist,self.tag)
            else:
                pass
#                print "Rien "+self.msg
        else:
            pass
#            print "alarm desactivated"
        return self.error_code

        


def get_settings(instr_label=None,fname="alarm_settings.txt"):
    """#return the alarm settings from the file fname(=alarm_setting.txt) provided an instrument label"""
    try:
        alarm_file = open(fname)
    except:
        print "could not open the file "+ fname
    settings=[]
    alarm_flags={}
    snooze_default=3600
    snooze_timers={}
    #read each line of the file except the one starting with #
    for line in alarm_file:
        #strip() gets rid of the space before and after the text
        line = line.strip()
        if line[0] != '#' and line[0]!='@':
            temp=line.split('=')
            #there is only an instrument name
            if len(temp)==1:
                temp=temp[0]
                print temp
                if temp!='MAILING_LIST':
                    alarm_flags[temp]=False
                    
            #there are parameter(s)
            else:
                [left,right] = temp
                left = left.strip()
                right = right.strip()
                if left == instr_label:
                    if instr_label=='MAILING_LIST':
                        settings = right.split(';')
                    else:
                        param=right.split('@SNOOZE')
                        if len(param)==2:
                            [right,snooze]=param
                            right=right.strip()
                        if right!='':
                            presettings = right.split(';')
                            for setting in presettings:
                                if setting=='':
                                    settings.append(None)
                                else:
                                    settings.append(float(setting))
                elif instr_label==None:
                    if left!='MAILING_LIST':
                        alarm_flags[left]=True
                elif instr_label=='SNOOZE':
                #check if there is a snooze input
                        param=right.split('@'+instr_label)
                        if len(param)==2:
                            snooze=param[1].strip()
                            if snooze!='':
                                snooze_timers[left]=float(snooze)
#                                print "Snooze for "+left + " : " +snooze
        else:
            if line[0]=='@' and instr_label=='SNOOZE':
                param=line.split('@'+instr_label)
                if len(param)==2:
                    snooze=param[1].strip()
                    if snooze!='':
                        snooze_default=float(snooze)
#                        print "Snooze default : " +snooze
                            
    alarm_file.close()
    if instr_label==None:
        settings=alarm_flags
    elif instr_label=='SNOOZE':
        settings=[snooze_timers, snooze_default]
    return settings

def set_flags(instrument_list,flag_list=None):
    if flag_list==None:
        flag_list=get_settings()
    
    for inst in instrument_list:
        if not flag_list.has_key(inst):
            flag_list[inst]=False
    temp=[]
    for flag in flag_list:
        if not flag in instrument_list:
            temp.append(flag)
    for flag in temp:
        flag_list.pop(flag)
    return flag_list
    
def get_snooze_time(instrument_list):
    [snooze_list,snooze_default]=get_settings('SNOOZE')    
    
    for inst in instrument_list:
        if not snooze_list.has_key(inst):
            snooze_list[inst]=snooze_default
    
    temp=[]
    for flag in snooze_list:
        if not flag in instrument_list:
            temp.append(flag)
    
    for flag in temp:
        snooze_list.pop(flag)
    
    return snooze_list
    
    
def set_snooze_timer(alarm_flag,snoozetime,currenttime=0):
    if alarm_flag:
        #ALARME il y a eu, on active le snooze
        timer=currenttime+snoozetime
  
    else:
        #il n'y a pas d'alarme, on veut desactiver le snooze
        timer=-1
#    print "le timer est "+str(timer)
    return timer
        
def send_email(msg,sendto,alarm_tag):
    if sendto!=[]:
        #as the information is contained is the alarm_tag, the sender address might as well be always the same
        sender='alarms@physics.mcgill.ca'
    
        #build the message so it will be nicely diplayed in the email box
        body = "\r\n".join([
        	"From: %s" % sender,
        	"To: %s" % sendto,
        	"Subject: %s" % alarm_tag ,
        	"",
         msg
        	])
    
        #connect to the host server  
        host='mailhost.mcgill.ca'
        server = smtplib.SMTP(host)
        
        try:
            error_sendmail=server.sendmail(sender, sendto, body)
        except:
            print "Email not sent"
            print error_sendmail
                
        server.quit()    