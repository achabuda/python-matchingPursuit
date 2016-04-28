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
import numpy     as np
import pandas    as pd

from PyQt4        import QtCore, QtGui

# gui imports #
from calcGraphics import calcWindowUI

# modules imports #
from src.utils      import generateRangeFromString, generateFinalConfig , retranslateDictionaryConfig
from src.dictionary import generateDictionary
from src.processing import calculateMP

class calcWindow(QtGui.QMainWindow):
#class calcWindow(QtGui.QDialog):
	sig_singleBookDone       = QtCore.pyqtSignal(np.ndarray , dict , str)

	sig_calculationsStoped   = QtCore.pyqtSignal()
	sig_calculationsFinished = QtCore.pyqtSignal()

	def __init__(self, dataMatrixes , dictionaryConfig , parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint)

		self.ui = calcWindowUI()
		self.ui.setupUi(self)

		
		self.initializeFlags()
		self.initializeVariables(dataMatrixes , dictionaryConfig)

		self.mpThread = thr_MP(self.files2run , self.input , self.dictionary , self.dictionaryConfig)

		self.setConnections()

		self.setWidgetsInitialState()

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
		self.dictionary       = generateDictionary(self.timeVector , retranslateDictionaryConfig(self.dictionaryConfig))

	def setConnections(self):
		self.ui.btn_stop.clicked.connect(self.stopCalculations)

		self.mpThread.sig_lbl_file_update.connect(self.updateFileLabel)
		self.mpThread.sig_lbl_trial_update.connect(self.updateTrialLabel)
		self.mpThread.sig_lbl_channel_update.connect(self.updateChannelLabel)

		self.mpThread.sig_prb_file_update.connect(self.updateFileBar)
		self.mpThread.sig_prb_trial_update.connect(self.updateTrialBar)
		self.mpThread.sig_prb_channel_update.connect(self.updateChannelBar)

		self.mpThread.sig_prb_file_setMax.connect(self.setMaximumFileBar)
		self.mpThread.sig_prb_trial_setMax.connect(self.setMaximumTrialBar)
		self.mpThread.sig_prb_channel_setMax.connect(self.setMaximumChannelBar)

		self.mpThread.sig_singleBookDone.connect(self.mpThreadReturningSingleBook)
		self.mpThread.finished.connect(self.mpThreadFinished)

	def timerEvent(self):
		self.mpThread.start()

	def setWidgetsInitialState(self):
		self.timer = QtCore.QTimer()
		self.timer.setSingleShot(True)
		self.timer.timeout.connect(self.timerEvent)
		self.timer.start(500)

	def stopCalculations(self):
		self.flags['cancelClicked'] = 1
		self.mpThread.stop()

	def mpThreadFinished(self):
		self.sig_calculationsFinished.emit()
		self.close()

	def mpThreadReturningSingleBook(self, book , config , file2run):
		self.sig_singleBookDone.emit(book , config , file2run)

	def updateFileLabel(self , text):
		self.ui.lbl_file.setText(text)

	def updateTrialLabel(self , text):
		self.ui.lbl_trial.setText(text)

	def updateChannelLabel(self , text):
		self.ui.lbl_channel.setText(text)

	def updateFileBar(self , value):
		self.ui.prb_file.setValue(value)

	def updateTrialBar(self , value):
		self.ui.prb_trial.setValue(value)

	def updateChannelBar(self , value):
		self.ui.prb_channel.setValue(value)

	def setMaximumFileBar(self , value):
		self.ui.prb_file.setMaximum(value)

	def setMaximumChannelBar(self , value):
		self.ui.prb_channel.setMaximum(value)

	def setMaximumTrialBar(self , value):
		self.ui.prb_trial.setMaximum(value)


class thr_MP(QtCore.QThread):
	sig_lbl_file_update      = QtCore.pyqtSignal(str)
	sig_lbl_trial_update     = QtCore.pyqtSignal(str)
	sig_lbl_channel_update   = QtCore.pyqtSignal(str)

	sig_prb_file_update      = QtCore.pyqtSignal(int)
	sig_prb_trial_update     = QtCore.pyqtSignal(int)
	sig_prb_channel_update   = QtCore.pyqtSignal(int)

	sig_prb_file_setMax      = QtCore.pyqtSignal(int)
	sig_prb_trial_setMax     = QtCore.pyqtSignal(int)
	sig_prb_channel_setMax   = QtCore.pyqtSignal(int)

	sig_singleBookDone       = QtCore.pyqtSignal(np.ndarray , dict , str)

	def __init__(self , files2run , inputData , dictionary , dictionaryConfig , parent=None):
		QtCore.QThread.__init__(self, parent)

		self.input            = inputData
		self.files2run        = files2run
		self.dictionary       = dictionary
		self.dictionaryConfig = dictionaryConfig

		self.cancelClicked    = 0

	def run(self):
		self.sig_prb_file_setMax.emit(len(self.files2run))
		ind_file = 0
		self.sig_prb_file_update.emit(ind_file)
		self.sig_lbl_file_update.emit('Files - (' + str(ind_file) + ' / ' + str(len(self.files2run)) + ')')
		for file2run in self.files2run:
			dataMatrix      = self.input[file2run][0]
			dataInfo        = self.input[file2run][1]
			algorithmConfig = self.input[file2run][2]

			config = generateFinalConfig(self.dictionaryConfig , dataInfo , algorithmConfig)

			book = np.empty(shape=(len(config['trials2calc']),len(config['channels2calc'])) , dtype = pd.core.frame.DataFrame)

			self.sig_prb_channel_setMax.emit(len(config['channels2calc']))
			self.sig_prb_trial_setMax.emit(len(config['trials2calc']))

			ind_channel = 0
			self.sig_prb_channel_update.emit(ind_channel)
			self.sig_lbl_channel_update.emit('Channels - (' + str(ind_channel) + ' / ' + str(len(config['channels2calc'])) + ')')
			for channel in config['channels2calc']:
				ind_trial   = 0
				self.sig_prb_trial_update.emit(ind_trial)
				self.sig_lbl_trial_update.emit('Trials - (' + str(ind_trial) + ' / ' + str(len(config['trials2calc'])) + ')')
				for trial in config['trials2calc']:
					book[trial-1 , channel-1] = calculateMP(self.dictionary , np.squeeze(dataMatrix[trial-1,channel-1,:]) , config)
					ind_trial += 1
					self.sig_prb_trial_update.emit(ind_trial)
					self.sig_lbl_trial_update.emit('Trials - (' + str(ind_trial) + ' / ' + str(len(config['trials2calc'])) + ')')

					if self.cancelClicked == 1:
						return

				ind_channel += 1
				self.sig_prb_channel_update.emit(ind_channel)
				self.sig_lbl_channel_update.emit('Channels - (' + str(ind_channel) + ' / ' + str(len(config['channels2calc'])) + ')')

			ind_file += 1
			self.sig_prb_file_update.emit(ind_file)
			self.sig_lbl_file_update.emit('Files - (' + str(ind_file) + ' / ' + str(len(self.files2run)) + ')')

			self.sig_singleBookDone.emit(book , config , file2run)

	def stop(self):
		self.cancelClicked = 1
