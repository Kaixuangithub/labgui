# -*- coding: utf-8 -*-
"""
Created on Wed Sep 05 14:21:56 2012

Copyright (C) 10th april 2015 Pierre-Francois Duc
License: see LICENSE.txt file
"""
import smtplib
#import string

def send(msg,sendto):
   # msg = {'FROM':'pfduc@physics.mcgill.ca', 'TO':'pfduc@physics.mcgill.ca', 'SUBJECT': 'hi', 'HOST': 'mailhost.mcgill.ca', 'BODY': 'testing'}
    #print "Sending message"
    
  #  sendto= {'pfduc87@gmail.com','pfduc@physics.mcgill.ca','lephysicien@gmail.com'}
    body= msg
    #BODY = string.join((
    #	"From: %s" % msg['FROM'],
    #	"To: %s" % msg['TO'],
    #	"Subject: %s" % msg['SUBJECT'] ,
    #	"",
    #	msg['BODY']
    #	), "\r\n")
    host='mailhost.mcgill.ca'
    

    #print 'Sending a message from '+ host
    server = smtplib.SMTP(host)
    #print server
   # print body
    error_sendmail=server.sendmail('OneKPotIsTooHot@mail.mcgill.ca',sendto,body)
    server.quit()
    print 'If the following brakets is empty it means the temperature alert was sent without a problem'
    print error_sendmail