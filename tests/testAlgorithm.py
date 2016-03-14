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
import unittest

from src.dictionary       import generateDictionary
from data.signalGenerator import generateTestSignal , simpleValues , advancedValues , masterValues
from src.processing       import calculateMP

freqThreshold = 0.05
amplThreshold = 0.10


(gaborParams , sinusParams , asymetricParams , rectParams , noiseRatio , samplingFrequency , numberOfSamples) = simpleValues()
(signal,time) = generateTestSignal(gaborParams,sinusParams,asymetricParams,rectParams,numberOfSamples,samplingFrequency,noiseRatio)

# print gaborParams
# print '---'
# print sinusParams
# print '---'

flags = {}
flags['useAsymA'] = 0
flags['useRectA'] = 0
flags['useGradientOptimization']  = 1
flags['displayInfo']              = 0

config = {}
config['flags']                            = flags
config['algorithm']                        = 'smp'
config['minS']                             = 32
config['maxS']                             = numberOfSamples
config['density']                          = 0.01
config['maxNumberOfIterations']            = 3
config['minEnergyExplained']               = 0.99
config['samplingFrequency']                = samplingFrequency
config['minNFFT']                          = 2 * samplingFrequency

dictionary = generateDictionary(time , config)
book       = calculateMP(dictionary , signal , config)

# print book

class AlgorithmTest(unittest.TestCase):
	def test_simpleFirstIteration_frequency(self):
		'''
		Test for the very first iteration of the algorithm
		working on simple synthetic signal. Frequency check.
		'''
		self.assertTrue( (book['freq'][0] < sinusParams[0][1]*(1+freqThreshold)) and (book['freq'][0] > sinusParams[0][1]*(1-freqThreshold)) )
	def test_simpleFirstIteration_amplitude(self):
		'''
		Test for the very first iteration of the algorithm
		working on simple synthetic signal. Amplitude check.
		'''
		self.assertTrue( (np.abs(book['amplitude'][0]) < sinusParams[0][0]*(1+amplThreshold)) and (np.abs(book['amplitude'][0]) > sinusParams[0][0]*(1-amplThreshold)) )