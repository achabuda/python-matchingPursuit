#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
#    This file is part of Matching Pursuit Python program (python-MP).
#
#    python-MP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    python-MP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with python-MP. If not, see <http://www.gnu.org/licenses/>.

author: Tomasz Spustek
e-mail: tomasz@spustek.pl
University of Warsaw, July 06, 2015
'''

from PyQt4 import QtCore, QtGui

from dragAndDropListWidget_PYQT import DragDropListWidget_PYQT

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class mainWindowUI(object):
    ''' GUI graphical part for the main window.

    Class governing the graphical part of the default graphical user interface.
    It describes only parameters of used widgets, all operational functions
    are placed in separate class - settingsFunctions.py.

    '''

    def setupUi(self, mainWindow):
        mainWindow.setObjectName(_fromUtf8("mainWindow"))
        mainWindow.setEnabled(True)
        mainWindow.move(100,100)
        icon = QtGui.QIcon()
        icon1path = _fromUtf8("./Pictures/icon_application.png")
        icon.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon)
        
        # self.screenSize = QtGui.QDesktopWidget().screenGeometry()
        # print screenSize.width(), screenSize.height()

# CENTRAL WIDGET:
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

# TAB WIDGET:
        self.tabSpace = QtGui.QTabWidget()
        self.tabSpace.setTabsClosable(False)
        self.tabSpace.setTabShape(0)
        self.tabSpace.setMovable(0)
        self.tabSpace.setIconSize(QtCore.QSize(16,16))

        self.tab_books      = QtGui.QWidget()
        self.tab_dataInfo   = QtGui.QWidget()
        self.tab_settings   = QtGui.QWidget()
        self.tab_saving     = QtGui.QWidget()

        icon1 = QtGui.QIcon()
        iconPath = _fromUtf8("./pictures/icon_folder.png")
        icon1.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        icon2 = QtGui.QIcon()
        iconPath = _fromUtf8("./pictures/icon_settings.png")
        icon2.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.tabSpace.addTab(self.tab_books    , icon1 , "Books")
        self.tabSpace.addTab(self.tab_dataInfo , icon2 , "Parameters")
        self.tabSpace.addTab(self.tab_settings , icon2 , "Settings")

# GROUPBOXES:
        self.groupBoxData = QtGui.QGroupBox()
        self.groupBoxData.setObjectName(_fromUtf8("groupBoxData"))

        self.groupBoxDataInfo = QtGui.QGroupBox()
        self.groupBoxDataInfo.setObjectName(_fromUtf8("groupBoxDataInfo"))

        self.groupBoxAlgorithm = QtGui.QGroupBox()
        self.groupBoxAlgorithm.setObjectName(_fromUtf8("groupBoxAlgorithm"))

        self.groupBoxDictionary = QtGui.QGroupBox()
        self.groupBoxDictionary.setObjectName(_fromUtf8("groupBoxDictionary"))

        self.groupBoxSaving = QtGui.QGroupBox()
        self.groupBoxSaving.setObjectName(_fromUtf8("groupBoxSaving"))

        self.groupBoxBooks = QtGui.QGroupBox()
        self.groupBoxBooks.setObjectName(_fromUtf8("groupBoxBooks"))

        self.groupBoxErrors = QtGui.QGroupBox()
        self.groupBoxErrors.setObjectName(_fromUtf8("groupBoxErrors"))

# MAIN LAYOUTS:
        # books
        self.lay_books = QtGui.QHBoxLayout()
        self.lay_books.addWidget(self.groupBoxBooks)
        self.tab_books.setLayout(self.lay_books)
        
        # settings
        self.lay_settings  = QtGui.QVBoxLayout()
        self.lay_settings.addWidget(self.groupBoxDictionary)
        self.lay_settings.addWidget(self.groupBoxAlgorithm)
        self.tab_settings.setLayout(self.lay_settings)

        # dataInfo
        self.lay_dataInfo = QtGui.QVBoxLayout()
        self.lay_dataInfo.addWidget(self.groupBoxDataInfo)
        self.lay_dataInfo.addWidget(self.groupBoxSaving)
        self.tab_dataInfo.setLayout(self.lay_dataInfo)

# GROUPBOX - DATA
        dataGrid = QtGui.QGridLayout()
        self.groupBoxData.setLayout(dataGrid)

        self.btn_addData = QtGui.QPushButton(self.groupBoxData)
        icon1 = QtGui.QIcon()
        icon1path = _fromUtf8("./pictures/icon_add.png")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_addData.setIcon(icon1)
        self.btn_addData.setIconSize(QtCore.QSize(24, 24))
        self.btn_addData.setObjectName(_fromUtf8("btn_addData"))
        dataGrid.addWidget(self.btn_addData,0,0)

        self.btn_removeData = QtGui.QPushButton(self.groupBoxData)
        icon1 = QtGui.QIcon()
        icon1path = _fromUtf8("./pictures/icon_remove.png")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_removeData.setIcon(icon1)
        self.btn_removeData.setIconSize(QtCore.QSize(24, 24))
        self.btn_removeData.setObjectName(_fromUtf8("btn_removeData"))
        dataGrid.addWidget(self.btn_removeData,0,1)

        self.btn_calculate = QtGui.QPushButton(self.groupBoxData)
        icon1 = QtGui.QIcon()
        icon1path = _fromUtf8("./pictures/icon_run.png")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_calculate.setIcon(icon1)
        self.btn_calculate.setIconSize(QtCore.QSize(24, 24))
        self.btn_calculate.setObjectName(_fromUtf8("btn_calculate"))
        dataGrid.addWidget(self.btn_calculate,0,2)

        self.lst_data = DragDropListWidget_PYQT(QtGui.QMainWindow)
        dataGrid.addWidget(self.lst_data,1,0,2,0)

# GROUPBOX - DATAINFO
        dataInfoGrid = QtGui.QGridLayout()
        dataInfoGrid.setSpacing(5)
        self.groupBoxDataInfo.setLayout(dataInfoGrid)

        self.lbl_samplingFrequency = QtGui.QLabel(self.groupBoxDataInfo)
        self.lbl_samplingFrequency.setObjectName(_fromUtf8("lbl_samplingFrequency"))
        dataInfoGrid.addWidget(self.lbl_samplingFrequency,0,0)

        self.led_samplingFrequency = QtGui.QLineEdit(self.groupBoxDataInfo)
        self.led_samplingFrequency.setAlignment(QtCore.Qt.AlignCenter)
        self.led_samplingFrequency.setObjectName(_fromUtf8("led_samplingFrequency"))
        dataInfoGrid.addWidget(self.led_samplingFrequency,0,1)

        self.lbl_samplingFrequencyUnit = QtGui.QLabel(self.groupBoxDataInfo)
        self.lbl_samplingFrequencyUnit.setObjectName(_fromUtf8("lbl_samplingFrequencyUnit"))
        dataInfoGrid.addWidget(self.lbl_samplingFrequencyUnit,0,2)

        self.lbl_samples = QtGui.QLabel(self.groupBoxDataInfo)
        self.lbl_samples.setObjectName(_fromUtf8("lbl_samples"))
        dataInfoGrid.addWidget(self.lbl_samples,1,0)

        self.led_samples = QtGui.QLineEdit(self.groupBoxDataInfo)
        self.led_samples.setObjectName(_fromUtf8("led_samples"))
        self.led_samples.setAlignment(QtCore.Qt.AlignCenter)
        self.led_samples.setEnabled(False)
        dataInfoGrid.addWidget(self.led_samples,1,1)

        self.lbl_channels = QtGui.QLabel(self.groupBoxDataInfo)
        self.lbl_channels.setObjectName(_fromUtf8("lbl_channels"))
        dataInfoGrid.addWidget(self.lbl_channels,2,0)

        self.led_channels = QtGui.QLineEdit(self.groupBoxDataInfo)
        self.led_channels.setObjectName(_fromUtf8("led_channels"))
        self.led_channels.setAlignment(QtCore.Qt.AlignCenter)
        self.led_channels.setEnabled(False)
        dataInfoGrid.addWidget(self.led_channels,2,1)

        self.lbl_trials = QtGui.QLabel(self.groupBoxDataInfo)
        self.lbl_trials.setObjectName(_fromUtf8("lbl_trials"))
        dataInfoGrid.addWidget(self.lbl_trials,3,0)

        self.led_trials = QtGui.QLineEdit(self.groupBoxDataInfo)
        self.led_trials.setObjectName(_fromUtf8("led_trials"))
        self.led_trials.setAlignment(QtCore.Qt.AlignCenter)
        self.led_trials.setEnabled(False)
        dataInfoGrid.addWidget(self.led_trials,3,1)

        dataInfoGrid.setRowStretch(4,1)

# GROUPBOX - CONFIG
        configGrid = QtGui.QGridLayout()
        self.groupBoxAlgorithm.setLayout(configGrid)

        self.lbl_channels2calc = QtGui.QLabel(self.groupBoxAlgorithm)
        self.lbl_channels2calc.setObjectName(_fromUtf8("lbl_channels2calc"))
        configGrid.addWidget(self.lbl_channels2calc,0,0)

        self.led_channels2calc = QtGui.QLineEdit(self.groupBoxAlgorithm)
        self.led_channels2calc.setObjectName(_fromUtf8("led_channels2calc"))
        self.led_channels2calc.setAlignment(QtCore.Qt.AlignCenter)
        configGrid.addWidget(self.led_channels2calc,0,1)

        self.lbl_trials2calc = QtGui.QLabel(self.groupBoxAlgorithm)
        self.lbl_trials2calc.setObjectName(_fromUtf8("lbl_trials2calc"))
        configGrid.addWidget(self.lbl_trials2calc,1,0)

        self.led_trials2calc = QtGui.QLineEdit(self.groupBoxAlgorithm)
        self.led_trials2calc.setObjectName(_fromUtf8("led_trials2calc"))
        self.led_trials2calc.setAlignment(QtCore.Qt.AlignCenter)
        configGrid.addWidget(self.led_trials2calc,1,1)


        self.lbl_algorithmType = QtGui.QLabel(self.groupBoxAlgorithm)
        self.lbl_algorithmType.setObjectName(_fromUtf8("lbl_algorithmType"))
        configGrid.addWidget(self.lbl_algorithmType,2,0)

        self.cmb_algorithmType = QtGui.QComboBox(self.groupBoxAlgorithm)
        self.cmb_algorithmType.setObjectName(_fromUtf8("cmb_algorithmType"))
        configGrid.addWidget(self.cmb_algorithmType,2,1)

        self.lbl_useGradient = QtGui.QLabel(self.groupBoxAlgorithm)
        self.lbl_useGradient.setObjectName(_fromUtf8("lbl_useGradient"))
        configGrid.addWidget(self.lbl_useGradient,3,0)

        self.chb_useGradient = QtGui.QCheckBox(self.groupBoxAlgorithm)
        self.chb_useGradient.setTristate(False)
        self.chb_useGradient.setObjectName(_fromUtf8("chb_useGradient"))
        configGrid.addWidget(self.chb_useGradient,3,1)

        self.lbl_iterationsLimit = QtGui.QLabel(self.groupBoxAlgorithm)
        self.lbl_iterationsLimit.setObjectName(_fromUtf8("lbl_iterationsLimit"))
        configGrid.addWidget(self.lbl_iterationsLimit,4,0)

        self.led_iterationsLimit = QtGui.QLineEdit(self.groupBoxAlgorithm)
        self.led_iterationsLimit.setObjectName(_fromUtf8("led_iterationsLimit"))
        self.led_iterationsLimit.setAlignment(QtCore.Qt.AlignCenter)
        configGrid.addWidget(self.led_iterationsLimit,4,1)

        self.lbl_energyLimit = QtGui.QLabel(self.groupBoxAlgorithm)
        self.lbl_energyLimit.setObjectName(_fromUtf8("lbl_energyLimit"))
        configGrid.addWidget(self.lbl_energyLimit,5,0)

        self.led_energyLimit = QtGui.QLineEdit(self.groupBoxAlgorithm)
        self.led_energyLimit.setObjectName(_fromUtf8("led_energyLimit"))
        self.led_energyLimit.setAlignment(QtCore.Qt.AlignCenter)
        configGrid.addWidget(self.led_energyLimit,5,1)

        self.lbl_nfft = QtGui.QLabel(self.groupBoxAlgorithm)
        self.lbl_nfft.setObjectName(_fromUtf8("lbl_nfft"))
        configGrid.addWidget(self.lbl_nfft,6,0)

        self.led_nfft = QtGui.QLineEdit(self.groupBoxAlgorithm)
        self.led_nfft.setObjectName(_fromUtf8("led_nfft"))
        self.led_nfft.setAlignment(QtCore.Qt.AlignCenter)
        configGrid.addWidget(self.led_nfft,6,1)

        self.lbl_displayInfo = QtGui.QLabel(self.groupBoxAlgorithm)
        self.lbl_displayInfo.setObjectName(_fromUtf8("lbl_displayInfo"))
        configGrid.addWidget(self.lbl_displayInfo,7,0)

        self.chb_displayInfo = QtGui.QCheckBox(self.groupBoxAlgorithm)
        self.chb_displayInfo.setTristate(False)
        self.chb_displayInfo.setObjectName(_fromUtf8("chb_displayInfo"))
        configGrid.addWidget(self.chb_displayInfo,7,1)

        configGrid.setRowStretch(8,1)



# GROUPBOX - DICTIONARY
        dictionaryGrid = QtGui.QGridLayout()
        self.groupBoxDictionary.setLayout(dictionaryGrid)

        self.lbl_dictionaryH1 = QtGui.QLabel(self.groupBoxDictionary)
        self.lbl_dictionaryH1.setStyleSheet('font-weight: bold;')
        self.lbl_dictionaryH1.setObjectName(_fromUtf8("lbl_dictionaryH1"))
        dictionaryGrid.addWidget(self.lbl_dictionaryH1,0,0,2,0)

        self.lbl_dictonaryDensity = QtGui.QLabel(self.groupBoxDictionary)
        self.lbl_dictonaryDensity.setObjectName(_fromUtf8("lbl_dictonaryDensity"))
        dictionaryGrid.addWidget(self.lbl_dictonaryDensity,1,0,1,0)

        self.led_dictonaryDensity = QtGui.QLineEdit(self.groupBoxDictionary)
        self.led_dictonaryDensity.setObjectName(_fromUtf8("led_dictonaryDensity"))
        self.led_dictonaryDensity.setAlignment(QtCore.Qt.AlignCenter)
        dictionaryGrid.addWidget(self.led_dictonaryDensity,1,1)

        self.lbl_minS = QtGui.QLabel(self.groupBoxDictionary)
        self.lbl_minS.setObjectName(_fromUtf8("lbl_minS"))
        dictionaryGrid.addWidget(self.lbl_minS,2,0)

        self.led_minS = QtGui.QLineEdit(self.groupBoxDictionary)
        self.led_minS.setObjectName(_fromUtf8("led_minS"))
        self.led_minS.setAlignment(QtCore.Qt.AlignCenter)
        dictionaryGrid.addWidget(self.led_minS,2,1)

        self.cmb_minS = QtGui.QComboBox(self.groupBoxDictionary)
        self.cmb_minS.setObjectName(_fromUtf8("cmb_minS"))
        dictionaryGrid.addWidget(self.cmb_minS,2,2)

        self.lbl_maxS = QtGui.QLabel(self.groupBoxDictionary)
        self.lbl_maxS.setObjectName(_fromUtf8("lbl_maxS"))
        dictionaryGrid.addWidget(self.lbl_maxS,3,0)

        self.led_maxS = QtGui.QLineEdit(self.groupBoxDictionary)
        self.led_maxS.setObjectName(_fromUtf8("led_minS"))
        self.led_maxS.setAlignment(QtCore.Qt.AlignCenter)
        dictionaryGrid.addWidget(self.led_maxS,3,1)

        self.cmb_maxS = QtGui.QComboBox(self.groupBoxDictionary)
        self.cmb_maxS.setObjectName(_fromUtf8("cmb_maxS"))
        dictionaryGrid.addWidget(self.cmb_maxS,3,2)

        self.lbl_useAsym = QtGui.QLabel(self.groupBoxDictionary)
        self.lbl_useAsym.setObjectName(_fromUtf8("lbl_useAsym"))
        dictionaryGrid.addWidget(self.lbl_useAsym,4,0,1,0)

        self.chb_useAsym = QtGui.QCheckBox(self.groupBoxDictionary)
        self.chb_useAsym.setTristate(0)
        self.chb_useAsym.setObjectName(_fromUtf8("chb_useAsym"))
        dictionaryGrid.addWidget(self.chb_useAsym,4,1)

        self.lbl_useRect = QtGui.QLabel(self.groupBoxDictionary)
        self.lbl_useRect.setObjectName(_fromUtf8("lbl_useRect"))
        dictionaryGrid.addWidget(self.lbl_useRect,5,0,1,0)

        self.chb_useRect = QtGui.QCheckBox(self.groupBoxDictionary)
        self.chb_useRect.setTristate(0)
        self.chb_useRect.setObjectName(_fromUtf8("chb_useRect"))
        dictionaryGrid.addWidget(self.chb_useRect,5,1)

        dictionaryGrid.setColumnStretch(0,3)
        dictionaryGrid.setColumnStretch(1,2)
        dictionaryGrid.setColumnStretch(2,2)

        dictionaryGrid.setRowStretch(6,1)


# GROUPBOX - SAVING
        savingGrid = QtGui.QGridLayout()
        self.groupBoxSaving.setLayout(savingGrid)

        self.btn_dictionarySave = QtGui.QPushButton(self.groupBoxSaving)
        icon1 = QtGui.QIcon()
        icon1path = _fromUtf8("./pictures/icon_save.png")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_dictionarySave.setIcon(icon1)
        self.btn_dictionarySave.setIconSize(QtCore.QSize(24, 24))
        self.btn_dictionarySave.setObjectName(_fromUtf8("btn_dictionarySave"))
        self.btn_dictionarySave.setStyleSheet("text-align: left")

        savingGrid.addWidget(self.btn_dictionarySave,0,0)

        self.btn_configSave = QtGui.QPushButton(self.groupBoxSaving)
        icon1 = QtGui.QIcon()
        icon1path = _fromUtf8("./pictures/icon_save.png")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_configSave.setIcon(icon1)
        self.btn_configSave.setIconSize(QtCore.QSize(24, 24))
        self.btn_configSave.setObjectName(_fromUtf8("btn_configSave"))
        self.btn_configSave.setStyleSheet("text-align: left")

        savingGrid.addWidget(self.btn_configSave,1,0)

        savingGrid.setColumnStretch(1,1)
        savingGrid.setRowStretch(2,1)

# GROUPBOX - BOOKS
        booksGrid = QtGui.QGridLayout()
        self.groupBoxBooks.setLayout(booksGrid)

        self.btn_saveSelectedBooks = QtGui.QPushButton(self.groupBoxBooks)
        icon1 = QtGui.QIcon()
        icon1path = _fromUtf8("./pictures/icon_save.png")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_saveSelectedBooks.setIcon(icon1)
        self.btn_saveSelectedBooks.setIconSize(QtCore.QSize(24, 24))
        self.btn_saveSelectedBooks.setObjectName(_fromUtf8("btn_saveSelectedBooks"))
        booksGrid.addWidget(self.btn_saveSelectedBooks,0,0)

        self.btn_openVisualisationTool = QtGui.QPushButton(self.groupBoxBooks)
        icon1 = QtGui.QIcon()
        icon1path = _fromUtf8("./pictures/icon_visualize.png")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_openVisualisationTool.setIcon(icon1)
        self.btn_openVisualisationTool.setIconSize(QtCore.QSize(24, 24))
        self.btn_openVisualisationTool.setObjectName(_fromUtf8("btn_openVisualisationTool"))
        booksGrid.addWidget(self.btn_openVisualisationTool,0,1)

        self.lst_books = QtGui.QListWidget(self.groupBoxBooks)
        self.lst_books.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        booksGrid.addWidget(self.lst_books,1,0,1,0)

# GROUPBOX - ERRORS
        lay_errors = QtGui.QVBoxLayout()
        self.groupBoxErrors.setLayout(lay_errors)

        self.lbl_errors = QtGui.QLabel(self.groupBoxErrors)
        self.lbl_errors.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setItalic(True)
        self.lbl_errors.setFont(font)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)
        self.lbl_errors.setPalette(palette)
        self.lbl_errors.setObjectName(_fromUtf8("lbl_errors"))
        lay_errors.addWidget(self.lbl_errors)
        lay_errors.addStretch(1)


# SET ALL THINGS UP:
        self.lay_main = QtGui.QVBoxLayout()

        self.lay_panels = QtGui.QHBoxLayout()
        self.lay_panels.addWidget(self.groupBoxData)
        self.lay_panels.addWidget(self.tabSpace)

        self.lay_main.addLayout(self.lay_panels)
        self.lay_main.addWidget(self.groupBoxErrors)

        self.centralwidget.setLayout(self.lay_main)

        mainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        
        mainWindow.setWindowTitle(_translate("mainWindow", "python-MatchingPursuit -- main window", None))

        self.groupBoxData.setTitle(_translate("mainWindow"  , "Data", None))
        self.groupBoxDataInfo.setTitle(_translate("mainWindow", "Data specification", None))
        self.groupBoxAlgorithm.setTitle(_translate("mainWindow", "MP configuration", None))
        self.groupBoxDictionary.setTitle(_translate("mainWindow", "Dictionary configuration", None))
        self.groupBoxSaving.setTitle(_translate("mainWindow", "Save", None))
        self.groupBoxBooks.setTitle(_translate("mainWindow", "Results", None))
        self.groupBoxErrors.setTitle(_translate("mainWindow", "", None))

        self.lbl_samplingFrequency.setText(_translate("mainWindow", "Sampling:", None))
        self.lbl_samplingFrequencyUnit.setText(_translate("mainWindow", "[Hz]", None))
        self.lbl_samples.setText(_translate("mainWindow", "# of samples:", None))
        self.lbl_channels.setText(_translate("mainWindow", "# of channels:", None))
        self.lbl_trials.setText(_translate("mainWindow", "# of trials:", None))
        self.lbl_channels2calc.setText(_translate("mainWindow", "Channel range:", None))
        self.lbl_trials2calc.setText(_translate("mainWindow", "Trial range:", None))
        self.lbl_algorithmType.setText(_translate("mainWindow", "Algorithm:", None))
        self.lbl_useGradient.setText(_translate("mainWindow", "Use gradient opt:", None))
        self.lbl_iterationsLimit.setText(_translate("mainWindow", "# of iterations:", None))
        self.lbl_energyLimit.setText(_translate("mainWindow", "Energy percentage:", None))
        self.lbl_nfft.setText(_translate("mainWindow", "NFFT:", None))
        self.lbl_displayInfo.setText(_translate("mainWindow", "Display informations:", None))
        self.lbl_dictonaryDensity.setText(_translate("mainWindow", "Dictionary density:", None))
        self.lbl_minS.setText(_translate("mainWindow", "Min. width:", None))
        self.lbl_maxS.setText(_translate("mainWindow", "Max. width:", None))
        self.lbl_useAsym.setText(_translate("mainWindow", "Include asymetrics:", None))
        self.lbl_useRect.setText(_translate("mainWindow", "Include rectangularities:", None))
        self.lbl_errors.setText(_translate("mainWindow", "Some error", None))

        self.btn_addData.setText(_translate("mainWindow", "Add", None))
        self.btn_removeData.setText(_translate("mainWindow", "Remove", None))
        self.btn_calculate.setText(_translate("mainWindow", "Run", None))
        self.btn_saveSelectedBooks.setText(_translate("mainWindow", "", None))
        self.btn_openVisualisationTool.setText(_translate("mainWindow", "", None))
        self.btn_dictionarySave.setText(_translate("mainWindow", "Save the dictionary", None))
        self.btn_configSave.setText(_translate("mainWindow", "Save current configuration", None))


###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################

if __name__ == '__main__':
    print 'Using this classes without it\'s functional parts may be possible, but'
    print 'it would be completely useless.'
