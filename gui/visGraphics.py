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

from PySide   import QtGui, QtCore
# from PyQt4 import QtCore, QtGui
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


class visWindowUI(object):
    def setupUi(self , visWindow):
        visWindow.setObjectName(_fromUtf8("visWindow"))
        visWindow.setEnabled(True)
        # visWindow.resize(500 , 200)
        # visWindow.setMinimumSize(QtCore.QSize(500 , 200))
        # visWindow.setMaximumSize(QtCore.QSize(500 , 200))
        # visWindow.move(0,0)

# CENTRAL WIDGET:
        self.centralwidget   = QtGui.QWidget(visWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

# MAIN LAYOUTS:
        mainLayout = QtGui.QHBoxLayout()
        leftPanel  = QtGui.QVBoxLayout()
        rightPanel = QtGui.QVBoxLayout()

# GROUPBOXES:
        self.groupBoxBooks = QtGui.QGroupBox()
        self.groupBoxBooks.setObjectName(_fromUtf8("groupBoxBooks"))

        self.groupBoxSettings = QtGui.QGroupBox()
        self.groupBoxSettings.setObjectName(_fromUtf8("groupBoxSettings"))

        self.groupBoxStatus = QtGui.QGroupBox()
        self.groupBoxStatus.setObjectName(_fromUtf8("groupBoxStatus"))

        # self.groupBoxSubControlls= QtGui.QGroupBox()
        # self.groupBoxSubControlls.setObjectName(_fromUtf8("groupBoxSubControlls"))

# GLOBAL BUTTONS & OTHER CONTROLLS:
        self.btn_saveDecomp = QtGui.QPushButton()
        self.btn_saveDecomp.setObjectName(_fromUtf8("btn_saveDecomp"))

        self.btn_saveWigner = QtGui.QPushButton()
        self.btn_saveWigner.setObjectName(_fromUtf8("btn_saveWigner"))

        self.btn_saveAmplitude = QtGui.QPushButton()
        self.btn_saveAmplitude.setObjectName(_fromUtf8("btn_saveAmplitude"))

        self.btn_saveTopography = QtGui.QPushButton()
        self.btn_saveTopography.setObjectName(_fromUtf8("btn_saveTopography"))

        self.btn_complex = QtGui.QPushButton()
        self.btn_complex.setObjectName(_fromUtf8("btn_complex"))

# GROUPBOX STATUS:
        self.statusLayout = QtGui.QGridLayout()

        self.lbl_atomAmplitude = QtGui.QLabel()
        self.lbl_atomAmplitude.setObjectName(_fromUtf8("lbl_atomAmplitude"))

        self.led_atomAmplitude = QtGui.QLineEdit()
        self.led_atomAmplitude.setObjectName(_fromUtf8("led_atomAmplitude"))
        self.led_atomAmplitude.setEnabled(False)
        self.led_atomAmplitude.setAlignment(QtCore.Qt.AlignCenter)


        self.lbl_atomWidth = QtGui.QLabel()
        self.lbl_atomWidth.setObjectName(_fromUtf8("lbl_atomWidth"))

        self.led_atomWidth = QtGui.QLineEdit()
        self.led_atomWidth.setObjectName(_fromUtf8("led_atomWidth"))
        self.led_atomWidth.setEnabled(False)
        self.led_atomWidth.setAlignment(QtCore.Qt.AlignCenter)



        self.lbl_atomFrequency = QtGui.QLabel()
        self.lbl_atomFrequency.setObjectName(_fromUtf8("lbl_atomFrequency"))

        self.led_atomFrequency = QtGui.QLineEdit()
        self.led_atomFrequency.setObjectName(_fromUtf8("led_atomFrequency"))
        self.led_atomFrequency.setEnabled(False)
        self.led_atomFrequency.setAlignment(QtCore.Qt.AlignCenter)



        self.lbl_atomLatency = QtGui.QLabel()
        self.lbl_atomLatency.setObjectName(_fromUtf8("lbl_atomLatency"))

        self.led_atomLatency = QtGui.QLineEdit()
        self.led_atomLatency.setObjectName(_fromUtf8("led_atomLatency"))
        self.led_atomLatency.setEnabled(False)
        self.led_atomLatency.setAlignment(QtCore.Qt.AlignCenter)




        self.lbl_atomStart = QtGui.QLabel()
        self.lbl_atomStart.setObjectName(_fromUtf8("lbl_atomStart"))

        self.led_atomStart = QtGui.QLineEdit()
        self.led_atomStart.setObjectName(_fromUtf8("led_atomStart"))
        self.led_atomStart.setEnabled(False)
        self.led_atomStart.setAlignment(QtCore.Qt.AlignCenter)



        self.lbl_atomEnd = QtGui.QLabel()
        self.lbl_atomEnd.setObjectName(_fromUtf8("lbl_atomEnd"))

        self.led_atomEnd = QtGui.QLineEdit()
        self.led_atomEnd.setObjectName(_fromUtf8("led_atomEnd"))
        self.led_atomEnd.setEnabled(False)
        self.led_atomEnd.setAlignment(QtCore.Qt.AlignCenter)

        self.statusLayout.addWidget(self.lbl_atomAmplitude,0,0)
        self.statusLayout.addWidget(self.led_atomAmplitude,0,1)
        self.statusLayout.addWidget(self.lbl_atomWidth,1,0)
        self.statusLayout.addWidget(self.led_atomWidth,1,1)
        self.statusLayout.addWidget(self.lbl_atomFrequency,2,0)
        self.statusLayout.addWidget(self.led_atomFrequency,2,1)

        self.statusLayout.addWidget(self.lbl_atomStart,0,2)
        self.statusLayout.addWidget(self.led_atomStart,0,3)
        self.statusLayout.addWidget(self.lbl_atomLatency,1,2)
        self.statusLayout.addWidget(self.led_atomLatency,1,3)
        self.statusLayout.addWidget(self.lbl_atomEnd,2,2)
        self.statusLayout.addWidget(self.led_atomEnd,2,3)

        self.statusLayout.setColumnStretch(4,1)

        self.groupBoxStatus.setLayout(self.statusLayout)

# GROUPBOX BOOKS:
        booksLayout = QtGui.QVBoxLayout()
        booksButtonsLayout = QtGui.QHBoxLayout()
        
        self.lst_books = QtGui.QListWidget(self.groupBoxBooks)
        
        self.btn_add = QtGui.QPushButton(self.groupBoxBooks)
        self.btn_add.setObjectName(_fromUtf8("btn_add"))

        self.btn_remove = QtGui.QPushButton(self.groupBoxBooks)
        self.btn_remove.setObjectName(_fromUtf8("btn_remove"))

        booksButtonsLayout.addWidget(self.btn_add)
        booksButtonsLayout.addWidget(self.btn_remove)

        booksLayout.addLayout(booksButtonsLayout)
        booksLayout.addWidget(self.lst_books)

        self.groupBoxBooks.setLayout(booksLayout)

# GROUPBOX SETTINGS:
        settingsLayout             = QtGui.QVBoxLayout()
        settingsControllsLayout    = QtGui.QVBoxLayout()
        settingsFiltersLayout      = QtGui.QVBoxLayout()
        

        self.lbl_channel = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_channel.setObjectName(_fromUtf8("lbl_channel"))

        self.btn_channelPrev = QtGui.QPushButton(self.groupBoxSettings)
        self.btn_channelPrev.setObjectName(_fromUtf8("btn_channelPrev"))

        self.led_channel = QtGui.QLineEdit(self.groupBoxSettings)
        self.led_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.led_channel.setObjectName(_fromUtf8("led_channel"))

        self.btn_channelNext = QtGui.QPushButton(self.groupBoxSettings)
        self.btn_channelNext.setObjectName(_fromUtf8("btn_channelNext"))

        settingsControllsSubLayout = QtGui.QHBoxLayout()
        settingsControllsSubLayout.addWidget(self.lbl_channel)
        settingsControllsSubLayout.addStretch(1)
        settingsControllsSubLayout.addWidget(self.btn_channelPrev)
        settingsControllsSubLayout.addWidget(self.led_channel)
        settingsControllsSubLayout.addWidget(self.btn_channelNext)
        settingsControllsLayout.addLayout(settingsControllsSubLayout)

        self.lbl_trial = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_trial.setObjectName(_fromUtf8("lbl_trial"))

        self.btn_trialPrev = QtGui.QPushButton(self.groupBoxSettings)
        self.btn_trialPrev.setObjectName(_fromUtf8("btn_trialPrev"))

        self.led_trial = QtGui.QLineEdit(self.groupBoxSettings)
        self.led_trial.setAlignment(QtCore.Qt.AlignCenter)
        self.led_trial.setObjectName(_fromUtf8("led_trial"))

        self.btn_trialNext = QtGui.QPushButton(self.groupBoxSettings)
        self.btn_trialNext.setObjectName(_fromUtf8("btn_trialNext"))

        settingsControllsSubLayout = QtGui.QHBoxLayout()
        settingsControllsSubLayout.addWidget(self.lbl_trial)
        settingsControllsSubLayout.addStretch(1)
        settingsControllsSubLayout.addWidget(self.btn_trialPrev)
        settingsControllsSubLayout.addWidget(self.led_trial)
        settingsControllsSubLayout.addWidget(self.btn_trialNext)
        settingsControllsLayout.addLayout(settingsControllsSubLayout)

        self.lbl_atom = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_atom.setObjectName(_fromUtf8("lbl_atom"))

        self.btn_atomPrev = QtGui.QPushButton(self.groupBoxSettings)
        self.btn_atomPrev.setObjectName(_fromUtf8("btn_atomPrev"))

        self.led_atom = QtGui.QLineEdit(self.groupBoxSettings)
        self.led_atom.setAlignment(QtCore.Qt.AlignCenter)
        self.led_atom.setObjectName(_fromUtf8("led_atom"))

        self.btn_atomNext = QtGui.QPushButton(self.groupBoxSettings)
        self.btn_atomNext.setObjectName(_fromUtf8("btn_atomNext"))

        settingsControllsSubLayout = QtGui.QHBoxLayout()
        settingsControllsSubLayout.addWidget(self.lbl_atom)
        settingsControllsSubLayout.addStretch(1)
        settingsControllsSubLayout.addWidget(self.btn_atomPrev)
        settingsControllsSubLayout.addWidget(self.led_atom)
        settingsControllsSubLayout.addWidget(self.btn_atomNext)
        settingsControllsLayout.addLayout(settingsControllsSubLayout)


        settingsFiltersLayout.addSpacing(50)

        self.lbl_mapFreqRange = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_mapFreqRange.setStyleSheet('font-weight: bold;')
        self.lbl_mapFreqRange.setObjectName(_fromUtf8("lbl_mapFreqRange"))

        settingsFiltersLayout.addWidget(self.lbl_mapFreqRange)

        self.lbl_mapFreqRangeMin = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_mapFreqRangeMin.setObjectName(_fromUtf8("lbl_mapFreqRangeMin"))

        self.hsb_mapFreqRangeMin = QtGui.QScrollBar(self.groupBoxSettings)
        self.hsb_mapFreqRangeMin.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_mapFreqRangeMin.setMinimum(0)
        self.hsb_mapFreqRangeMin.setMaximum(100)
        self.hsb_mapFreqRangeMin.setObjectName(_fromUtf8("hsb_mapFreqRangeMin"))

        self.lbl_mapFreqRangeMinN = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_mapFreqRangeMinN.setObjectName(_fromUtf8("lbl_mapFreqRangeMinN"))

        settingsFiltersSubLayout = QtGui.QHBoxLayout()
        settingsFiltersSubLayout.addWidget(self.lbl_mapFreqRangeMin)
        settingsFiltersSubLayout.addWidget(self.hsb_mapFreqRangeMin)
        settingsFiltersSubLayout.addWidget(self.lbl_mapFreqRangeMinN)
        settingsFiltersLayout.addLayout(settingsFiltersSubLayout)

        self.lbl_mapFreqRangeMax = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_mapFreqRangeMax.setObjectName(_fromUtf8("lbl_mapFreqRangeMax"))

        self.hsb_mapFreqRangeMax = QtGui.QScrollBar(self.groupBoxSettings)
        self.hsb_mapFreqRangeMax.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_mapFreqRangeMax.setObjectName(_fromUtf8("hsb_mapFreqRangeMax"))

        self.lbl_mapFreqRangeMaxN = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_mapFreqRangeMaxN.setObjectName(_fromUtf8("lbl_mapFreqRangeMaxN"))

        settingsFiltersSubLayout = QtGui.QHBoxLayout()
        settingsFiltersSubLayout.addWidget(self.lbl_mapFreqRangeMax)
        settingsFiltersSubLayout.addWidget(self.hsb_mapFreqRangeMax)
        settingsFiltersSubLayout.addWidget(self.lbl_mapFreqRangeMaxN)
        settingsFiltersLayout.addLayout(settingsFiltersSubLayout)
        settingsFiltersLayout.addSpacing(20)

        self.lbl_structFreqRange = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structFreqRange.setStyleSheet('font-weight: bold;')
        self.lbl_structFreqRange.setObjectName(_fromUtf8("lbl_structFreqRange"))

        settingsFiltersLayout.addWidget(self.lbl_structFreqRange)

        self.lbl_structFreqRangeMin = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structFreqRangeMin.setObjectName(_fromUtf8("lbl_structFreqRangeMin"))

        self.hsb_structFreqRangeMin = QtGui.QScrollBar(self.groupBoxSettings)
        self.hsb_structFreqRangeMin.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_structFreqRangeMin.setObjectName(_fromUtf8("hsb_structFreqRangeMin"))

        self.lbl_structFreqRangeMinN = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structFreqRangeMinN.setObjectName(_fromUtf8("lbl_structFreqRangeMinN"))

        settingsFiltersSubLayout = QtGui.QHBoxLayout()
        settingsFiltersSubLayout.addWidget(self.lbl_structFreqRangeMin)
        settingsFiltersSubLayout.addWidget(self.hsb_structFreqRangeMin)
        settingsFiltersSubLayout.addWidget(self.lbl_structFreqRangeMinN)
        settingsFiltersLayout.addLayout(settingsFiltersSubLayout)

        self.lbl_structFreqRangeMax = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structFreqRangeMax.setObjectName(_fromUtf8("lbl_structFreqRangeMax"))

        self.hsb_structFreqRangeMax = QtGui.QScrollBar(self.groupBoxSettings)
        self.hsb_structFreqRangeMax.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_structFreqRangeMax.setObjectName(_fromUtf8("hsb_structFreqRangeMax"))

        self.lbl_structFreqRangeMaxN = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structFreqRangeMaxN.setObjectName(_fromUtf8("lbl_structFreqRangeMaxN"))

        settingsFiltersSubLayout = QtGui.QHBoxLayout()
        settingsFiltersSubLayout.addWidget(self.lbl_structFreqRangeMax)
        settingsFiltersSubLayout.addWidget(self.hsb_structFreqRangeMax)
        settingsFiltersSubLayout.addWidget(self.lbl_structFreqRangeMaxN)
        settingsFiltersLayout.addLayout(settingsFiltersSubLayout)
        settingsFiltersLayout.addSpacing(20)

        self.lbl_structWidthRange = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structWidthRange.setStyleSheet('font-weight: bold;')
        self.lbl_structWidthRange.setObjectName(_fromUtf8("lbl_structWidthRange"))

        settingsFiltersLayout.addWidget(self.lbl_structWidthRange)        

        self.lbl_structWidthRangeMin = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structWidthRangeMin.setObjectName(_fromUtf8("lbl_structWidthRangeMin"))

        self.hsb_structWidthRangeMin = QtGui.QScrollBar(self.groupBoxSettings)
        self.hsb_structWidthRangeMin.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_structWidthRangeMin.setObjectName(_fromUtf8("hsb_structWidthRangeMin"))

        self.lbl_structWidthRangeMinN = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structWidthRangeMinN.setObjectName(_fromUtf8("lbl_structWidthRangeMinN"))

        settingsFiltersSubLayout = QtGui.QHBoxLayout()
        settingsFiltersSubLayout.addWidget(self.lbl_structWidthRangeMin)
        settingsFiltersSubLayout.addWidget(self.hsb_structWidthRangeMin)
        settingsFiltersSubLayout.addWidget(self.lbl_structWidthRangeMinN)
        settingsFiltersLayout.addLayout(settingsFiltersSubLayout)

        self.lbl_structWidthRangeMax = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structWidthRangeMax.setObjectName(_fromUtf8("lbl_structWidthRangeMax"))

        self.hsb_structWidthRangeMax = QtGui.QScrollBar(self.groupBoxSettings)
        self.hsb_structWidthRangeMax.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_structWidthRangeMax.setObjectName(_fromUtf8("hsb_structWidthRangeMax"))

        self.lbl_structWidthRangeMaxN = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structWidthRangeMaxN.setObjectName(_fromUtf8("lbl_structWidthRangeMaxN"))

        settingsFiltersSubLayout = QtGui.QHBoxLayout()
        settingsFiltersSubLayout.addWidget(self.lbl_structWidthRangeMax)
        settingsFiltersSubLayout.addWidget(self.hsb_structWidthRangeMax)
        settingsFiltersSubLayout.addWidget(self.lbl_structWidthRangeMaxN)
        settingsFiltersLayout.addLayout(settingsFiltersSubLayout)

        self.btn_apply = QtGui.QPushButton(self.groupBoxSettings)
        self.btn_apply.setObjectName(_fromUtf8("btn_apply"))

        settingsFiltersSubLayout = QtGui.QHBoxLayout()
        settingsFiltersSubLayout.addStretch(1)
        settingsFiltersSubLayout.addWidget(self.btn_apply)
        settingsFiltersSubLayout.addStretch(1)
        settingsFiltersLayout.addSpacing(20)
        settingsFiltersLayout.addLayout(settingsFiltersSubLayout)

        settingsLayout.addLayout(settingsControllsLayout)
        settingsLayout.addSpacing(50)
        settingsLayout.addLayout(settingsFiltersLayout)
        self.groupBoxSettings.setLayout(settingsLayout)

# TABWIDGET & TABS:
        self.tabSpace = QtGui.QTabWidget()
        self.tabSpace.setTabsClosable(False)

        tab_decomposition = QtGui.QWidget()
        self.layout1 = QtGui.QVBoxLayout(tab_decomposition)
        self.layout1.addWidget(self.groupBoxStatus)
        subLayout1 = QtGui.QHBoxLayout()
        subLayout1.addWidget(self.btn_saveDecomp)
        subLayout1.addStretch(1)
        self.layout1.addLayout(subLayout1)
        self.tabSpace.addTab(tab_decomposition, "Decomposition")

        tab_wvRepresentation = QtGui.QWidget()
        self.layout2 = QtGui.QVBoxLayout(tab_wvRepresentation)
        subLayout2 = QtGui.QHBoxLayout()
        subLayout2.addWidget(self.btn_saveWigner)
        subLayout2.addStretch(1)
        self.layout2.addLayout(subLayout2)
        self.tabSpace.addTab(tab_wvRepresentation, "Wigner-Ville map")

        tab_amplitudeRepresentation = QtGui.QWidget()
        self.layout3 = QtGui.QVBoxLayout(tab_amplitudeRepresentation)
        subLayout3 = QtGui.QHBoxLayout()
        subLayout3.addWidget(self.btn_saveAmplitude)
        subLayout3.addWidget(self.btn_complex)
        subLayout3.addStretch(1)
        self.layout3.addLayout(subLayout3)
        self.tabSpace.addTab(tab_amplitudeRepresentation, "Amplitude map")

        tab_topographicalRepresentation = QtGui.QWidget()
        self.layout4 = QtGui.QVBoxLayout(tab_topographicalRepresentation)
        subLayout4 = QtGui.QHBoxLayout()
        subLayout4.addWidget(self.btn_saveTopography)
        subLayout4.addStretch(1)
        self.layout4.addLayout(subLayout4)
        self.tabSpace.addTab(tab_topographicalRepresentation, "Topography")


# SET ALL THINGS UP:
        leftPanel.addWidget(self.groupBoxBooks)
        leftPanel.addSpacing(25)
        leftPanel.addWidget(self.groupBoxSettings)

        rightPanel.addWidget(self.tabSpace)
        # rightPanel.addWidget(self.groupBoxSubControlls)
        # rightPanel.addWidget(self.groupBoxStatus)

        mainLayout.addLayout(leftPanel)
        mainLayout.addLayout(rightPanel)
        mainLayout.setStretch(1,3)

        self.centralwidget.setLayout(mainLayout)
        visWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(visWindow)
        QtCore.QMetaObject.connectSlotsByName(visWindow)

    def retranslateUi(self, visWindow):
        
        visWindow.setWindowTitle(_translate("visWindow", "python-MatchingPursuit -- visualiser", None))

        self.groupBoxBooks.setTitle(_translate("visWindow"  , "Books", None))
        # self.groupBoxStatus.setTitle(_translate("visWindow"  , "Status", None))
        self.groupBoxSettings.setTitle(_translate("visWindow"  , "Settings", None))
        # self.groupBoxSubControlls.setTitle(_translate("visWindow"  , "", None))

        self.btn_saveDecomp.setText(_translate("visWindow", "Save Picture", None))
        self.btn_saveAmplitude.setText(_translate("visWindow", "Save", None))
        self.btn_saveWigner.setText(_translate("visWindow", "Save", None))
        self.btn_saveTopography.setText(_translate("visWindow", "Save", None))
        self.btn_complex.setText(_translate("visWindow", "ComplexMap", None))
        self.btn_add.setText(_translate("visWindow", "Add", None))
        self.btn_remove.setText(_translate("visWindow", "Remove", None))
        self.btn_trialNext.setText(_translate("visWindow", ">", None))
        self.btn_trialPrev.setText(_translate("visWindow", "<", None))
        self.btn_channelNext.setText(_translate("visWindow", ">", None))
        self.btn_channelPrev.setText(_translate("visWindow", "<", None))
        self.btn_atomNext.setText(_translate("visWindow", ">", None))
        self.btn_atomPrev.setText(_translate("visWindow", "<", None))
        self.btn_apply.setText(_translate("visWindow", "Apply", None))

        self.lbl_trial.setText(_translate("visWindow", "Trial:", None))
        self.lbl_channel.setText(_translate("visWindow", "Channel:", None))
        self.lbl_atom.setText(_translate("visWindow", "Atom:", None))
        self.lbl_mapFreqRange.setText(_translate("visWindow", "Map frequency range", None))
        self.lbl_mapFreqRangeMin.setText(_translate("visWindow", "Lower limit [Hz]:", None))
        self.lbl_mapFreqRangeMinN.setText(_translate("visWindow", "xx", None))
        self.lbl_mapFreqRangeMax.setText(_translate("visWindow", "Upper limit [Hz]:", None))
        self.lbl_mapFreqRangeMaxN.setText(_translate("visWindow", "yy", None))
        self.lbl_structFreqRange.setText(_translate("visWindow", "Structures frequency range", None))
        self.lbl_structFreqRangeMin.setText(_translate("visWindow", "Lower limit [Hz]:", None))
        self.lbl_structFreqRangeMinN.setText(_translate("visWindow", "xx", None))
        self.lbl_structFreqRangeMax.setText(_translate("visWindow", "Upper limit [Hz]:", None))
        self.lbl_structFreqRangeMaxN.setText(_translate("visWindow", "yy", None))
        self.lbl_structWidthRange.setText(_translate("visWindow", "Structures width range", None))
        self.lbl_structWidthRangeMin.setText(_translate("visWindow", "Lower limit [s]:", None))
        self.lbl_structWidthRangeMinN.setText(_translate("visWindow", "xx", None))
        self.lbl_structWidthRangeMax.setText(_translate("visWindow", "Upper limit [s]:", None))
        self.lbl_structWidthRangeMaxN.setText(_translate("visWindow", "yy", None))
        self.lbl_atomAmplitude.setText(_translate("visWindow", "Amplitude [au]:", None))
        self.lbl_atomWidth.setText(_translate("visWindow", "Width [s]:", None))
        self.lbl_atomFrequency.setText(_translate("visWindow", "Frequency [Hz]:", None))
        self.lbl_atomStart.setText(_translate("visWindow", "AtomStart [s]:", None))
        self.lbl_atomLatency.setText(_translate("visWindow", "Latency [s]:", None))
        self.lbl_atomEnd.setText(_translate("visWindow", "AtomEnd [s]:", None))

###################################################################################################################################################
###################################################################################################################################################

if __name__ == '__main__':
    print 'Using this class without it\'s functional parts may be possible, but'
    print 'it would be completely useless.'