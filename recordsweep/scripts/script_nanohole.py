# -*- coding: utf-8 -*-
"""
Created on Tue May 21 21:38:20 2013

@author: Ben

This is a script to be used with DataTakerThread.py, part of the recordsweep.py
program. This example just loops until the thread is killed. It runs within 
the namespace of DataTakerThread.
"""
import alarm_toolbox as alarm
#import Tool

# available methods and variables:
# self.read_data() - reads instruments, returns values to GUI and checks if
#                    thread has been stopped
# self.log_file.write() - write something to the log file

#Decides whether we want to turn an alarm on or off on one instrument
#alarm_flags={}
#contain the time spend (in seconds) between two alarms for each instrument
#snooze_time={}
#contain the remaining time before the next alarm for each instrument, if no alarm status the value is set to -1

#snooze_timers={}
##change that later
#instr_id_names=[]
#
#for inst in self.active_instruments:
#    if inst!='TIME':
##        print inst
#        id_name=inst.ID_name
##        print id_name
#        snooze_timers[id_name]=-1
#        if not id_name in instr_id_names:
#            instr_id_names.append(id_name)

print "INIT DONE"
while self.isStopped() == False:
    

    print "---MEASURE SEQUENCE---"
 #self.alarm_manager(self.query_alarm())
#    try:
    self.read_data()
#    except:
#        self.stopped=True
#        self.error_visa=True
#    print "---MEASURE SEQUENCE DONE---"
    #look in the file alarm_settings.txt for instruments alarm settings, if found nothing set the flag to False
#
#    alarm_flags=alarm.set_flags(instr_id_names)
##    print alarm_flags
#    #look in the file alarm_settings.txt for instruments alarm settings, if found nothing set the timer
#    
#    snooze_time=alarm.get_snooze_time(instr_id_names)
##    print snooze_time
#    #look in the file alarm_settings.txt
#    mailinglist=alarm.get_settings('MAILING_LIST')   

#    print mailinglist
#    if len(mailinglist)==0:
#        print "The email alarm system is desactivated, to reactivate, please add a line MAILING_LIST=pfduc@physics.mcgill.ca;pierre-francois.duc@a3.epfl.ch into the alarm_settings.txt file"
#        print "If error occurs emails will be sent to the following recipients : ",mailinglist
    
#    print "---ALARM SEQUENCE---"
##    print snooze_timers
#    for inst in self.active_instruments: 
#        if inst!='TIME':
#            id_name=inst.ID_name
##            print id_name
#    #       self.instruments[inst].ID_name
#            #collect whatever the responses from the query alarm() of the instruments
#
#            alarm_stack=inst.query_alarm()
#
#            #self.active_instruments[inst].query_alarm()
##            print "you"
##            print len(alarm_stack)
#            curtime=time.time() - self.t_start
##            print "curtime ", curtime
##            print " logic... ",snooze_timers[id_name]==-1,snooze_timers[id_name]>curtime
# 
#            if snooze_timers[id_name]==-1 or snooze_timers[id_name]<curtime:
#                for al_h in alarm_stack:
##                    print id_name
##                    print al_h.get()
#                    alarm_status=al_h.manage(alarm_flags[id_name],mailinglist)
##                    print alarm_status
#                    if alarm_status:
#                        print "Timer was set until ", snooze_timers[id_name]
#                        print "It is now ",curtime
#                        print al_h.get()
#                        snooze_timers[id_name]=alarm.set_snooze_timer(alarm_status,snooze_time[id_name],curtime)
#                        print snooze_timers
#    print "---ALARM SEQUENCE DONE---"
    time.sleep(3)   