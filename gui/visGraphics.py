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
# from platform import system
from dragAndDropListWidget_PYSIDE import DragDropListWidget_PYSIDE

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

        self.groupBoxSubControlls = QtGui.QGroupBox()
        self.groupBoxSubControlls.setObjectName(_fromUtf8("groupBoxSubControlls"))

# GLOBAL BUTTONS & OTHER CONTROLLS:
        icon1 = QtGui.QIcon()
        icon1path = _fromUtf8("./pictures/icon_save.png")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.btn_saveDecomp = QtGui.QPushButton()
        self.btn_saveDecomp.setIcon(icon1)
        self.btn_saveDecomp.setIconSize(QtCore.QSize(24, 24))
        self.btn_saveDecomp.setObjectName(_fromUtf8("btn_saveDecomp"))

        self.btn_saveWigner = QtGui.QPushButton()
        self.btn_saveWigner.setIcon(icon1)
        self.btn_saveWigner.setIconSize(QtCore.QSize(24, 24))
        self.btn_saveWigner.setObjectName(_fromUtf8("btn_saveWigner"))

        self.btn_saveAmplitude = QtGui.QPushButton()
        self.btn_saveAmplitude.setIcon(icon1)
        self.btn_saveAmplitude.setIconSize(QtCore.QSize(24, 24))
        self.btn_saveAmplitude.setObjectName(_fromUtf8("btn_saveAmplitude"))

        self.btn_saveAmplitudeAsArray = QtGui.QPushButton()
        self.btn_saveAmplitudeAsArray.setIcon(icon1)
        self.btn_saveAmplitudeAsArray.setIconSize(QtCore.QSize(24, 24))
        self.btn_saveAmplitudeAsArray.setObjectName(_fromUtf8("btn_saveAmplitudeAsArray"))

        self.btn_saveTopography = QtGui.QPushButton()
        self.btn_saveTopography.setIcon(icon1)
        self.btn_saveTopography.setIconSize(QtCore.QSize(24, 24))
        self.btn_saveTopography.setObjectName(_fromUtf8("btn_saveTopography"))

        # self.btn_complex = QtGui.QPushButton()
        # self.btn_complex.setObjectName(_fromUtf8("btn_complex"))

# GROUPBOX STATUS:
        self.statusLayout = QtGui.QGridLayout()

        self.lbl_atomType = QtGui.QLabel()
        self.lbl_atomType.setObjectName(_fromUtf8("lbl_atomType"))

        self.led_atomType = QtGui.QLineEdit()
        self.led_atomType.setObjectName(_fromUtf8("led_atomType"))
        self.led_atomType.setReadOnly(True)
        self.led_atomType.setAlignment(QtCore.Qt.AlignCenter)
        self.led_atomType.setStyleSheet("font: bold;")

        self.lbl_atomAmplitude = QtGui.QLabel()
        self.lbl_atomAmplitude.setObjectName(_fromUtf8("lbl_atomAmplitude"))

        self.led_atomAmplitude = QtGui.QLineEdit()
        self.led_atomAmplitude.setObjectName(_fromUtf8("led_atomAmplitude"))
        self.led_atomAmplitude.setReadOnly(True)
        self.led_atomAmplitude.setAlignment(QtCore.Qt.AlignCenter)
        self.led_atomAmplitude.setStyleSheet("font: bold;")

        self.lbl_atomWidth = QtGui.QLabel()
        self.lbl_atomWidth.setObjectName(_fromUtf8("lbl_atomWidth"))

        self.led_atomWidth = QtGui.QLineEdit()
        self.led_atomWidth.setObjectName(_fromUtf8("led_atomWidth"))
        self.led_atomWidth.setReadOnly(True)
        self.led_atomWidth.setAlignment(QtCore.Qt.AlignCenter)
        self.led_atomWidth.setStyleSheet("font: bold;")

        self.lbl_atomFrequency = QtGui.QLabel()
        self.lbl_atomFrequency.setObjectName(_fromUtf8("lbl_atomFrequency"))

        self.led_atomFrequency = QtGui.QLineEdit()
        self.led_atomFrequency.setObjectName(_fromUtf8("led_atomFrequency"))
        self.led_atomFrequency.setReadOnly(True)
        self.led_atomFrequency.setAlignment(QtCore.Qt.AlignCenter)
        self.led_atomFrequency.setStyleSheet("font: bold;")

        self.lbl_atomLatency = QtGui.QLabel()
        self.lbl_atomLatency.setObjectName(_fromUtf8("lbl_atomLatency"))

        self.led_atomLatency = QtGui.QLineEdit()
        self.led_atomLatency.setObjectName(_fromUtf8("led_atomLatency"))
        self.led_atomLatency.setReadOnly(True)
        self.led_atomLatency.setAlignment(QtCore.Qt.AlignCenter)
        self.led_atomLatency.setStyleSheet("font: bold;")

        self.lbl_atomStart = QtGui.QLabel()
        self.lbl_atomStart.setObjectName(_fromUtf8("lbl_atomStart"))

        self.led_atomStart = QtGui.QLineEdit()
        self.led_atomStart.setObjectName(_fromUtf8("led_atomStart"))
        self.led_atomStart.setReadOnly(True)
        self.led_atomStart.setAlignment(QtCore.Qt.AlignCenter)
        self.led_atomStart.setStyleSheet("font: bold;")

        self.lbl_atomEnd = QtGui.QLabel()
        self.lbl_atomEnd.setObjectName(_fromUtf8("lbl_atomEnd"))

        self.led_atomEnd = QtGui.QLineEdit()
        self.led_atomEnd.setObjectName(_fromUtf8("led_atomEnd"))
        self.led_atomEnd.setReadOnly(True)
        self.led_atomEnd.setAlignment(QtCore.Qt.AlignCenter)
        self.led_atomEnd.setStyleSheet("font: bold;")


        self.statusLayout.addWidget(self.lbl_atomType,1,0)
        self.statusLayout.addWidget(self.led_atomType,1,1)        

        self.statusLayout.addWidget(self.lbl_atomAmplitude,0,2)
        self.statusLayout.addWidget(self.led_atomAmplitude,0,3)
        self.statusLayout.addWidget(self.lbl_atomWidth,1,2)
        self.statusLayout.addWidget(self.led_atomWidth,1,3)
        self.statusLayout.addWidget(self.lbl_atomFrequency,2,2)
        self.statusLayout.addWidget(self.led_atomFrequency,2,3)

        self.statusLayout.addWidget(self.lbl_atomStart,0,4)
        self.statusLayout.addWidget(self.led_atomStart,0,5)
        self.statusLayout.addWidget(self.lbl_atomLatency,1,4)
        self.statusLayout.addWidget(self.led_atomLatency,1,5)
        self.statusLayout.addWidget(self.lbl_atomEnd,2,4)
        self.statusLayout.addWidget(self.led_atomEnd,2,5)

        self.statusLayout.setColumnStretch(6,1)

        self.groupBoxStatus.setLayout(self.statusLayout)

# GROUPBOX SUBCONTROLLS:
        subControllsLayout = QtGui.QGridLayout()

        self.lbl_mapFreqRange = QtGui.QLabel()
        self.lbl_mapFreqRange.setStyleSheet('font-weight: bold;')
        self.lbl_mapFreqRange.setObjectName(_fromUtf8("lbl_mapFreqRange"))

        self.lbl_mapFreqRangeMin = QtGui.QLabel()
        self.lbl_mapFreqRangeMin.setObjectName(_fromUtf8("lbl_mapFreqRangeMin"))

        self.hsb_mapFreqRangeMin = QtGui.QScrollBar()
        self.hsb_mapFreqRangeMin.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_mapFreqRangeMin.setObjectName(_fromUtf8("hsb_mapFreqRangeMin"))

        self.lbl_mapFreqRangeMinN = QtGui.QLabel()
        self.lbl_mapFreqRangeMinN.setObjectName(_fromUtf8("lbl_mapFreqRangeMinN"))

        self.lbl_mapFreqRangeMax = QtGui.QLabel()
        self.lbl_mapFreqRangeMax.setObjectName(_fromUtf8("lbl_mapFreqRangeMax"))

        self.hsb_mapFreqRangeMax = QtGui.QScrollBar()
        self.hsb_mapFreqRangeMax.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_mapFreqRangeMax.setObjectName(_fromUtf8("hsb_mapFreqRangeMax"))

        self.lbl_mapFreqRangeMaxN = QtGui.QLabel()
        self.lbl_mapFreqRangeMaxN.setObjectName(_fromUtf8("lbl_mapFreqRangeMaxN"))

        self.btn_map2sqrt = QtGui.QPushButton()
        self.btn_map2sqrt.setCheckable(True)
        self.btn_map2sqrt.setObjectName(_fromUtf8("lbl_map2sqrt"))

        self.btn_map2log = QtGui.QPushButton()
        self.btn_map2log.setCheckable(True)
        self.btn_map2log.setObjectName(_fromUtf8("lbl_map2log"))        

        subControllsLayout.addWidget(self.lbl_mapFreqRange , 0 , 1)
        subControllsLayout.addWidget(self.lbl_mapFreqRangeMin , 1 , 0)
        subControllsLayout.addWidget(self.hsb_mapFreqRangeMin , 1 , 1)
        subControllsLayout.addWidget(self.lbl_mapFreqRangeMinN , 1 , 2)
        subControllsLayout.addWidget(self.lbl_mapFreqRangeMax , 2 , 0)
        subControllsLayout.addWidget(self.hsb_mapFreqRangeMax , 2 , 1)
        subControllsLayout.addWidget(self.lbl_mapFreqRangeMaxN , 2 , 2)

        subControllsLayout.addWidget(self.btn_map2sqrt , 0 , 3)
        subControllsLayout.addWidget(self.btn_map2log , 0 , 4)

        subControllsLayout.setColumnStretch(0,1)
        subControllsLayout.setColumnStretch(1,2)
        subControllsLayout.setColumnStretch(2,1)
        subControllsLayout.setColumnStretch(3,1)
        subControllsLayout.setColumnStretch(4,1)
        subControllsLayout.setColumnStretch(5,5)

        self.groupBoxSubControlls.setLayout(subControllsLayout)

# GROUPBOX BOOKS:
        booksLayout = QtGui.QVBoxLayout()
        booksButtonsLayout = QtGui.QHBoxLayout()
        
        self.lst_books = DragDropListWidget_PYSIDE(QtGui.QMainWindow)
        
        self.btn_add = QtGui.QPushButton(self.groupBoxBooks)
        icon1 = QtGui.QIcon()
        icon1path = _fromUtf8("./pictures/icon_add.png")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add.setIcon(icon1)
        self.btn_add.setIconSize(QtCore.QSize(24, 24))
        self.btn_add.setObjectName(_fromUtf8("btn_add"))

        self.btn_remove = QtGui.QPushButton(self.groupBoxBooks)
        icon1 = QtGui.QIcon()
        icon1path = _fromUtf8("./pictures/icon_remove.png")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_remove.setIcon(icon1)
        self.btn_remove.setIconSize(QtCore.QSize(24, 24))
        self.btn_remove.setObjectName(_fromUtf8("btn_remove"))

        self.btn_saveBook = QtGui.QPushButton(self.groupBoxBooks)
        icon1 = QtGui.QIcon()
        icon1path = _fromUtf8("./pictures/icon_save.png")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_saveBook.setIcon(icon1)
        self.btn_saveBook.setIconSize(QtCore.QSize(24, 24))
        self.btn_saveBook.setObjectName(_fromUtf8("btn_saveBook"))

        booksButtonsLayout.addWidget(self.btn_add)
        booksButtonsLayout.addWidget(self.btn_remove)
        booksButtonsLayout.addWidget(self.btn_saveBook)

        booksLayout.addLayout(booksButtonsLayout)
        booksLayout.addWidget(self.lst_books)

        self.groupBoxBooks.setLayout(booksLayout)

# GROUPBOX SETTINGS:
        settingsLayout             = QtGui.QVBoxLayout()
        settingsControllsLayout    = QtGui.QGridLayout()
        settingsFiltersLayout      = QtGui.QVBoxLayout()
        
        self.lbl_channel = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_channel.setObjectName(_fromUtf8("lbl_channel"))

        self.btn_channelPrev = QtGui.QPushButton(self.groupBoxSettings)
        self.btn_channelPrev.setObjectName(_fromUtf8("btn_channelPrev"))

        self.led_channel = QtGui.QLineEdit(self.groupBoxSettings)
        self.led_channel.setAlignment(QtCore.Qt.AlignCenter)
        self.led_channel.setObjectName(_fromUtf8("led_channel"))

        self.lbl_channelMax = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_channelMax.setObjectName(_fromUtf8("lbl_channelMax"))

        self.btn_channelNext = QtGui.QPushButton(self.groupBoxSettings)
        self.btn_channelNext.setObjectName(_fromUtf8("btn_channelNext"))

        settingsControllsLayout.addWidget(self.lbl_channel ,0,0)
        settingsControllsLayout.addWidget(self.btn_channelPrev ,0,1)
        settingsControllsLayout.addWidget(self.led_channel ,0,2)
        settingsControllsLayout.addWidget(self.lbl_channelMax ,0,3)
        settingsControllsLayout.addWidget(self.btn_channelNext ,0,4)

        self.lbl_trial = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_trial.setObjectName(_fromUtf8("lbl_trial"))

        self.btn_trialPrev = QtGui.QPushButton(self.groupBoxSettings)
        self.btn_trialPrev.setObjectName(_fromUtf8("btn_trialPrev"))

        self.led_trial = QtGui.QLineEdit(self.groupBoxSettings)
        self.led_trial.setAlignment(QtCore.Qt.AlignCenter)
        self.led_trial.setObjectName(_fromUtf8("led_trial"))

        self.lbl_trialMax = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_trialMax.setObjectName(_fromUtf8("lbl_trialMax"))

        self.btn_trialNext = QtGui.QPushButton(self.groupBoxSettings)
        self.btn_trialNext.setObjectName(_fromUtf8("btn_trialNext"))

        settingsControllsLayout.addWidget(self.lbl_trial ,1,0)
        settingsControllsLayout.addWidget(self.btn_trialPrev ,1,1)
        settingsControllsLayout.addWidget(self.led_trial ,1,2)
        settingsControllsLayout.addWidget(self.lbl_trialMax ,1,3)
        settingsControllsLayout.addWidget(self.btn_trialNext ,1,4)

        self.lbl_atom = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_atom.setObjectName(_fromUtf8("lbl_atom"))

        self.btn_atomPrev = QtGui.QPushButton(self.groupBoxSettings)
        self.btn_atomPrev.setObjectName(_fromUtf8("btn_atomPrev"))

        self.led_atom = QtGui.QLineEdit(self.groupBoxSettings)
        self.led_atom.setAlignment(QtCore.Qt.AlignCenter)
        self.led_atom.setObjectName(_fromUtf8("led_atom"))

        self.lbl_atomMax = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_atomMax.setObjectName(_fromUtf8("lbl_atomMax"))

        self.btn_atomNext = QtGui.QPushButton(self.groupBoxSettings)
        self.btn_atomNext.setObjectName(_fromUtf8("btn_atomNext"))

        settingsControllsLayout.addWidget(self.lbl_atom ,2,0)
        settingsControllsLayout.addWidget(self.btn_atomPrev ,2,1)
        settingsControllsLayout.addWidget(self.led_atom ,2,2)
        settingsControllsLayout.addWidget(self.lbl_atomMax ,2,3)
        settingsControllsLayout.addWidget(self.btn_atomNext ,2,4)



        settingsFiltersLayout.addSpacing(50)

        self.lbl_structAmplitudeRange = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structAmplitudeRange.setStyleSheet('font-weight: bold;')
        self.lbl_structAmplitudeRange.setObjectName(_fromUtf8("lbl_structAmplitudeRange"))

        settingsFiltersLayout.addWidget(self.lbl_structAmplitudeRange)

        self.lbl_structAmplitudeRangeMin = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structAmplitudeRangeMin.setObjectName(_fromUtf8("lbl_structAmplitudeRangeMin"))

        self.hsb_structAmplitudeRangeMin = QtGui.QScrollBar(self.groupBoxSettings)
        self.hsb_structAmplitudeRangeMin.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_structAmplitudeRangeMin.setObjectName(_fromUtf8("hsb_structAmplitudeRangeMin"))

        self.lbl_structAmplitudeRangeMinN = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structAmplitudeRangeMinN.setObjectName(_fromUtf8("lbl_structAmplitudeRangeMinN"))

        settingsFiltersSubLayout = QtGui.QHBoxLayout()
        settingsFiltersSubLayout.addWidget(self.lbl_structAmplitudeRangeMin)
        settingsFiltersSubLayout.addWidget(self.hsb_structAmplitudeRangeMin)
        settingsFiltersSubLayout.addWidget(self.lbl_structAmplitudeRangeMinN)
        settingsFiltersSubLayout.setStretch(0,2)
        settingsFiltersSubLayout.setStretch(1,3)
        settingsFiltersSubLayout.setStretch(2,1)
        settingsFiltersLayout.addLayout(settingsFiltersSubLayout)

        self.lbl_structAmplitudeRangeMax = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structAmplitudeRangeMax.setObjectName(_fromUtf8("lbl_structAmplitudeRangeMax"))

        self.hsb_structAmplitudeRangeMax = QtGui.QScrollBar(self.groupBoxSettings)
        self.hsb_structAmplitudeRangeMax.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_structAmplitudeRangeMax.setObjectName(_fromUtf8("hsb_structAmplitudeRangeMax"))

        self.lbl_structAmplitudeRangeMaxN = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structAmplitudeRangeMaxN.setObjectName(_fromUtf8("lbl_structAmplitudeRangeMaxN"))

        settingsFiltersSubLayout = QtGui.QHBoxLayout()
        settingsFiltersSubLayout.addWidget(self.lbl_structAmplitudeRangeMax)
        settingsFiltersSubLayout.addWidget(self.hsb_structAmplitudeRangeMax)
        settingsFiltersSubLayout.addWidget(self.lbl_structAmplitudeRangeMaxN)
        settingsFiltersSubLayout.setStretch(0,2)
        settingsFiltersSubLayout.setStretch(1,3)
        settingsFiltersSubLayout.setStretch(2,1)
        settingsFiltersLayout.addLayout(settingsFiltersSubLayout)

        settingsFiltersLayout.addSpacing(20)

        self.lbl_structPositionRange = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structPositionRange.setStyleSheet('font-weight: bold;')
        self.lbl_structPositionRange.setObjectName(_fromUtf8("lbl_structPositionRange"))

        settingsFiltersLayout.addWidget(self.lbl_structPositionRange)

        self.lbl_structPositionRangeMin = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structPositionRangeMin.setObjectName(_fromUtf8("lbl_structPositionRangeMin"))

        self.hsb_structPositionRangeMin = QtGui.QScrollBar(self.groupBoxSettings)
        self.hsb_structPositionRangeMin.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_structPositionRangeMin.setObjectName(_fromUtf8("hsb_structPositionRangeMin"))

        self.lbl_structPositionRangeMinN = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structPositionRangeMinN.setObjectName(_fromUtf8("lbl_structPositionRangeMinN"))

        settingsFiltersSubLayout = QtGui.QHBoxLayout()
        settingsFiltersSubLayout.addWidget(self.lbl_structPositionRangeMin)
        settingsFiltersSubLayout.addWidget(self.hsb_structPositionRangeMin)
        settingsFiltersSubLayout.addWidget(self.lbl_structPositionRangeMinN)
        settingsFiltersSubLayout.setStretch(0,2)
        settingsFiltersSubLayout.setStretch(1,3)
        settingsFiltersSubLayout.setStretch(2,1)
        settingsFiltersLayout.addLayout(settingsFiltersSubLayout)

        self.lbl_structPositionRangeMax = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structPositionRangeMax.setObjectName(_fromUtf8("lbl_structPositionRangeMax"))

        self.hsb_structPositionRangeMax = QtGui.QScrollBar(self.groupBoxSettings)
        self.hsb_structPositionRangeMax.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_structPositionRangeMax.setObjectName(_fromUtf8("hsb_structPositionRangeMax"))

        self.lbl_structPositionRangeMaxN = QtGui.QLabel(self.groupBoxSettings)
        self.lbl_structPositionRangeMaxN.setObjectName(_fromUtf8("lbl_structPositionRangeMaxN"))

        settingsFiltersSubLayout = QtGui.QHBoxLayout()
        settingsFiltersSubLayout.addWidget(self.lbl_structPositionRangeMax)
        settingsFiltersSubLayout.addWidget(self.hsb_structPositionRangeMax)
        settingsFiltersSubLayout.addWidget(self.lbl_structPositionRangeMaxN)
        settingsFiltersSubLayout.setStretch(0,2)
        settingsFiltersSubLayout.setStretch(1,3)
        settingsFiltersSubLayout.setStretch(2,1)
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
        settingsFiltersSubLayout.setStretch(0,2)
        settingsFiltersSubLayout.setStretch(1,3)
        settingsFiltersSubLayout.setStretch(2,1)
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
        settingsFiltersSubLayout.setStretch(0,2)
        settingsFiltersSubLayout.setStretch(1,3)
        settingsFiltersSubLayout.setStretch(2,1)
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
        settingsFiltersSubLayout.setStretch(0,2)
        settingsFiltersSubLayout.setStretch(1,3)
        settingsFiltersSubLayout.setStretch(2,1)
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
        settingsFiltersSubLayout.setStretch(0,2)
        settingsFiltersSubLayout.setStretch(1,3)
        settingsFiltersSubLayout.setStretch(2,1)
        settingsFiltersLayout.addLayout(settingsFiltersSubLayout)

        self.btn_apply = QtGui.QPushButton(self.groupBoxSettings)
        icon1 = QtGui.QIcon()
        icon1path = _fromUtf8("./pictures/icon_apply.png")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_apply.setIcon(icon1)
        self.btn_apply.setIconSize(QtCore.QSize(24, 24))
        self.btn_apply.setObjectName(_fromUtf8("btn_apply"))

        self.btn_reset = QtGui.QPushButton(self.groupBoxSettings)
        icon1 = QtGui.QIcon()
        icon1path = _fromUtf8("./pictures/icon_reset.png")
        icon1.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_reset.setIcon(icon1)
        self.btn_reset.setIconSize(QtCore.QSize(24, 24))
        self.btn_reset.setObjectName(_fromUtf8("btn_reset"))

        settingsFiltersSubLayout = QtGui.QHBoxLayout()
        settingsFiltersSubLayout.addStretch(1)
        settingsFiltersSubLayout.addWidget(self.btn_apply)
        settingsFiltersSubLayout.addStretch(1)
        settingsFiltersSubLayout.addWidget(self.btn_reset)
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

        tab_amplitudeRepresentation = QtGui.QWidget()
        self.layout2 = QtGui.QVBoxLayout(tab_amplitudeRepresentation)
        self.layout2.addWidget(self.groupBoxSubControlls)
        subLayout2 = QtGui.QHBoxLayout()
        subLayout2.addWidget(self.btn_saveAmplitude)
        subLayout2.addWidget(self.btn_saveAmplitudeAsArray)
        # subLayout2.addWidget(self.btn_complex)
        subLayout2.addStretch(1)
        self.layout2.addLayout(subLayout2)
        self.tabSpace.addTab(tab_amplitudeRepresentation, "Amplitude map")

        # tab_wvRepresentation = QtGui.QWidget()
        # self.layout3 = QtGui.QVBoxLayout(tab_wvRepresentation)
        # subLayout3 = QtGui.QHBoxLayout()
        # subLayout3.addWidget(self.btn_saveWigner)
        # subLayout3.addStretch(1)
        # self.layout3.addLayout(subLayout3)
        # self.tabSpace.addTab(tab_wvRepresentation, "Wigner-Ville map")

        # tab_topographicalRepresentation = QtGui.QWidget()
        # self.layout4 = QtGui.QVBoxLayout(tab_topographicalRepresentation)
        # subLayout4 = QtGui.QHBoxLayout()
        # subLayout4.addWidget(self.btn_saveTopography)
        # subLayout4.addStretch(1)
        # self.layout4.addLayout(subLayout4)
        # self.tabSpace.addTab(tab_topographicalRepresentation, "Topography")


# SET ALL THINGS UP:
        leftPanel.addWidget(self.groupBoxBooks)
        leftPanel.addSpacing(25)
        leftPanel.addWidget(self.groupBoxSettings)

        rightPanel.addWidget(self.tabSpace)

        mainLayout.addLayout(leftPanel)
        mainLayout.addLayout(rightPanel)
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,5)

        self.centralwidget.setLayout(mainLayout)
        visWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(visWindow)
        QtCore.QMetaObject.connectSlotsByName(visWindow)

    def retranslateUi(self, visWindow):
        
        visWindow.setWindowTitle(_translate("visWindow", "python-MatchingPursuit -- visualiser", None))

        self.groupBoxBooks.setTitle(_translate("visWindow"  , "Books", None))
        self.groupBoxStatus.setTitle(_translate("visWindow"  , "Atom parmeters", None))
        self.groupBoxSettings.setTitle(_translate("visWindow"  , "Settings", None))
        self.groupBoxSubControlls.setTitle(_translate("visWindow"  , "", None))

        self.btn_saveDecomp.setText(_translate("visWindow", "Picture", None))
        self.btn_saveAmplitude.setText(_translate("visWindow", "Picture", None))
        self.btn_saveAmplitudeAsArray.setText(_translate("visWindow", "Array", None))
        self.btn_saveWigner.setText(_translate("visWindow", "Save", None))
        self.btn_saveTopography.setText(_translate("visWindow", "Save", None))
        # self.btn_complex.setText(_translate("visWindow", "Draw complex maps", None))
        self.btn_add.setText(_translate("visWindow", "Add", None))
        self.btn_remove.setText(_translate("visWindow", "Remove", None))
        self.btn_saveBook.setText(_translate("visWindow", "Save", None))
        self.btn_trialNext.setText(_translate("visWindow", ">", None))
        self.btn_trialPrev.setText(_translate("visWindow", "<", None))
        self.btn_channelNext.setText(_translate("visWindow", ">", None))
        self.btn_channelPrev.setText(_translate("visWindow", "<", None))
        self.btn_atomNext.setText(_translate("visWindow", ">", None))
        self.btn_atomPrev.setText(_translate("visWindow", "<", None))
        self.btn_apply.setText(_translate("visWindow", "Apply", None))
        self.btn_reset.setText(_translate("visWindow", "Reset", None))
        self.btn_map2log.setText(_translate("visWindow", "> Logarithm", None))
        self.btn_map2sqrt.setText(_translate("visWindow", "> Sqrt", None))

        self.lbl_trial.setText(_translate("visWindow", "Trial:", None))
        self.lbl_trialMax.setText(_translate("visWindow", "/tr", None))
        self.lbl_channel.setText(_translate("visWindow", "Channel:", None))
        self.lbl_channelMax.setText(_translate("visWindow", "/ch", None))
        self.lbl_atom.setText(_translate("visWindow", "Atom:", None))
        self.lbl_atomMax.setText(_translate("visWindow", "/at", None))
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
        self.lbl_structWidthRange.setText(_translate("visWindow", "Structures widths range", None))
        self.lbl_structWidthRangeMin.setText(_translate("visWindow", "Lower limit [s]:", None))
        self.lbl_structWidthRangeMinN.setText(_translate("visWindow", "xx", None))
        self.lbl_structWidthRangeMax.setText(_translate("visWindow", "Upper limit [s]:", None))
        self.lbl_structWidthRangeMaxN.setText(_translate("visWindow", "yy", None))
        self.lbl_structAmplitudeRange.setText(_translate("visWindow", "Structures amplitudes range", None))
        self.lbl_structAmplitudeRangeMin.setText(_translate("visWindow", "Lower limit [au]:", None))
        self.lbl_structAmplitudeRangeMinN.setText(_translate("visWindow", "xx", None))
        self.lbl_structAmplitudeRangeMax.setText(_translate("visWindow", "Upper limit [au]:", None))
        self.lbl_structAmplitudeRangeMaxN.setText(_translate("visWindow", "yy", None))
        self.lbl_structPositionRange.setText(_translate("visWindow", "Structures positions range", None))
        self.lbl_structPositionRangeMin.setText(_translate("visWindow", "Lower limit [s]:", None))
        self.lbl_structPositionRangeMinN.setText(_translate("visWindow", "xx", None))
        self.lbl_structPositionRangeMax.setText(_translate("visWindow", "Upper limit [s]:", None))
        self.lbl_structPositionRangeMaxN.setText(_translate("visWindow", "yy", None))
        self.lbl_atomType.setText(_translate("visWindow", "Atom type:", None))
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