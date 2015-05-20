# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recordsweep.ui'
#
# Created: Fri Feb 15 18:17:16 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

from mplZoomWidget import MatplotlibZoomWidget

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RecordSweepWindow(object):
    def setupUi(self, RecordSweepWindow):
        RecordSweepWindow.setObjectName(_fromUtf8("RecordSweepWindow"))
        RecordSweepWindow.resize(1099, 520)
        RecordSweepWindow.setWindowTitle(QtGui.QApplication.translate("RecordSweepWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(RecordSweepWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.mplwidget = MatplotlibZoomWidget(self.centralwidget)
        self.mplwidget.setObjectName(_fromUtf8("mplwidget"))
        self.gridLayout.addWidget(self.mplwidget, 0, 0, 2, 1)
        self.startStopButton = QtGui.QPushButton(self.centralwidget)
        self.startStopButton.setText(QtGui.QApplication.translate("RecordSweepWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.startStopButton.setObjectName(_fromUtf8("startStopButton"))
        self.gridLayout.addWidget(self.startStopButton, 0, 1, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.groupBox_Name = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_Name.sizePolicy().hasHeightForWidth())
        self.groupBox_Name.setSizePolicy(sizePolicy)
        self.groupBox_Name.setMinimumSize(QtCore.QSize(100, 0))
        self.groupBox_Name.setTitle(QtGui.QApplication.translate("RecordSweepWindow", "Channel", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_Name.setObjectName(_fromUtf8("groupBox_Name"))
        self.horizontalLayout_3.addWidget(self.groupBox_Name)
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox_Type = QtGui.QGroupBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_Type.sizePolicy().hasHeightForWidth())
        self.groupBox_Type.setSizePolicy(sizePolicy)
        self.groupBox_Type.setMinimumSize(QtCore.QSize(80, 0))
        self.groupBox_Type.setTitle(QtGui.QApplication.translate("RecordSweepWindow", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_Type.setObjectName(_fromUtf8("groupBox_Type"))
        self.horizontalLayout.addWidget(self.groupBox_Type)
        self.groupBox_Instr = QtGui.QGroupBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_Instr.sizePolicy().hasHeightForWidth())
        self.groupBox_Instr.setSizePolicy(sizePolicy)
        self.groupBox_Instr.setMinimumSize(QtCore.QSize(80, 0))
        self.groupBox_Instr.setTitle(QtGui.QApplication.translate("RecordSweepWindow", "Instrument", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_Instr.setObjectName(_fromUtf8("groupBox_Instr"))
        self.horizontalLayout.addWidget(self.groupBox_Instr)
        self.groupBox_Param = QtGui.QGroupBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_Param.sizePolicy().hasHeightForWidth())
        self.groupBox_Param.setSizePolicy(sizePolicy)
        self.groupBox_Param.setMinimumSize(QtCore.QSize(80, 0))
        self.groupBox_Param.setTitle(QtGui.QApplication.translate("RecordSweepWindow", "Parameter", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_Param.setObjectName(_fromUtf8("groupBox_Param"))
        self.horizontalLayout.addWidget(self.groupBox_Param)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.groupBox_X = QtGui.QGroupBox(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_X.sizePolicy().hasHeightForWidth())
        self.groupBox_X.setSizePolicy(sizePolicy)
        self.groupBox_X.setTitle(QtGui.QApplication.translate("RecordSweepWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_X.setObjectName(_fromUtf8("groupBox_X"))
        self.horizontalLayout_2.addWidget(self.groupBox_X)
        self.groupBox_Y = QtGui.QGroupBox(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_Y.sizePolicy().hasHeightForWidth())
        self.groupBox_Y.setSizePolicy(sizePolicy)
        self.groupBox_Y.setTitle(QtGui.QApplication.translate("RecordSweepWindow", "YL", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_Y.setObjectName(_fromUtf8("groupBox_Y"))
        self.horizontalLayout_2.addWidget(self.groupBox_Y)
        
        self.groupBox_YR = QtGui.QGroupBox(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_YR.sizePolicy().hasHeightForWidth())        
        self.groupBox_YR.setSizePolicy(sizePolicy)
        self.groupBox_YR.setTitle(QtGui.QApplication.translate("RecordSweepWindow", "YR", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_YR.setObjectName(_fromUtf8("groupBox_YR"))       
        self.horizontalLayout_2.addWidget(self.groupBox_YR)
        
        spacerItem = QtGui.QSpacerItem(187, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.tabWidget)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        RecordSweepWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(RecordSweepWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1099, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        RecordSweepWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(RecordSweepWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        RecordSweepWindow.setStatusBar(self.statusbar)
        self.actionSave_figure = QtGui.QAction(RecordSweepWindow)
        self.actionSave_figure.setText(QtGui.QApplication.translate("RecordSweepWindow", "Save figure", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_figure.setObjectName(_fromUtf8("actionSave_figure"))
        self.actionQuit = QtGui.QAction(RecordSweepWindow)
        self.actionQuit.setText(QtGui.QApplication.translate("RecordSweepWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))

        self.lineEdit_Name = []
        self.comboBox_Type = []
        self.comboBox_Instr = []
        self.comboBox_Param = []       
        self.radioButton_X = [] 
        self.checkBox_Y = [] 
        self.checkBox_YR = []
   
        self.color_set = ['black', 'blue', 'green', 'red', 'orange', 'magenta', 'chartreuse', 'maroon', 'plum','violet'] 
        
        for i in range (self.MAX_CHANNELS):   

            pos_LE = lambda x: (20 * x + 1) + 50
                    
            self.lineEdit_Name.append(QtGui.QLineEdit(self.groupBox_Name))
            self.lineEdit_Name[i].setGeometry(QtCore.QRect(10, pos_LE(i), 81, 16))
            self.lineEdit_Name[i].setText(QtGui.QApplication.translate("RecordSweepWindow", "", None, QtGui.QApplication.UnicodeUTF8))
            self.lineEdit_Name[i].setObjectName(_fromUtf8("lineEdit_Name"))
            self.lineEdit_Name[i].setStyleSheet('QLineEdit {color: %s}'%self.color_set[i])
            
            
            self.comboBox_Type.append(QtGui.QComboBox(self.groupBox_Type))
            self.comboBox_Type[i].setGeometry(QtCore.QRect(5, 20 * (i+1), 71, 16))
            self.comboBox_Type[i].setObjectName(_fromUtf8("comboBox"))
            self.comboBox_Type[i].addItems(self.INSTRUMENT_TYPES)
            
            self.connect(self.comboBox_Type[i], QtCore.SIGNAL("currentIndexChanged(int)"), self.ComboBoxTypeHandler)                  

            self.comboBox_Instr.append(QtGui.QComboBox(self.groupBox_Instr))
            self.comboBox_Instr[i].setGeometry(QtCore.QRect(5, 20 * (i+1), 71, 16))
            self.comboBox_Instr[i].setObjectName(_fromUtf8("comboBox"))
            
            self.comboBox_Param.append(QtGui.QComboBox(self.groupBox_Param))
            self.comboBox_Param[i].setGeometry(QtCore.QRect(5, 20 * (i+1), 71, 16))
            self.comboBox_Param[i].setObjectName(_fromUtf8("comboBox"))

            self.radioButton_X.append(QtGui.QRadioButton(self.groupBox_X))
            self.radioButton_X[i].setGeometry(QtCore.QRect(7, 20*(i+1), 16, 16))
            self.radioButton_X[i].setText(_fromUtf8(""))
            self.radioButton_X[i].setObjectName(_fromUtf8("radioButton_" + str(i)))
            self.connect(self.radioButton_X[i], QtCore.SIGNAL("toggled(bool)"), self.XRadioButtonHandler)                          
      
            self.checkBox_Y.append(QtGui.QCheckBox(self.groupBox_Y))
            self.checkBox_Y[i].setGeometry(QtCore.QRect(5, 20 * (i+1), 16, 16))
            self.checkBox_Y[i].setText(_fromUtf8(""))
            self.checkBox_Y[i].setObjectName(_fromUtf8("checkBox_" +str(i)))  
            self.connect(self.checkBox_Y[i], QtCore.SIGNAL("stateChanged(int)"), self.YCheckBoxHandler)     
            
            self.checkBox_YR.append(QtGui.QCheckBox(self.groupBox_YR))
            self.checkBox_YR[i].setGeometry(QtCore.QRect(5, 20 * (i+1), 16, 16))
            self.checkBox_YR[i].setText(_fromUtf8(""))
            self.checkBox_YR[i].setObjectName(_fromUtf8("checkBox_" +str(i)))  
            self.connect(self.checkBox_YR[i], QtCore.SIGNAL("stateChanged(int)"), self.YCheckBoxHandler)     
            
        self.fileSaveSettingsAction = self.createAction("Save Settings", slot=self.fileSaveSettings, shortcut=QtGui.QKeySequence.SaveAs,
                                        icon=None, tip="Save the current instrument settings")
        
        self.fileLoadSettingsAction = self.createAction("Load Settings", slot=self.fileLoadSettings, shortcut=QtGui.QKeySequence.Open,
                                        icon=None, tip="Load instrument settings from file")               
        
        self.fileSaveFigAction = self.createAction("&Save Figure", slot=self.fileSaveFig, shortcut=QtGui.QKeySequence.Save,
                                        icon=None, tip="Save the current figure")      
        
        self.filePrintAction = self.createAction("&Print Report", slot=self.filePrint, shortcut=QtGui.QKeySequence.Print,
                                        icon=None, tip="Print the figure along with relevant information")                   
        
        self.plotToggleControlLAction = self.createAction("Toggle &Left Axes Control", slot=self.toggleControlL, shortcut=QtGui.QKeySequence("Ctrl+L"),
                                        icon="toggleLeft", tip="Toggle whether the mouse adjusts Left axes pan and zoom", checkable=True)                   

        self.plotToggleControlRAction = self.createAction("Toggle &Right Axes Control", slot=self.toggleControlR, shortcut=QtGui.QKeySequence("Ctrl+R"),
                                        icon="toggleRight", tip="Toggle whether the mouse adjusts right axes pan and zoom", checkable=True)                   

        self.plotToggleXControlAction = self.createAction("Toggle &X Axes Control", slot=self.toggleXControl, shortcut=QtGui.QKeySequence("Ctrl+X"),
                                        icon="toggleX", tip="Toggle whether the mouse adjusts x axis pan and zoom", checkable=True)                   
         
                    
        self.plotAutoScaleXAction = self.createAction("Auto Scale X", slot=self.toggleAutoScaleX, shortcut=QtGui.QKeySequence("Ctrl+A"),
                                        icon="toggleAutoScaleX", tip="Turn autoscale X on or off", checkable=True)                   
                    
        self.plotAutoScaleLAction = self.createAction("Auto Scale L", slot=self.toggleAutoScaleL, shortcut=QtGui.QKeySequence("Ctrl+D"),
                                        icon="toggleAutoScaleL", tip="Turn autoscale Left Y on or off", checkable=True)                   

        self.plotAutoScaleRAction = self.createAction("Auto Scale R", slot=self.toggleAutoScaleR, shortcut=QtGui.QKeySequence("Ctrl+E"),
                                        icon="toggleAutoScaleR", tip="Turn autoscale Right Y on or off", checkable=True)                   
                            
        
        self.fileMenu = self.menuBar().addMenu("File")  

        self.fileMenu.addAction(self.fileLoadSettingsAction)
        self.fileMenu.addAction(self.fileSaveSettingsAction)
        self.fileMenu.addAction(self.filePrintAction)       
        #self.fileMenu.addAction("Refresh Instrument List", self.refresh_instrument_list)
        self.fileMenu.addAction(self.fileSaveFigAction)

        
        self.plotMenu = self.menuBar().addMenu("&Plot")
        
        self.plotMenu.addAction(self.plotToggleXControlAction)
        self.plotMenu.addAction(self.plotToggleControlLAction)
        self.plotMenu.addAction(self.plotToggleControlRAction)

        self.plotMenu.addAction(self.plotAutoScaleXAction)    
        self.plotMenu.addAction(self.plotAutoScaleLAction)  
        self.plotMenu.addAction(self.plotAutoScaleRAction)
        
        plotToolbar = self.addToolBar("Plot")
        plotToolbar.addAction(self.plotToggleXControlAction)
        plotToolbar.addAction(self.plotToggleControlLAction)
        plotToolbar.addAction(self.plotToggleControlRAction)

        plotToolbar.addAction(self.plotAutoScaleXAction)
        plotToolbar.addAction(self.plotAutoScaleLAction)
        plotToolbar.addAction(self.plotAutoScaleRAction)

              
        self.tabWidget.setCurrentIndex(0)

        self.retranslateUi(RecordSweepWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(RecordSweepWindow)


    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):     
        action = QtGui.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon("./images/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, QtCore.SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
        
    def retranslateUi(self, RecordSweepWindow):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("RecordSweepWindow", "Instrument Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("RecordSweepWindow", "Plotting Options", None, QtGui.QApplication.UnicodeUTF8))

from matplotlibwidget import MatplotlibWidget
