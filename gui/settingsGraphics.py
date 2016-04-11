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
import time
from platform import system

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

        self.basicWindowSize = (600, 550)

        mainWindow.setObjectName(_fromUtf8("mainWindow"))
        mainWindow.setEnabled(True)
        mainWindow.resize(self.basicWindowSize[0] , self.basicWindowSize[1])
        mainWindow.setMinimumSize(QtCore.QSize(self.basicWindowSize[0] , self.basicWindowSize[1]))
        mainWindow.setMaximumSize(QtCore.QSize(self.basicWindowSize[0] , self.basicWindowSize[1]))
        # icon = QtGui.QIcon()
        # 
        # if system() == 'Windows':
        #     icon1path = _fromUtf8("./Pictures/settings.png")
        # else:
        #     icon1path = _fromUtf8("./Pictures/settings.svg")
        # 
        # icon.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # mainWindow.setWindowIcon(icon)
        
        self.screenSize = QtGui.QDesktopWidget().screenGeometry()
        #print screenSize.width(), screenSize.height()

# CENTRAL WIDGET:
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

# GROUPBOXES:
        self.groupBoxData = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxData.setGeometry(QtCore.QRect(10,10,280,370))
        self.groupBoxData.setObjectName(_fromUtf8("groupBoxData"))

        self.groupBoxDataInfo = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxDataInfo.setGeometry(QtCore.QRect(305,10,0,140))
        self.groupBoxDataInfo.setObjectName(_fromUtf8("groupBoxDataInfo"))

        self.groupBoxAlgorithm = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxAlgorithm.setGeometry(QtCore.QRect(305,160,0,220))
        self.groupBoxAlgorithm.setObjectName(_fromUtf8("groupBoxAlgorithm"))        

        self.groupBoxDictionary = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxDictionary.setGeometry(QtCore.QRect(305,10,0,370))
        self.groupBoxDictionary.setObjectName(_fromUtf8("groupBoxDictionary"))

        self.groupBoxBooks = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxBooks.setGeometry(QtCore.QRect(310,10,280,370))
        self.groupBoxBooks.setObjectName(_fromUtf8("groupBoxBooks"))

        self.groupBoxErrors = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxErrors.setGeometry(QtCore.QRect(10,380,580,160))
        self.groupBoxErrors.setObjectName(_fromUtf8("groupBoxErrors"))

# GROUPBOX - DATA
        dataGrid = QtGui.QGridLayout()
        self.groupBoxData.setLayout(dataGrid)

        self.btn_addData = QtGui.QPushButton(self.groupBoxData)
        icon1 = QtGui.QIcon()
        if system() == 'Windows':
            icon1path = _fromUtf8("./pictures/add.png")
        else:
            icon1path = _fromUtf8("./pictures/add.svg")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_addData.setIcon(icon1)
        self.btn_addData.setIconSize(QtCore.QSize(24, 24))
        self.btn_addData.setObjectName(_fromUtf8("btn_addData"))
        dataGrid.addWidget(self.btn_addData,0,0)

        self.btn_removeData = QtGui.QPushButton(self.groupBoxData)
        icon1 = QtGui.QIcon()
        if system() == 'Windows':
            icon1path = _fromUtf8("./pictures/clear.png")
        else:
            icon1path = _fromUtf8("./pictures/clear.svg")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_removeData.setIcon(icon1)
        self.btn_removeData.setIconSize(QtCore.QSize(24, 24))
        self.btn_removeData.setObjectName(_fromUtf8("btn_removeData"))
        dataGrid.addWidget(self.btn_removeData,0,1)

        self.btn_settingsData = QtGui.QPushButton(self.groupBoxData)
        icon1 = QtGui.QIcon()
        if system() == 'Windows':
            icon1path = _fromUtf8("./pictures/settings.png")
        else:
            icon1path = _fromUtf8("./pictures/settings.svg")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_settingsData.setIcon(icon1)
        self.btn_settingsData.setIconSize(QtCore.QSize(24, 24))
        self.btn_settingsData.setObjectName(_fromUtf8("btn_settingsData"))
        dataGrid.addWidget(self.btn_settingsData,0,2)

        self.lst_data = QtGui.QListWidget(self.groupBoxData)
        self.lst_data.setAcceptDrops(True)
        # self.lst_data.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        # self.lst_data.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        # self.lst_data.setViewMode(QtGui.QListView.IconMode)
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
        configGrid.addWidget(self.led_channels2calc,0,1)

        self.lbl_trials2calc = QtGui.QLabel(self.groupBoxAlgorithm)
        self.lbl_trials2calc.setObjectName(_fromUtf8("lbl_trials2calc"))
        configGrid.addWidget(self.lbl_trials2calc,1,0)

        self.led_trials2calc = QtGui.QLineEdit(self.groupBoxAlgorithm)
        self.led_trials2calc.setObjectName(_fromUtf8("led_trials2calc"))
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
        configGrid.addWidget(self.led_iterationsLimit,4,1)

        self.lbl_energyLimit = QtGui.QLabel(self.groupBoxAlgorithm)
        self.lbl_energyLimit.setObjectName(_fromUtf8("lbl_energyLimit"))
        configGrid.addWidget(self.lbl_energyLimit,5,0)

        self.led_energyLimit = QtGui.QLineEdit(self.groupBoxAlgorithm)
        self.led_energyLimit.setObjectName(_fromUtf8("led_energyLimit"))
        configGrid.addWidget(self.led_energyLimit,5,1)

        self.lbl_nfft = QtGui.QLabel(self.groupBoxAlgorithm)
        self.lbl_nfft.setObjectName(_fromUtf8("lbl_nfft"))
        configGrid.addWidget(self.lbl_nfft,6,0)

        self.led_nfft = QtGui.QLineEdit(self.groupBoxAlgorithm)
        self.led_nfft.setObjectName(_fromUtf8("led_nfft"))
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
        dictionaryGrid.addWidget(self.led_dictonaryDensity,1,2)

        self.lbl_minS = QtGui.QLabel(self.groupBoxDictionary)
        self.lbl_minS.setObjectName(_fromUtf8("lbl_minS"))
        dictionaryGrid.addWidget(self.lbl_minS,2,0)

        self.led_minS = QtGui.QLineEdit(self.groupBoxDictionary)
        self.led_minS.setObjectName(_fromUtf8("led_minS"))
        dictionaryGrid.addWidget(self.led_minS,2,1)

        self.cmb_minS = QtGui.QComboBox(self.groupBoxDictionary)
        self.cmb_minS.setObjectName(_fromUtf8("cmb_minS"))
        dictionaryGrid.addWidget(self.cmb_minS,2,2)

        self.lbl_maxS = QtGui.QLabel(self.groupBoxDictionary)
        self.lbl_maxS.setObjectName(_fromUtf8("lbl_maxS"))
        dictionaryGrid.addWidget(self.lbl_maxS,3,0)

        self.led_maxS = QtGui.QLineEdit(self.groupBoxDictionary)
        self.led_maxS.setObjectName(_fromUtf8("led_minS"))
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
        dictionaryGrid.addWidget(self.chb_useAsym,4,2)

        self.lbl_useRect = QtGui.QLabel(self.groupBoxDictionary)
        self.lbl_useRect.setObjectName(_fromUtf8("lbl_useRect"))
        dictionaryGrid.addWidget(self.lbl_useRect,5,0,1,0)

        self.chb_useRect = QtGui.QCheckBox(self.groupBoxDictionary)
        self.chb_useRect.setTristate(0)
        self.chb_useRect.setObjectName(_fromUtf8("chb_useRect"))
        dictionaryGrid.addWidget(self.chb_useRect,5,2)

        self.btn_dictionarySave = QtGui.QPushButton(self.groupBoxDictionary)
        # icon1 = QtGui.QIcon()
        # if system() == 'Windows':
        #     icon1path = _fromUtf8("./pictures/add.png")
        # else:
        #     icon1path = _fromUtf8("./pictures/add.svg")
        # icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.btn_dictionarySave.setIcon(icon1)
        # self.btn_dictionarySave.setIconSize(QtCore.QSize(24, 24))
        self.btn_dictionarySave.setObjectName(_fromUtf8("btn_dictionarySave"))
        dictionaryGrid.addWidget(self.btn_dictionarySave,6,0,1,0)

        dictionaryGrid.setRowStretch(7,0)

        self.lbl_dictionaryH2 = QtGui.QLabel(self.groupBoxDictionary)
        self.lbl_dictionaryH2.setStyleSheet('font-weight: bold;')
        self.lbl_dictionaryH2.setObjectName(_fromUtf8("lbl_dictionaryH2"))
        dictionaryGrid.addWidget(self.lbl_dictionaryH2,8,0,2,0)

        self.lbl_dictionaryFileName = QtGui.QLabel(self.groupBoxDictionary)
        self.lbl_dictionaryFileName.setStyleSheet("border: 1px solid gray; background-color: white;")
        self.lbl_dictionaryFileName.setObjectName(_fromUtf8("lbl_dictionaryFileName"))
        dictionaryGrid.addWidget(self.lbl_dictionaryFileName,9,0,1,0)

        self.btn_openDictionary = QtGui.QPushButton(self.groupBoxDictionary)
        icon1 = QtGui.QIcon()
        if system() == 'Windows':
            icon1path = _fromUtf8("./pictures/file.png")
        else:
            icon1path = _fromUtf8("./pictures/file.svg")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)        
        self.btn_openDictionary.setIcon(icon1)
        self.btn_openDictionary.setIconSize(QtCore.QSize(24, 24))
        self.btn_openDictionary.setObjectName(_fromUtf8("btn_openDictionary"))
        dictionaryGrid.addWidget(self.btn_openDictionary,9,2)

# GROUPBOX - BOOKS
        booksGrid = QtGui.QGridLayout()
        self.groupBoxBooks.setLayout(booksGrid)

        self.btn_calculate = QtGui.QPushButton(self.groupBoxBooks)
        # icon1 = QtGui.QIcon()
        # if system() == 'Windows':
        #     icon1path = _fromUtf8("./pictures/add.png")
        # else:
        #     icon1path = _fromUtf8("./pictures/add.svg")
        # icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.btn_calculate.setIcon(icon1)
        # self.btn_calculate.setIconSize(QtCore.QSize(24, 24))
        self.btn_calculate.setObjectName(_fromUtf8("btn_calculate"))
        booksGrid.addWidget(self.btn_calculate,0,0)

        self.btn_saveSelectedBooks = QtGui.QPushButton(self.groupBoxBooks)
        # icon1 = QtGui.QIcon()
        # if system() == 'Windows':
        #     icon1path = _fromUtf8("./pictures/add.png")
        # else:
        #     icon1path = _fromUtf8("./pictures/add.svg")
        # icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.btn_saveSelectedBooks.setIcon(icon1)
        # self.btn_saveSelectedBooks.setIconSize(QtCore.QSize(24, 24))
        self.btn_saveSelectedBooks.setObjectName(_fromUtf8("btn_saveSelectedBooks"))
        booksGrid.addWidget(self.btn_saveSelectedBooks,0,1)

        self.btn_openVisualisationTool = QtGui.QPushButton(self.groupBoxBooks)
        # icon1 = QtGui.QIcon()
        # if system() == 'Windows':
        #     icon1path = _fromUtf8("./pictures/add.png")
        # else:
        #     icon1path = _fromUtf8("./pictures/add.svg")
        # icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.btn_openVisualisationTool.setIcon(icon1)
        # self.btn_openVisualisationTool.setIconSize(QtCore.QSize(24, 24))
        self.btn_openVisualisationTool.setObjectName(_fromUtf8("btn_openVisualisationTool"))
        booksGrid.addWidget(self.btn_openVisualisationTool,0,2)

        self.lst_books = QtGui.QListWidget(self.groupBoxBooks)
        # self.lst_data.setViewMode(QtGui.QListView.IconMode)
        booksGrid.addWidget(self.lst_books,1,0,2,0)

# GROUPBOX - ERRORS
        errorsGrid = QtGui.QGridLayout()
        self.groupBoxErrors.setLayout(errorsGrid)

        self.lbl_errors = QtGui.QLabel(self.groupBoxErrors)
        self.lbl_errors.setEnabled(True)
        self.lbl_errors.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setItalic(True)
        self.lbl_errors.setFont(font)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)
        self.lbl_errors.setPalette(palette)
        self.lbl_errors.setObjectName(_fromUtf8("lbl_errors"))
        errorsGrid.addWidget(self.lbl_errors,0,0)

        errorsGrid.setRowStretch(1,1)

# SET ALL THINGS UP:
        mainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        
        mainWindow.setWindowTitle(_translate("mainWindow", "python-MatchingPursuit -- main window", None))

        self.groupBoxData.setTitle(_translate("mainWindow"  , "Data", None))
        self.groupBoxDataInfo.setTitle(_translate("mainWindow", "Data specification", None))
        self.groupBoxAlgorithm.setTitle(_translate("mainWindow", "MP configuration", None))
        self.groupBoxDictionary.setTitle(_translate("mainWindow", "Dictionary configuration", None))
        self.groupBoxBooks.setTitle(_translate("mainWindow", "Results", None))
        self.groupBoxErrors.setTitle(_translate("mainWindow", "Informations", None))
        self.groupBoxErrors.setHidden(False)

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
        self.lbl_dictionaryH1.setText(_translate("mainWindow", "Generate a dictionary:", None))
        self.lbl_dictonaryDensity.setText(_translate("mainWindow", "Dictionary density:", None))
        self.lbl_minS.setText(_translate("mainWindow", "Min. width:", None))
        self.lbl_maxS.setText(_translate("mainWindow", "Max. width:", None))
        self.lbl_useAsym.setText(_translate("mainWindow", "Include asymetrics:", None))
        self.lbl_useRect.setText(_translate("mainWindow", "Include rectangularities:", None))
        self.lbl_dictionaryH2.setText(_translate("mainWindow", "Or load dictionary from a file:", None))
        self.lbl_errors.setText(_translate("mainWindow", "Some error", None))

        self.btn_addData.setText(_translate("mainWindow", "Add", None))
        self.btn_removeData.setText(_translate("mainWindow", "Remove", None))
        self.btn_settingsData.setText(_translate("mainWindow", "", None))
        self.btn_calculate.setText(_translate("mainWindow", "Run MP", None))
        self.btn_saveSelectedBooks.setText(_translate("mainWindow", "Save selected", None))
        self.btn_openVisualisationTool.setText(_translate("mainWindow", "Visualise", None))
        self.btn_dictionarySave.setText(_translate("mainWindow", "Generate and Save", None))

###################################################################################################################################################
###################################################################################################################################################

# class DragDropListWidget(QListWidget):
#     def __init__(self, type, parent=None):
#         super(DragDropListWidget, self).__init__(parent)
#         self.setAcceptDrops(True)
#         # self.setIconSize(QSize(72, 72))
 
#     def dragEnterEvent(self, event):
#         if event.mimeData().hasUrls():
#             event.accept()
#         else:
#             event.ignore()
 
#     def dragMoveEvent(self, event):
#         if event.mimeData().hasUrls():
#             event.setDropAction(Qt.CopyAction)
#             event.accept()
#         else:
#             event.ignore()
 
#     def dropEvent(self, event):
#         if event.mimeData().hasUrls():
#             event.setDropAction(Qt.CopyAction)
#             event.accept()
#             l = []
#             for url in event.mimeData().urls():
#                 l.append(str(url.toLocalFile()))
#             self.emit(SIGNAL("dropped"), l)
#         else:
#             event.ignore()

###################################################################################################################################################
###################################################################################################################################################

if __name__ == '__main__':
    print 'Using this class without it\'s functional part may be possible, but'
    print 'it would be completely useless.'
