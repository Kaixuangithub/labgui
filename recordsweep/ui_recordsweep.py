# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recordsweep.ui'
#
# Created: Fri Jun 07 14:52:14 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RecordSweepWindow(object):
    def setupUi(self, RecordSweepWindow):
        RecordSweepWindow.setObjectName(_fromUtf8("RecordSweepWindow"))
        RecordSweepWindow.resize(1268, 668)
        RecordSweepWindow.setWindowTitle(QtGui.QApplication.translate("RecordSweepWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(RecordSweepWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.plot_holder = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_holder.sizePolicy().hasHeightForWidth())
        self.plot_holder.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.plot_holder.setPalette(palette)
        self.plot_holder.setAutoFillBackground(True)
        self.plot_holder.setObjectName(_fromUtf8("plot_holder"))
        self.gridLayout.addWidget(self.plot_holder, 0, 0, 4, 1)
        self.startStopButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startStopButton.sizePolicy().hasHeightForWidth())
        self.startStopButton.setSizePolicy(sizePolicy)
        self.startStopButton.setMinimumSize(QtCore.QSize(100, 0))
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
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
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
        self.groupBox_Y.setTitle(QtGui.QApplication.translate("RecordSweepWindow", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_Y.setObjectName(_fromUtf8("groupBox_Y"))
        self.horizontalLayout_2.addWidget(self.groupBox_Y)
        self.groupBox_YR = QtGui.QGroupBox(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_YR.sizePolicy().hasHeightForWidth())
        self.groupBox_YR.setSizePolicy(sizePolicy)
        self.groupBox_YR.setTitle(QtGui.QApplication.translate("RecordSweepWindow", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_YR.setObjectName(_fromUtf8("groupBox_YR"))
        self.horizontalLayout_2.addWidget(self.groupBox_YR)
        spacerItem = QtGui.QSpacerItem(187, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.tabWidget)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        self.outputFileGroupBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputFileGroupBox.sizePolicy().hasHeightForWidth())
        self.outputFileGroupBox.setSizePolicy(sizePolicy)
        self.outputFileGroupBox.setTitle(QtGui.QApplication.translate("RecordSweepWindow", "Output File", None, QtGui.QApplication.UnicodeUTF8))
        self.outputFileGroupBox.setObjectName(_fromUtf8("outputFileGroupBox"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.outputFileGroupBox)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.outputFileLineEdit = QtGui.QLineEdit(self.outputFileGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputFileLineEdit.sizePolicy().hasHeightForWidth())
        self.outputFileLineEdit.setSizePolicy(sizePolicy)
        self.outputFileLineEdit.setObjectName(_fromUtf8("outputFileLineEdit"))
        self.horizontalLayout_4.addWidget(self.outputFileLineEdit)
        self.outputFileButton = QtGui.QPushButton(self.outputFileGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputFileButton.sizePolicy().hasHeightForWidth())
        self.outputFileButton.setSizePolicy(sizePolicy)
        self.outputFileButton.setText(QtGui.QApplication.translate("RecordSweepWindow", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.outputFileButton.setObjectName(_fromUtf8("outputFileButton"))
        self.horizontalLayout_4.addWidget(self.outputFileButton)
        self.gridLayout.addWidget(self.outputFileGroupBox, 2, 1, 1, 1)
        self.inputFileGroupBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputFileGroupBox.sizePolicy().hasHeightForWidth())
        self.inputFileGroupBox.setSizePolicy(sizePolicy)
        self.inputFileGroupBox.setTitle(QtGui.QApplication.translate("RecordSweepWindow", "Script to run", None, QtGui.QApplication.UnicodeUTF8))
        self.inputFileGroupBox.setObjectName(_fromUtf8("inputFileGroupBox"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.inputFileGroupBox)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.scriptFileLineEdit = QtGui.QLineEdit(self.inputFileGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scriptFileLineEdit.sizePolicy().hasHeightForWidth())
        self.scriptFileLineEdit.setSizePolicy(sizePolicy)
        self.scriptFileLineEdit.setObjectName(_fromUtf8("scriptFileLineEdit"))
        self.horizontalLayout_5.addWidget(self.scriptFileLineEdit)
        self.scriptFileButton = QtGui.QPushButton(self.inputFileGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scriptFileButton.sizePolicy().hasHeightForWidth())
        self.scriptFileButton.setSizePolicy(sizePolicy)
        self.scriptFileButton.setText(QtGui.QApplication.translate("RecordSweepWindow", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.scriptFileButton.setObjectName(_fromUtf8("scriptFileButton"))
        self.horizontalLayout_5.addWidget(self.scriptFileButton)
        self.gridLayout.addWidget(self.inputFileGroupBox, 3, 1, 1, 1)
        RecordSweepWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(RecordSweepWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1268, 21))
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

        self.retranslateUi(RecordSweepWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(RecordSweepWindow)

    def retranslateUi(self, RecordSweepWindow):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("RecordSweepWindow", "Instrument Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("RecordSweepWindow", "Plotting Options", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RecordSweepWindow = QtGui.QMainWindow()
    ui = Ui_RecordSweepWindow()
    ui.setupUi(RecordSweepWindow)
    RecordSweepWindow.show()
    sys.exit(app.exec_())

