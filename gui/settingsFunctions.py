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

# libraries imports #
import os
import time
from platform import system
from functools import partial
from PyQt4 import QtCore, QtGui

# gui imports #
from settingsGraphics import mainWindowUI

# modules imports #
# from saveAndLoadModule import loadDefaultValues, setDefaultSettings, saveSettings, loadSettings
# from processingModule  import processFile


class mainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        
        print '#################'
        print 'Application starting'
        
        print 'Window creation...'
        QtGui.QWidget.__init__(self, parent)
        self.ui = mainWindowUI()
        self.ui.setupUi(self)
        print 'done'

        print 'Variables initialization...'
        self.initializeFlags()
        self.setVariablesState(0)
        print 'done'
        
        print 'Signals and slots connecting...'
        self.setConnections()
        print 'done'
        
        print 'Application started'
        print '###################'
    
    def initializeFlags(self):
    	self.flags = {}
    	self.flags['groupBoxDataResized'] = 0

    def setVariablesState(self , flag):
   		print 'aaa'

    def setConnections(self):
    	self.ui.btn_settingsData.clicked.connect(self.resizeWindow)

    def resizeWindow(self):

    	self.animation = QtCore.QParallelAnimationGroup(self)
    	self.animation.finished.connect(self.setProperWindowSize)

    	self.animationWindow = QtCore.QPropertyAnimation(self, "size")
        self.animationWindow.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationWindow.setDuration(1000)

        self.animationGroupBoxBooks = QtCore.QPropertyAnimation(self.ui.groupBoxBooks, "geometry")
        self.animationGroupBoxBooks.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationGroupBoxBooks.setDuration(1000)        

        self.animationGroupBoxDataInfo = QtCore.QPropertyAnimation(self.ui.groupBoxDataInfo, "size")
        self.animationGroupBoxDataInfo.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationGroupBoxDataInfo.setDuration(1000)

        self.animationGroupBoxAlgorithm = QtCore.QPropertyAnimation(self.ui.groupBoxAlgorithm, "size")
        self.animationGroupBoxAlgorithm.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationGroupBoxAlgorithm.setDuration(1000)

        self.animationGroupBoxDictionary = QtCore.QPropertyAnimation(self.ui.groupBoxDictionary, "geometry")
        self.animationGroupBoxDataInfo.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationGroupBoxDataInfo.setDuration(1000)

        self.animationGroupBoxErrors = QtCore.QPropertyAnimation(self.ui.groupBoxErrors, "size")
        self.animationGroupBoxErrors.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationGroupBoxErrors.setDuration(1000)

        if self.flags['groupBoxDataResized'] == 0:
            self.animationWindow.setEndValue(QtCore.QSize(1000,450))
            self.animationGroupBoxBooks.setEndValue(QtCore.QRect(710,10,280,370))
            self.animationGroupBoxDataInfo.setEndValue(QtCore.QSize(180,140))
            self.animationGroupBoxAlgorithm.setEndValue(QtCore.QSize(180,220))
            self.animationGroupBoxErrors.setEndValue(QtCore.QSize(980,60))
            self.animationGroupBoxDictionary.setEndValue(QtCore.QRect(495,10,200,370))
            self.setMaximumSize(QtCore.QSize(1000, 450))
            self.flags['groupBoxDataResized'] = 1
        else:
            self.animationWindow.setEndValue(QtCore.QSize(600,450))
            self.animationGroupBoxBooks.setEndValue(QtCore.QRect(310,10,280,370))
            self.animationGroupBoxDataInfo.setEndValue(QtCore.QSize(0,140))
            self.animationGroupBoxAlgorithm.setEndValue(QtCore.QSize(0,220))
            self.animationGroupBoxErrors.setEndValue(QtCore.QSize(580,60))
            #self.animationGroupBoxDictionary.setEndValue(QtCore.QRect(305,10,0,370))
            self.animationGroupBoxDictionary.setEndValue(QtCore.QRect(495,10,0,370))
            self.setMinimumSize(QtCore.QSize(600, 450))
            self.flags['groupBoxDataResized'] = 0

        self.animation.addAnimation(self.animationWindow)
        self.animation.addAnimation(self.animationGroupBoxBooks)
        self.animation.addAnimation(self.animationGroupBoxDataInfo)
        self.animation.addAnimation(self.animationGroupBoxAlgorithm)
        self.animation.addAnimation(self.animationGroupBoxDictionary)
        self.animation.addAnimation(self.animationGroupBoxErrors)

        self.animation.start()

    def setProperWindowSize(self):
    	if self.flags['groupBoxDataResized'] == 0:
    		self.setMaximumSize(QtCore.QSize(600, 450))
    	else:
    		self.setMinimumSize(QtCore.QSize(1000, 450))


