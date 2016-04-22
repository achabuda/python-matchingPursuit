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
# import os
# import time
import numpy as np
import pandas as pd
# from platform  import system
# from functools import partial
# from scipy.io  import savemat
# from os.path   import expanduser
from PyQt4     import QtCore, QtGui
# from pickle    import dump

# gui imports #
from calcGraphics import calcWindowUI

# modules imports #
from src.utils      import generateRangeFromString, generateFinalConfig , retranslateDictionaryConfig
from src.dictionary import generateDictionary
from src.processing import calculateMP

class calcWindow(QtGui.QMainWindow):
	sig_calculationsStoped   = QtCore.pyqtSignal()
	sig_calculationsFinished = QtCore.pyqtSignal()
	sig_singleBookDone       = QtCore.pyqtSignal(np.ndarray , dict , str)

	def __init__(self, dataMatrixes , dictionaryConfig , parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = calcWindowUI()
		self.ui.setupUi(self)

		self.setConnections()
		self.initializeVariables(dataMatrixes , dictionaryConfig)
		self.initializeFlags()

		self.setWidgetsInitialState()

	def stopCalculations(self):
		self.flags['cancelClicked'] = 1

	def runCalculations(self):
		dictionary = generateDictionary(self.timeVector , retranslateDictionaryConfig(self.dictionaryConfig))

		self.ui.prb_file.setMaximum(len(self.files2run))
		ind_file = 0
		self.ui.prb_file.setValue(ind_file)
		self.ui.lbl_file.setText('Files - (' + str(ind_file) + ' / ' + str(len(self.files2run)) + ')')

		for file2run in self.files2run:
			dataMatrix      = self.input[file2run][0]
			dataInfo        = self.input[file2run][1]
			algorithmConfig = self.input[file2run][2]

			config = generateFinalConfig(self.dictionaryConfig , dataInfo , algorithmConfig)

			book = np.empty(shape=(len(config['trials2calc']),len(config['channels2calc'])) , dtype = pd.core.frame.DataFrame)

			self.ui.prb_channel.setMaximum(len(config['channels2calc']))
			self.ui.prb_trial.setMaximum(len(config['trials2calc']))

			ind_channel = 0
			self.ui.prb_channel.setValue(ind_channel)
			self.ui.lbl_channel.setText('Channels - (' + str(ind_channel) + ' / ' + str(len(config['channels2calc'])) + ')')
			for channel in config['channels2calc']:
				ind_trial   = 0
				self.ui.prb_trial.setValue(ind_trial)
				self.ui.lbl_trial.setText('Trials - (' + str(ind_trial) + ' / ' + str(len(config['trials2calc'])) + ')')
				for trial in config['trials2calc']:
					book[trial-1 , channel-1] = calculateMP(dictionary , np.squeeze(dataMatrix[trial-1,channel-1,:]) , config)
					ind_trial += 1
					self.ui.prb_trial.setValue(ind_trial)
					self.ui.lbl_trial.setText('Trials - (' + str(ind_trial) + ' / ' + str(len(config['trials2calc'])) + ')')
				ind_channel += 1
				self.ui.prb_channel.setValue(ind_channel)
				self.ui.lbl_channel.setText('Channels - (' + str(ind_channel) + ' / ' + str(len(config['channels2calc'])) + ')')

			ind_file += 1
			self.ui.prb_file.setValue(ind_file)
			self.ui.lbl_file.setText('Files - (' + str(ind_file) + ' / ' + str(len(self.files2run)) + ')')

			self.sig_singleBookDone.emit(book , config , file2run)

		self.sig_calculationsStoped.emit()
		self.close()
		
			# if self.flags['cancelClicked'] == 1:
			# 	self.calculationsStoped.emit()
			# 	self.close()

	def initializeFlags(self):
		self.flags = {}
		self.flags['cancelClicked'] = 0

	def initializeVariables(self , dataMatrixes , dictionaryConfig):
		self.input  = dataMatrixes
		self.output = []

		self.files2run     = self.input.keys()
		self.numberOfFiles = len(self.input)

		maximumLength = 0
		for f in self.files2run:
			if self.input[f][1]['numberOfSamples'] > maximumLength:
				maximumLength = self.input[f][1]['numberOfSamples']
		self.timeVector = np.arange(0,maximumLength)

		self.dictionaryConfig = dictionaryConfig

	def setConnections(self):
		self.ui.btn_stop.clicked.connect(self.stopCalculations)

	def timerEvent(self):
		self.runCalculations()

	def setWidgetsInitialState(self):
		self.timer = QtCore.QTimer()
		self.timer.setSingleShot(True)
		self.timer.timeout.connect(self.timerEvent)
		self.timer.start(1000)