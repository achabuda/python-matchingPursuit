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

# drawing tools imports #
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4'] = 'PySide'
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib        import gridspec, ticker


# libraries imports #
from PySide    import QtGui, QtCore
from weakref   import proxy
from functools import partial
from platform  import system
from os.path   import expanduser
import numpy    as np
# import pandas as pd
import pickle


# gui imports #
from visGraphics import visWindowUI


# modules imports #
from src.drawing import calculateTFMap , getAtomReconstruction
from src.utils   import saveBookAsMat


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

			self.decompositionPlot = PlotterDecomposition(self.ui)
			self.amplitudeMapPlot  = PlotterAmplitudeMap(self.ui)
			
			self.setVariables()
			self.setWidgetsState()
		else:
			self.enableAllButtons(False)
			self.decompositionPlot = PlotterDecomposition(self.ui)
			self.amplitudeMapPlot  = PlotterAmplitudeMap(self.ui)
		
		self.decompositionPlot.binding_plotter_with_ui()
		self.amplitudeMapPlot.binding_plotter_with_ui()
		self.setConnections()

	def setVariables(self):
		self.trial     = 0
		self.channel   = 0
		self.atom      = 0

		self.atomTypes = {}
		self.atomTypes['11'] = 'Gabor function'
		self.atomTypes['21'] = 'Asymetric function'
		self.atomTypes['32'] = 'Tukey-based function'

		self.flags = {}
		self.flags['atom']    = 1
		self.flags['trial']   = 1
		self.flags['channel'] = 1

		try:
			self.nameOfBook = self.ui.lst_books.currentItem().text()
			self.channelsCalculated = self.books[self.nameOfBook]['config']['channels2calc']
			self.trialsCalculated   = self.books[self.nameOfBook]['config']['trials2calc']
		except AttributeError:
			# means that last book was removed from the list
			return

	def enableAllButtons(self , flag):
		self.ui.btn_remove.setEnabled(flag)
		self.ui.btn_saveBook.setEnabled(flag)
		self.ui.btn_channelNext.setEnabled(flag)
		self.ui.btn_channelPrev.setEnabled(flag)
		self.ui.btn_trialNext.setEnabled(flag)
		self.ui.btn_trialPrev.setEnabled(flag)
		self.ui.btn_atomNext.setEnabled(flag)
		self.ui.btn_atomPrev.setEnabled(flag)
		self.ui.btn_saveAmplitude.setEnabled(flag)
		self.ui.btn_reset.setEnabled(flag)
		self.ui.btn_apply.setEnabled(flag)
		self.ui.btn_saveDecomp.setEnabled(flag)
		self.ui.btn_saveAmplitudeAsArray.setEnabled(flag)

	def setConnections(self):
		self.ui.btn_atomNext.clicked.connect(self.nextAtom)
		self.ui.btn_atomPrev.clicked.connect(self.prevAtom)
		self.ui.btn_trialNext.clicked.connect(self.nextTrial)
		self.ui.btn_trialPrev.clicked.connect(self.prevTrial)
		self.ui.btn_channelNext.clicked.connect(self.nextChannel)
		self.ui.btn_channelPrev.clicked.connect(self.prevChannel)

		self.ui.btn_add.clicked.connect(self.addBooks)
		self.ui.btn_remove.clicked.connect(self.removeBook)
		self.ui.btn_saveBook.clicked.connect(self.saveBook)

		self.ui.btn_reset.clicked.connect(self.resetSliders)

		self.ui.btn_saveDecomp.clicked.connect(partial(self.saveFigure, 'decomposition'))
		self.ui.btn_saveAmplitude.clicked.connect(partial(self.saveFigure, 'amplitudeMap'))

		self.ui.btn_saveAmplitudeAsArray.clicked.connect(self.saveAmplitudeMapAsMatrix)

		self.ui.lst_books.currentItemChanged.connect(self.selectBook)
		self.ui.lst_books.sig_filesDropped.connect(self.dropBookFiles)

	def setWidgetsState(self , flag=1):
		if flag == 0:
			self.ui.led_atomType.setText('')
			self.ui.led_atomWidth.setText('')
			self.ui.led_atomFrequency.setText('')
			self.ui.led_atomAmplitude.setText('')
			self.ui.led_atomStart.setText('')
			self.ui.led_atomLatency.setText('')
			self.ui.led_atomEnd.setText('')
			self.ui.led_channel.setText('')
			self.ui.led_trial.setText('')
			self.ui.led_atom.setText('')
			self.ui.lbl_channelMax.setText('/ ch')
			self.ui.lbl_trialMax.setText('/ tr')
			self.ui.lbl_atomMax.setText('/ at')
			return

		self.determineRangesForHSBs()

		self.ui.led_atomType.setText( self.atomTypes[str( self.books[self.nameOfBook]['book'][self.trial,self.channel]['shapeType'][self.atom]) ])

		self.ui.led_trial.setText(str(self.trialsCalculated[self.trial]))
		self.ui.led_channel.setText(str(self.channelsCalculated[self.channel]))
		self.ui.led_atom.setText(str(self.atom+1))

		self.ui.lbl_trialMax.setText( '/'+str( self.trialsCalculated[-1:][0] ) )
		self.ui.lbl_channelMax.setText( '/'+str( self.channelsCalculated[-1:][0] ) )
		self.ui.lbl_atomMax.setText( '/ '+str(  self.books[self.nameOfBook]['book'][self.trial,self.channel].shape[0] ) )

		self.ui.led_atomWidth.setText(str(self.books[self.nameOfBook]['book'][self.trial,self.channel]['width'][self.atom]))
		self.ui.led_atomFrequency.setText(str(self.books[self.nameOfBook]['book'][self.trial,self.channel]['frequency'][self.atom]))
		self.ui.led_atomAmplitude.setText(str(self.books[self.nameOfBook]['book'][self.trial,self.channel]['amplitude'][self.atom]))

		self.ui.led_atomLatency.setText(str(self.books[self.nameOfBook]['book'][self.trial,self.channel]['atomLatency'][self.atom]))
		self.ui.led_atomStart.setText(str(self.books[self.nameOfBook]['book'][self.trial,self.channel]['atomStart'][self.atom]))
		self.ui.led_atomEnd.setText(str(self.books[self.nameOfBook]['book'][self.trial,self.channel]['atomEnd'][self.atom]))

		self.changeButtonsState()
		self.replot()

	def changeButtonsState(self):
		if self.ui.lst_books.count() == 0:
			self.enableAllButtons(False)
			return
		else:
			self.enableAllButtons(True)

		(maxTrial,maxChannel) = self.books[self.nameOfBook]['book'].shape
		maxAtom               = self.books[self.nameOfBook]['book'][self.trial,self.channel].shape[0]

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

	def determineRangesForHSBs(self):
		value_min = 0
		value_max = self.books[self.nameOfBook]['config']['samplingFrequency']
		self.ui.hsb_mapFreqRangeMin.setMinimum(value_min)
		self.ui.hsb_mapFreqRangeMin.setMaximum(value_max)
		self.ui.hsb_mapFreqRangeMin.setValue(value_min)
		self.ui.lbl_mapFreqRangeMinN.setText(str(value_min))
		self.ui.hsb_mapFreqRangeMax.setMinimum(value_min)
		self.ui.hsb_mapFreqRangeMax.setMaximum(value_max)
		self.ui.hsb_mapFreqRangeMax.setValue(value_max)
		self.ui.lbl_mapFreqRangeMaxN.setText(str(value_max))

		value_min = 0
		value_max = int(np.max(self.books[self.nameOfBook]['book'][self.trial,self.channel]['amplitude'])+1)
		self.ui.hsb_structAmplitudeRangeMin.setMinimum(value_min)
		self.ui.hsb_structAmplitudeRangeMin.setMaximum(value_max)
		self.ui.hsb_structAmplitudeRangeMin.setValue(value_min)
		self.ui.lbl_structAmplitudeRangeMinN.setText(str(value_min))
		self.ui.hsb_structAmplitudeRangeMax.setMinimum(value_min)
		self.ui.hsb_structAmplitudeRangeMax.setMaximum(value_max)
		self.ui.hsb_structAmplitudeRangeMax.setValue(value_max)
		self.ui.lbl_structAmplitudeRangeMaxN.setText(str(value_max))

		value_min = 0
		value_max = self.books[self.nameOfBook]['originalData'].shape[2] / self.books[self.nameOfBook]['config']['samplingFrequency']
		self.ui.hsb_structPositionRangeMin.setMinimum(value_min)
		self.ui.hsb_structPositionRangeMin.setMaximum(value_max)
		self.ui.hsb_structPositionRangeMin.setValue(value_min)
		self.ui.lbl_structPositionRangeMinN.setText(str(value_min))
		self.ui.hsb_structPositionRangeMax.setMinimum(value_min)
		self.ui.hsb_structPositionRangeMax.setMaximum(value_max)
		self.ui.hsb_structPositionRangeMax.setValue(value_max)
		self.ui.lbl_structPositionRangeMaxN.setText(str(value_max))

		value_min = 0
		value_max = self.books[self.nameOfBook]['config']['samplingFrequency']
		self.ui.hsb_structFreqRangeMin.setMinimum(value_min)
		self.ui.hsb_structFreqRangeMin.setMaximum(value_max)
		self.ui.hsb_structFreqRangeMin.setValue(value_min)
		self.ui.lbl_structFreqRangeMinN.setText(str(value_min))
		self.ui.hsb_structFreqRangeMax.setMinimum(value_min)
		self.ui.hsb_structFreqRangeMax.setMaximum(value_max)
		self.ui.hsb_structFreqRangeMax.setValue(value_max)
		self.ui.lbl_structFreqRangeMaxN.setText(str(value_max))

		value_min = self.books[self.nameOfBook]['config']['minS'] / self.books[self.nameOfBook]['config']['samplingFrequency']
		value_max = self.books[self.nameOfBook]['config']['maxS'] / self.books[self.nameOfBook]['config']['samplingFrequency']
		self.ui.hsb_structWidthRangeMin.setMinimum(value_min)
		self.ui.hsb_structWidthRangeMin.setMaximum(value_max)
		self.ui.hsb_structWidthRangeMin.setValue(value_min)
		self.ui.lbl_structWidthRangeMinN.setText(str(value_min))
		self.ui.hsb_structWidthRangeMax.setMinimum(value_min)
		self.ui.hsb_structWidthRangeMax.setMaximum(value_max)
		self.ui.hsb_structWidthRangeMax.setValue(value_max)
		self.ui.lbl_structWidthRangeMaxN.setText(str(value_max))

	def saveAmplitudeMapAsMatrix(self):
		nameOfBook = str(self.ui.lst_books.currentItem().text())

		whereFrom  = nameOfBook.rfind('/')
		whereTo    = nameOfBook.rfind('.')
		whereBOOK  = nameOfBook.rfind('_BOOK')
		nameOfBook = nameOfBook[whereFrom:whereTo]
		
		fileName = QtGui.QFileDialog.getSaveFileName(self , 'Save map array to file' , expanduser('~') + nameOfBook , 'Python pickles (*.p);;')

		if len(fileName[0]) == 0:
			return

		fileName = str(fileName[0])
		if fileName[-2:] == '.p':
			with open(fileName , 'wb') as f:
				pickle.dump({'arrayMap' : self.TFmap, 'time' : self.T , 'freqs' : self.F} , f)

	def saveFigure(self , which):
		nameOfBook = str(self.ui.lst_books.currentItem().text())

		whereFrom  = nameOfBook.rfind('/')
		whereTo    = nameOfBook.rfind('.')
		whereBOOK  = nameOfBook.rfind('_BOOK')
		nameOfBook = nameOfBook[whereFrom:whereTo]
		
		fileName = QtGui.QFileDialog.getSaveFileName(self , 'Save decomposition figure' , expanduser('~') + nameOfBook , 'Portable Network Graphics (*.png);;Scalable Vector Graphics (*.svg);;Portable Document Format (*.pdf);;')

		if len(fileName[0]) == 0:
			return
		
		fileName = str(fileName[0])
		
		if which == 'decomposition':
			self.decompositionPlot.fig.savefig(fileName , dpi=300)
		elif which == 'amplitudeMap':
			self.amplitudeMapPlot.fig.savefig(fileName , dpi=300)

	def resetSliders(self):
		self.determineRangesForHSBs()
		self.replot()

	def closeEvent(self, event):
		self.sig_windowClosed.emit()

	def selectBook(self):
		self.setVariables()
		self.setWidgetsState()
		self.changeButtonsState()

	def nextAtom(self):
		self.flags['atom'] = 1
		self.atom += 1
		self.setWidgetsState()

	def prevAtom(self):
		self.flags['atom'] = 1
		self.atom -= 1
		self.setWidgetsState()

	def nextChannel(self):
		self.flags['channel'] = 1
		self.flags['atom']    = 1
		self.channel += 1
		self.atom     = 0
		self.setWidgetsState()

	def prevChannel(self):
		self.flags['channel'] = 1
		self.flags['atom']    = 1
		self.channel -= 1
		self.atom     = 0
		self.setWidgetsState()

	def nextTrial(self):
		self.flags['trial'] = 1
		self.flags['atom']  = 1
		self.trial += 1
		self.atom   = 0
		self.setWidgetsState()

	def prevTrial(self):
		self.flags['trial'] = 1
		self.flags['atom']  = 1
		self.trial -= 1
		self.atom   = 0
		self.setWidgetsState()

	def replot(self):
		time     = np.arange(0,self.books[self.nameOfBook]['originalData'].shape[2]) / self.books[self.nameOfBook]['config']['samplingFrequency']
		tmp_time = np.arange(0,self.books[self.nameOfBook]['originalData'].shape[2])

		x_fromWhere = 0
		x_toWhere   = self.books[self.nameOfBook]['originalData'].shape[2] / self.books[self.nameOfBook]['config']['samplingFrequency']
		
		if self.flags['channel'] == 1 or self.flags['trial'] == 1:
			self.decompositionPlot.ax1.plot(time , np.squeeze(self.books[self.nameOfBook]['originalData'][self.trialsCalculated[self.trial]-1,self.channelsCalculated[self.channel]-1,:]) , 'k')
			self.decompositionPlot.ax1.set_title('Original signal')
			self.decompositionPlot.ax1.hold(False)
			self.decompositionPlot.ax1.set_ylabel(r'Amplitude [au]')
			self.decompositionPlot.ax1.set_xlim([x_fromWhere , x_toWhere])
			(y_fromWhere,y_toWhere) = self.decompositionPlot.ax1.get_ylim()

			reconstruction = np.zeros(tmp_time.shape)
			for (index,atom) in self.books[self.nameOfBook]['book'][self.trial,self.channel].iterrows():
				reconstruction += getAtomReconstruction(atom , tmp_time)

			self.decompositionPlot.ax2.plot(time , reconstruction , 'k')
			self.decompositionPlot.ax2.set_xlim([x_fromWhere , x_toWhere])
			self.decompositionPlot.ax2.set_ylim([y_fromWhere , y_toWhere])
			self.decompositionPlot.ax2.set_title('Decomposition')
			self.decompositionPlot.ax2.hold(False)
			self.decompositionPlot.ax2.set_ylabel(r'Amplitude [au]')

		if self.flags['atom'] == 1:
			func = getAtomReconstruction(self.books[self.nameOfBook]['book'][self.trial,self.channel].iloc[self.atom] , tmp_time)
			self.decompositionPlot.ax3.plot(time , func , 'k')
			self.decompositionPlot.ax3.set_xlim([x_fromWhere , x_toWhere])
			(y_fromWhere,y_toWhere) = self.decompositionPlot.ax1.get_ylim()
			self.decompositionPlot.ax3.set_ylim([y_fromWhere , y_toWhere])
			self.decompositionPlot.ax3.set_title('Single function')
			self.decompositionPlot.ax3.hold(False)
			self.decompositionPlot.ax3.set_ylabel(r'Amplitude [au]')
			self.decompositionPlot.ax3.set_xlabel(r'Time [s]')
		
		self.decompositionPlot.draw()

		if self.flags['channel'] == 1 or self.flags['trial'] == 1:
			(self.T,self.F,self.TFmap) = calculateTFMap(self.books[self.nameOfBook]['book'][self.trial,self.channel] , tmp_time , self.books[self.nameOfBook]['config']['samplingFrequency'] , 0)

			self.amplitudeMapPlot.ax0.imshow(np.abs(self.TFmap) , aspect='auto' , origin='lower' , extent=[x_fromWhere,x_toWhere , 0.0,self.books[self.nameOfBook]['config']['samplingFrequency']/2.])
			self.amplitudeMapPlot.ax0.hold(False)
			self.amplitudeMapPlot.ax0.set_ylabel(r'Frequency [Hz]')

			self.amplitudeMapPlot.ax1.clear()
			self.amplitudeMapPlot.ax1.plot(time , np.squeeze(self.books[self.nameOfBook]['originalData'][self.trialsCalculated[self.trial]-1,self.channelsCalculated[self.channel]-1,:]) , 'k')
			self.amplitudeMapPlot.ax1.plot(time , reconstruction , 'r')
			self.amplitudeMapPlot.ax1.set_xlim([x_fromWhere , x_toWhere])
			self.amplitudeMapPlot.ax1.set_ylabel(r'Amplitude [au]')
			(y_fromWhere,y_toWhere) = self.amplitudeMapPlot.ax1.get_ylim()

		if self.flags['atom'] == 1:
			self.amplitudeMapPlot.ax2.plot(time , func , 'r')
			self.amplitudeMapPlot.ax2.set_xlim([x_fromWhere , x_toWhere])
			self.amplitudeMapPlot.ax2.set_ylim([y_fromWhere , y_toWhere])
			self.amplitudeMapPlot.ax2.hold(False)
			self.amplitudeMapPlot.ax2.set_xlabel(r'Time [s]')
			self.amplitudeMapPlot.ax2.set_ylabel(r'Amplitude [au]')

		self.amplitudeMapPlot.draw()
		self.flags['atom']    = 0
		self.flags['channel'] = 0
		self.flags['trial']   = 0

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

	def removeBook(self):
		nameOfBook = self.ui.lst_books.currentItem().text()

		item = self.ui.lst_books.takeItem(self.ui.lst_books.currentRow())
		item = None
		del self.books[nameOfBook]

		if self.ui.lst_books.count() > 0:
			self.setVariables()
			self.setWidgetsState()
		else:
			self.decompositionPlot.ax1.clear()
			self.decompositionPlot.ax2.clear()
			self.decompositionPlot.ax3.clear()
			self.decompositionPlot.draw()

			self.amplitudeMapPlot.ax0.clear()
			self.amplitudeMapPlot.ax1.clear()
			self.amplitudeMapPlot.ax2.clear()
			self.amplitudeMapPlot.draw()

			self.setWidgetsState(0)
			self.enableAllButtons(False)

	def saveBook(self):
		data = self.books[self.nameOfBook]['originalData']
		book = self.books[self.nameOfBook]['book']
		conf = self.books[self.nameOfBook]['config']

		whereDot = self.nameOfBook.rfind('.')

		fileName = QtGui.QFileDialog.getSaveFileName(self , 'Save book file' , expanduser('~')+self.nameOfBook[:whereDot] , 'Python pickle (*.p);;Matlab file (*.mat);;')
		
		if len(fileName[0]) == 0:
			return

		bookFileName = str(fileName[0])
		whereDot = bookFileName.rfind('.')
		bookFileName = bookFileName[:whereDot]

		if fileName[1][-3:-1] == '.p':
			with open(bookFileName+'.p' , 'wb') as f:
				pickle.dump({'book':book,'config':conf,'originalData':data} , f)
		elif fileName[1][-5:-1] == '.mat':
			msg = saveBookAsMat(book , data , conf , bookFileName+'.mat')

	def dropBookFiles(self , listOfFiles):
		for filePath in listOfFiles:
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
		self.fig = Figure()
		super(PlotterDecomposition,self).__init__(self.fig)

		FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

		self.ax1 = self.fig.add_subplot(311)
		self.ax2 = self.fig.add_subplot(312)
		self.ax3 = self.fig.add_subplot(313)

    def binding_plotter_with_ui(self):
        self.parent.layout1.insertWidget(0, self)





class PlotterAmplitudeMap(FigureCanvas):
    def __init__(self, parent , book=[] , which=[0,0,0]):
		self.parent = proxy(parent)
		self.fig = Figure()
		super(PlotterAmplitudeMap,self).__init__(self.fig)

		FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

		gs = gridspec.GridSpec(3,1,height_ratios=[4,1,1])

		self.ax0 = self.fig.add_subplot(gs[0])
		self.ax1 = self.fig.add_subplot(gs[1])
		self.ax2 = self.fig.add_subplot(gs[2])

		self.fig.subplots_adjust(left=0.1, right=0.9)

    def binding_plotter_with_ui(self):
        self.parent.layout2.insertWidget(0, self)
