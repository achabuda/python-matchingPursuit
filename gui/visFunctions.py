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
# from PyQt4 import QtCore, QtGui

import random

from weakref import proxy

# libraries imports #
import numpy     as np
import pandas    as pd

# gui imports #
from visGraphics import visWindowUI

# modules imports #
from src.utils      import generateRangeFromString, generateFinalConfig , retranslateDictionaryConfig
from src.dictionary import generateDictionary
from src.processing import calculateMP

class visWindow(QtGui.QMainWindow):
	sig_windowClosed   = QtCore.Signal()
	# sig_windowClosed   = QtCore.pyqtSignal()

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

			self.plotter = Plotter(self.ui , self.books[str(self.ui.lst_books.currentItem().text())])
		else:
			self.plotter = Plotter(self.ui)
		self.plotter.binding_plotter_with_ui(1)

	def closeEvent(self, event):
		self.sig_windowClosed.emit()

	
#######################################################################
#######################################################################

class Plotter(FigureCanvas):
    def __init__(self, parent , book=[]):
    	print len(book)

        self.parent = proxy(parent)
        
        # data = [random.random() for i in range(10)]
        # fig = Figure(figsize=(5, 5), dpi=100)
        fig = Figure()
        super(Plotter,self).__init__(fig)

        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        # create an axis
        self.axes = fig.add_subplot(111)
        
        # discards the old graph
        self.axes.hold(False)
        
        # plot data
        # self.axes.plot(data, '*-')

    def binding_plotter_with_ui(self,where):
    	if where == 1:
        	self.parent.layout1.insertWidget(0, self)
        elif where == 2:
        	self.parent.layout2.insertWidget(0, self)
        elif where == 3:
        	self.parent.layout3.insertWidget(0, self)
        elif where == 4:
        	self.parent.layout4.insertWidget(0, self)
