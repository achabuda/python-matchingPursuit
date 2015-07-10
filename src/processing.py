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

import numpy as np
from scipy.signal import hilbert


def calculateMP(dictionary , signal , config):
	'''
	dictionary - pandas.DataFrame containing redundant base set of functions
	signal     - numpy.array containing signal to decompose
	config     - dict
	- 
	'''
	
	signal = initializeMP(signal)

	return signal

def initializeMP(signal):
	signal = hilbert(signal)
	signalRest   = signal
	signalEnergy = Energy(signal)
	out_book     = []
	siglen       = length(signal)
	env_part     = []
	subMaxDot    = []
	subMaxFreq   = []
	iteration    = 0
	print 'MP initialization - done'
	return signal


def calculateSignalEnergy(signal):
	return sum( signal * signal.conjugate() )
