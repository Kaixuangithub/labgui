# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 14:58:03 2013

Copyright (C) 10th april 2015 Benjamin Schmidt
License: see LICENSE.txt file
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import readconfigfile
import re

class StartWidget(QWidget):
    
    def __init__(self, parent = None):
        super(StartWidget, self).__init__(parent) 
        
        
        #main layout of the form is the verticallayout
        
        self.verticalLayout = QVBoxLayout()      
        self.verticalLayout.setObjectName("verticalLayout")

        self.scriptLayout = QHBoxLayout()

        self.verticalLayout.setObjectName("scriptLayout")
        self.scriptFileLabel = QLabel (self)
        self.scriptFileLabel.setText("Script to run:")
        self.scriptFileLineEdit = QLineEdit(self)
        self.scriptFileButton = QPushButton(self)
        self.scriptFileButton.setText("Browse")
        self.scriptLayout.addWidget(self.scriptFileLabel)
        self.scriptLayout.addWidget(self.scriptFileLineEdit)
        self.scriptLayout.addWidget(self.scriptFileButton)
        self.verticalLayout.addLayout(self.scriptLayout)

        self.outputLayout = QHBoxLayout()
        self.outputLayout.setObjectName("outputLayout")
        self.outputFileLabel = QLabel (self)
        self.outputFileLabel.setText("Output File:")
        self.outputFileLineEdit = QLineEdit(self)
        self.outputFileButton = QPushButton(self)
        self.outputFileButton.setText("Browse")
        self.outputLayout.addWidget(self.outputFileLabel)
        self.outputLayout.addWidget(self.outputFileLineEdit)
        self.outputLayout.addWidget(self.outputFileButton)
        self.verticalLayout.addLayout(self.outputLayout)
        
        self.headerTextEdit = QTextEdit("")       
        self.verticalLayout.addWidget(self.headerTextEdit)
        
        self.startStopButton = QPushButton(parent = self)
        self.startStopButton.setText("Start!")
        self.verticalLayout.addWidget(self.startStopButton)
               
        spacerItem = QSpacerItem(20, 183, QSizePolicy.Minimum, QSizePolicy.Expanding)        
        self.verticalLayout.addItem(spacerItem)   
  
        self.setLayout(self.verticalLayout)
                        
        self.outputFileLineEdit.setText(readconfigfile.get_file_name()) 
        
        self.scriptFileLineEdit.setText(readconfigfile.get_script_name())
        
        #make the magic function names/decorators work!
        #self.retranslateUi(StartWidget)
        self.connect(self.outputFileButton,SIGNAL('clicked()'),self.on_outputFileButton_clicked)
        self.connect(self.scriptFileButton,SIGNAL('clicked()'),self.on_scriptFileButton_clicked)


        
    def on_outputFileButton_clicked(self):
        fname = str(QFileDialog.getSaveFileName(self, 'Save output file as', 
                                                self.outputFileLineEdit.text()))
        if fname:
            self.outputFileLineEdit.setText(fname)        

    def on_scriptFileButton_clicked(self):
        fname = str(QFileDialog.getOpenFileName(self, 'Load script from', './scripts/'))
        if fname:
            self.scriptFileLineEdit.setText(fname) 
    
    def increment_filename(self):
        #search for the regular expression that corresponds to the incrementable
        # file name
        p = re.compile(r"_[0-9]{3}[.]dat$")
        fname = str(self.outputFileLineEdit.text())
        found = p.findall(fname)
        print "found:" + str(found)
        if not found == []:
            ending = found[0]
            num = int(ending[1:4]) + 1
            fname = fname.replace(ending, "_%3.3d.dat"%num)
            self.outputFileLineEdit.setText(fname) 
            
    def get_header_text(self):        
       text = str(self.headerTextEdit.toPlainText())
       if text:
           text = "# " + text.replace("\n", "\n#") + "\n"
           return text
       else:
           return ""
       
if __name__=="__main__":
    
    app = QApplication(sys.argv)
    ex = StartWidget()
    ex.show()
    sys.exit(app.exec_())