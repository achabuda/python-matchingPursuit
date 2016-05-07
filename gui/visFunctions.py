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

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4'] = 'PySide'
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from PySide import QtGui, QtCore

from weakref import proxy

# libraries imports #
import numpy     as np
import pandas    as pd
import pickle
from os.path   import expanduser

# gui imports #
from visGraphics import visWindowUI

# # modules imports #
# from src.utils      import generateRangeFromString, generateFinalConfig , retranslateDictionaryConfig
# from src.dictionary import generateDictionary
# from src.processing import calculateMP

class visWindow(QtGui.QMainWindow):
	sig_windowClosed   = QtCore.Signal()

	def __init__(self , inputs=[] , parent=None):
		QtGui.QMainWindow.__init__(self, parent)

		self.ui = visWindowUI()
		self.ui.setupUi(self)

		self.books = {}

		if inputs != []:
			for item in inputs.keys():
				self.ui.lst_books.addItem(item)
				self.books[item] = inputs[item]
			self.ui.lst_books.setCurrentRow(0)

			self.decompositionPlot = PlotterDecomposition(self.ui , self.books[str(self.ui.lst_books.currentItem().text())])
			self.amplitudeMapPlot  = PlotterAmplitudeMap(self.ui)
			self.setVariables()
			self.setWidgetsState()
		else:
			self.decompositionPlot = PlotterDecomposition(self.ui)
			self.amplitudeMapPlot  = PlotterAmplitudeMap(self.ui)
		
		self.decompositionPlot.binding_plotter_with_ui()
		self.amplitudeMapPlot.binding_plotter_with_ui()
		self.setConnections()

	def setVariables(self , flag = 0):
		self.trial     = 0
		self.channel   = 0
		self.atom      = 0

		self.nameOfBook = self.ui.lst_books.currentItem().text()

		self.atomTypes = {}
		self.atomTypes['11'] = 'Gabor function'
		self.atomTypes['21'] = 'Asymetric function'
		self.atomTypes['32'] = 'Tukey-based function'

		self.channelsCalculated = self.books[self.nameOfBook]['config']['channels2calc']
		self.trialsCalculated   = self.books[self.nameOfBook]['config']['trials2calc']

	def setConnections(self):
		self.ui.btn_atomNext.clicked.connect(self.nextAtom)
		self.ui.btn_atomPrev.clicked.connect(self.prevAtom)
		self.ui.btn_trialNext.clicked.connect(self.nextTrial)
		self.ui.btn_trialPrev.clicked.connect(self.prevTrial)
		self.ui.btn_channelNext.clicked.connect(self.nextChannel)
		self.ui.btn_channelPrev.clicked.connect(self.prevChannel)

		self.ui.btn_add.clicked.connect(self.addBooks)

		self.ui.lst_books.currentItemChanged.connect(self.selectBook)

	def setWidgetsState(self , flag=0):

		self.ui.led_atomType.setText( self.atomTypes[str( self.books[self.nameOfBook]['book'][self.trial,self.channel]['shapeType'][self.atom]) ])

		self.ui.led_trial.setText(str(self.trialsCalculated[self.trial]))
		self.ui.led_channel.setText(str(self.channelsCalculated[self.channel]))
		self.ui.led_atom.setText(str(self.atom+1))

		self.ui.led_atomWidth.setText(str(self.books[self.nameOfBook]['book'][self.trial,self.channel]['width'][self.atom]))
		self.ui.led_atomFrequency.setText(str(self.books[self.nameOfBook]['book'][self.trial,self.channel]['freq'][self.atom]))
		self.ui.led_atomAmplitude.setText(str(self.books[self.nameOfBook]['book'][self.trial,self.channel]['amplitude'][self.atom]))

		envelope  = self.books[self.nameOfBook]['book'][self.trial,self.channel]['envelope'][self.atom]
		whereMax  = np.argmax(envelope)
		threshold = 0.5
		where     =  np.where(envelope > threshold * envelope.max())[0] / self.books[self.nameOfBook]['config']['samplingFrequency']

		self.ui.led_atomStart.setText(str(where[0]))
		self.ui.led_atomEnd.setText(str(where[-1]))

		self.ui.led_atomLatency.setText( str(whereMax / self.books[self.nameOfBook]['config']['samplingFrequency']) )

		self.changeButtonsState()
		self.replot()

	def changeButtonsState(self):
		(maxTrial,maxChannel) = self.books[self.nameOfBook]['book'].shape
		maxAtom               = self.books[self.nameOfBook]['book'][self.trial,self.channel]['envelope'].shape[0]

		if self.atom == 0:
			self.ui.btn_atomPrev.setEnabled(False)
		else:
			self.ui.btn_atomPrev.setEnabled(True)

		if self.trial == 0:
			self.ui.btn_trialPrev.setEnabled(False)
		else:
			self.ui.btn_trialPrev.setEnabled(True)

		if self.channel == 0:
			self.ui.btn_channelPrev.setEnabled(False)
		else:
			self.ui.btn_channelPrev.setEnabled(True)


		if self.atom+1 == maxAtom:
			self.ui.btn_atomNext.setEnabled(False)
		else:
			self.ui.btn_atomNext.setEnabled(True)
		
		if self.channel+1 == maxChannel:
			self.ui.btn_channelNext.setEnabled(False)
		else:
			self.ui.btn_channelNext.setEnabled(True)

		if self.trial+1 == maxTrial:
			self.ui.btn_trialNext.setEnabled(False)
		else:
			self.ui.btn_trialNext.setEnabled(True)


	def closeEvent(self, event):
		self.sig_windowClosed.emit()

	def selectBook(self):
		self.setVariables()
		self.setWidgetsState()
		self.changeButtonsState()

	def nextAtom(self):
		self.atom += 1
		self.setWidgetsState(1)

	def prevAtom(self):
		self.atom -= 1
		self.setWidgetsState(1)

	def nextChannel(self):
		self.channel += 1
		self.atom     = 0
		self.setWidgetsState(1)

	def prevChannel(self):
		self.channel -= 1
		self.atom     = 0
		self.setWidgetsState(1)

	def nextTrial(self):
		self.trial += 1
		self.atom   = 0
		self.setWidgetsState(1)

	def prevTrial(self):
		self.trial -= 1
		self.atom   = 0
		self.setWidgetsState(1)

	def replot(self):
		self.decompositionPlot.ax1.plot(np.squeeze(self.books[self.nameOfBook]['originalData'][self.trialsCalculated[self.trial]-1,self.channelsCalculated[self.channel]-1,:]) , 'k')
		self.decompositionPlot.ax1.set_title('Original signal')
		self.decompositionPlot.ax1.hold(False)
		x_fromWhere = 0
		x_toWhere   = self.books[self.nameOfBook]['originalData'].shape[2]
		self.decompositionPlot.ax1.set_xlim([x_fromWhere , x_toWhere])
		(y_fromWhere,y_toWhere) = self.decompositionPlot.ax1.get_ylim()

		self.decompositionPlot.ax2.plot(np.squeeze(self.books[self.nameOfBook]['book'][self.trial,self.channel]['reconstruction'].sum()).real , 'k')
		self.decompositionPlot.ax2.set_xlim([x_fromWhere , x_toWhere])
		self.decompositionPlot.ax2.set_ylim([y_fromWhere , y_toWhere])
		self.decompositionPlot.ax2.set_title('Decomposition')
		self.decompositionPlot.ax2.hold(False)

		func = np.squeeze(self.books[self.nameOfBook]['book'][self.trial,self.channel]['reconstruction'][self.atom].real)
		self.decompositionPlot.ax3.plot(func , 'k')
		self.decompositionPlot.ax3.set_xlim([x_fromWhere , x_toWhere])
		self.decompositionPlot.ax3.set_ylim([y_fromWhere , y_toWhere])
		self.decompositionPlot.ax3.set_title('Single function')
		self.decompositionPlot.ax3.hold(False)
		
		self.decompositionPlot.draw()

	def addBooks(self):
		dialog = QtGui.QFileDialog.getOpenFileNames(self , 'Open book files' , expanduser('~') , 'Python pickles (*.p)')
		if len(dialog) == 0:
			return

		for filePath in dialog[0]:
			if filePath != '':
				if self.ui.lst_books.findItems(str(filePath) , QtCore.Qt.MatchExactly) != []:
					continue

				if filePath[-2:] == '.p':
					with open(filePath,'rb') as f:
						result = pickle.load(f)
					
					self.books[str(filePath)] = result

					item = QtGui.QListWidgetItem(str(filePath))
					self.ui.lst_books.addItem(item)
					self.ui.lst_books.setCurrentItem(item)
				else:
					pass

				self.setVariables()
				self.setWidgetsState()
			else:
				return
	
#######################################################################
#######################################################################

class PlotterDecomposition(FigureCanvas):
    def __init__(self, parent , book=[] , which=[0,0,0]):
		self.parent = proxy(parent)
		fig = Figure()
		super(PlotterDecomposition,self).__init__(fig)

		FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

		self.ax1 = fig.add_subplot(311)
		self.ax2 = fig.add_subplot(312)
		self.ax3 = fig.add_subplot(313)

		if book != []:
			x_fromWhere = 0
			x_toWhere   = book['originalData'].shape[2]

			self.ax1.hold(False)
			self.ax1.plot(np.squeeze(book['originalData'][which[0],which[1],:]) , 'k')
			self.ax1.set_title('Original signal')
			self.ax1.set_xlim([x_fromWhere , x_toWhere])

			(y_fromWhere,y_toWhere) = self.ax1.get_ylim()

			self.ax2.hold(False)
			self.ax2.plot(np.squeeze(book['book'][which[0],which[1]]['reconstruction'].sum()).real , 'k')
			self.ax2.set_title('Reconstruction')
			self.ax2.set_xlim([x_fromWhere , x_toWhere])
			self.ax2.set_ylim([y_fromWhere , y_toWhere])

			self.ax3.hold(False)
			self.ax3.plot(np.squeeze(book['book'][which[0],which[1]]['reconstruction'][which[2]].real) , 'k')
			self.ax3.set_title('Single function')
			self.ax3.set_xlim([x_fromWhere , x_toWhere])
			self.ax3.set_ylim([y_fromWhere , y_toWhere])


    def binding_plotter_with_ui(self):
        self.parent.layout1.insertWidget(0, self)





class PlotterAmplitudeMap(FigureCanvas):
    def __init__(self, parent , book=[] , which=[0,0,0]):
		self.parent = proxy(parent)
		fig = Figure()
		super(PlotterAmplitudeMap,self).__init__(fig)

		FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

		if book != []:
			pass

    def binding_plotter_with_ui(self):
        self.parent.layout2.insertWidget(0, self)
