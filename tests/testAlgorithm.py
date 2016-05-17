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

(gaborParamsAdvanced , sinusParamsAdvanced , asymetricParamsAdvanced , rectParamsAdvanced , noiseRatio , samplingFrequency , numberOfSamples) = advancedValues()
(advancedSignal,time) = generateTestSignal(gaborParamsAdvanced,sinusParamsAdvanced,asymetricParamsAdvanced,rectParamsAdvanced,numberOfSamples,samplingFrequency,noiseRatio)

(gaborParamsMaster , sinusParamsMaster , asymetricParamsMaster , rectParamsMaster , noiseRatio , samplingFrequency , numberOfSamples) = masterValues()
(masterSignal,time) = generateTestSignal(gaborParamsMaster,sinusParamsMaster,asymetricParamsMaster,rectParamsMaster,numberOfSamples,samplingFrequency,noiseRatio)


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
config['maxNumberOfIterations']            = 4
config['minEnergyExplained']               = 0.99
config['samplingFrequency']                = samplingFrequency
config['minNFFT']                          = 2 * samplingFrequency

dictionary = generateDictionary(time , config)
book       = calculateMP(dictionary , signal , config)

flags = {}
flags['useAsymA'] = 1
flags['useRectA'] = 0
flags['useGradientOptimization']  = 1
flags['displayInfo']              = 0
config['flags']   = flags

advancedDictionary = generateDictionary(time , config)
advancedBook       = calculateMP(advancedDictionary , advancedSignal , config)

flags = {}
flags['useAsymA'] = 1
flags['useRectA'] = 1
flags['useGradientOptimization']  = 1
flags['displayInfo']              = 0
config['flags']   = flags

masterDictionary = generateDictionary(time , config)
masterBook       = calculateMP(masterDictionary , masterSignal , config)

# print masterBook

print 'Preparations done, proceeding to testing...'

class AlgorithmTest(unittest.TestCase):
	def test_simpleFirstIteration_atomType(self):
		'''
		Test for the very first iteration of the algorithm
		working on simple synthetic signal. AtomType check.
		It should be sinusoid, ie 11.
		'''
		self.assertEqual(book['shapeType'][0] , 11)
	def test_simpleFirstIteration_frequency(self):
		'''
		Test for the very first iteration of the algorithm
		working on simple synthetic signal. Frequency check.
		'''
		self.assertTrue( (book['frequency'][0] < sinusParams[0][1]*(1+freqThreshold)) and (book['frequency'][0] > sinusParams[0][1]*(1-freqThreshold)) )
	def test_simpleFirstIteration_amplitude(self):
		'''
		Test for the very first iteration of the algorithm
		working on simple synthetic signal. Amplitude check.
		'''
		self.assertTrue( (np.abs(book['amplitude'][0]) < sinusParams[0][0]*(1+amplThreshold)) and (np.abs(book['amplitude'][0]) > sinusParams[0][0]*(1-amplThreshold)) )
	def test_simpleSecondIteration_atomType(self):
		'''
		Test for the second iteration of the algorithm
		working on simple synthetic signal. AtomType check.
		It should be Gabor function, ie 11.
		It should be the second Gabor function present in
		the gaborParams set.
		'''
		self.assertEqual(book['shapeType'][1] , 11)
	def test_simpleSecondIteration_frequency(self):
		'''
		Test for the second iteration of the algorithm
		working on simple synthetic signal. Frequency check.
		It should be the second Gabor function present in
		the gaborParams set.
		'''
		self.assertTrue( (book['frequency'][1] < gaborParams[1][5]*(1+freqThreshold)) and (book['frequency'][1] > gaborParams[1][5]*(1-freqThreshold)) )
	def test_simpleFirstIteration_amplitude(self):
		'''
		Test for the second iteration of the algorithm
		working on simple synthetic signal. Amplitude check.
		It should be the second Gabor function present in
		the gaborParams set.
		'''
		self.assertTrue( (np.abs(book['amplitude'][1]) < gaborParams[1][2]*(1+amplThreshold)) and (np.abs(book['amplitude'][1]) > gaborParams[1][2]*(1-amplThreshold)) )
	def test_simpleThirdIteration_atomType(self):
		'''
		Test for the third iteration of the algorithm
		working on simple synthetic signal. AtomType check.
		It should be Gabor function, ie 11.
		It should be the first Gabor function present in
		the gaborParams set.
		'''
		self.assertEqual(book['shapeType'][2] , 11)
	def test_simpleThirdIteration_frequency(self):
		'''
		Test for the third iteration of the algorithm
		working on simple synthetic signal. Frequency check.
		It should be the first Gabor function present in
		the gaborParams set.
		'''
		self.assertTrue( (book['frequency'][2] < gaborParams[0][5]*(1+freqThreshold)) and (book['frequency'][2] > gaborParams[0][5]*(1-freqThreshold)) )
	def test_simpleThirdIteration_amplitude(self):
		'''
		Test for the third iteration of the algorithm
		working on simple synthetic signal. Amplitude check.
		It should be the first Gabor function present in
		the gaborParams set.
		'''
		self.assertTrue( (np.abs(book['amplitude'][2]) < gaborParams[0][2]*(1+amplThreshold)) and (np.abs(book['amplitude'][2]) > gaborParams[0][2]*(1-amplThreshold)) )

	def test_simpleForthIteration(self):
		'''
		Test for the forth iteration of the algorithm
		working on simple synthetic signal. In this case,
		there should only be three iterations.
		'''
		self.assertEqual(len(book.index) , 3)

	# -------------------------------------------------------------------- #
	# ------ simple ends here -------------------------------------------- #

	def test_advancedFirstIteration_atomType(self):
		'''
		Test for the very first iteration of the algorithm
		working on advanced synthetic signal. AtomType check.
		It should be asymetric envelope, ie 21.
		It should be the second asymetric function present in
		the asymetricParamsAdvanced set.
		'''
		self.assertEqual(advancedBook['shapeType'][0] , 21)
	def test_advancedFirstIteration_frequency(self):
		'''
		Test for the very first iteration of the algorithm
		working on advanced synthetic signal. Frequency check.
		It should be the second asymetric function present in
		the asymetricParamsAdvanced set.
		'''
		self.assertTrue( (advancedBook['frequency'][0] < asymetricParamsAdvanced[1][1]*(1+freqThreshold)) and (advancedBook['frequency'][0] > asymetricParamsAdvanced[1][1]*(1-freqThreshold)) )
	def test_advancedFirstIteration_amplitude(self):
		'''
		Test for the very first iteration of the algorithm
		working on advanced synthetic signal. Amplitude check.
		It should be the second asymetric function present in
		the asymetricParamsAdvanced set.
		'''
		self.assertTrue( (advancedBook['amplitude'][0] < asymetricParamsAdvanced[1][0]*(1+amplThreshold)) and (advancedBook['amplitude'][0] > asymetricParamsAdvanced[1][0]*(1-amplThreshold)) )
	def test_advancedSecondIteration_atomType(self):
		'''
		Test for the second iteration of the algorithm
		working on advanced synthetic signal. AtomType check.
		It should be asymetric envelope, ie 21.
		It should be the first asymetric function present in
		the asymetricParamsAdvanced set.
		'''
		self.assertEqual(advancedBook['shapeType'][1] , 21)
	def test_advancedSecondIteration_frequency(self):
		'''
		Test for the second iteration of the algorithm
		working on advanced synthetic signal. Frequency check.
		It should be the first asymetric function present in
		the asymetricParamsAdvanced set.
		'''
		self.assertTrue( (advancedBook['frequency'][1] < asymetricParamsAdvanced[0][1]*(1+freqThreshold)) and (advancedBook['frequency'][1] > asymetricParamsAdvanced[0][1]*(1-freqThreshold)) )
	def test_advancedSecondIteration_amplitude(self):
		'''
		Test for the second iteration of the algorithm
		working on advanced synthetic signal. Amplitude check.
		It should be the first asymetric function present in
		the asymetricParamsAdvanced set.
		'''
		self.assertTrue( (advancedBook['amplitude'][1] < asymetricParamsAdvanced[0][0]*(1+amplThreshold)) and (advancedBook['amplitude'][1] > asymetricParamsAdvanced[0][0]*(1-amplThreshold)) )
	def test_advancedThirdIteration_atomType(self):
		'''
		Test for the third iteration of the algorithm
		working on advanced synthetic signal. AtomType check.
		It should represent the sinus function present in
		sinusParamsAdvanced, but after previous iterations,
		it will most likely be represented by another asymetric
		function, ie shape type should be 21.
		'''
		self.assertEqual(advancedBook['shapeType'][2] , 21)
	def test_advancedThirdIteration_frequency(self):
		'''
		Test for the third iteration of the algorithm
		working on advanced synthetic signal. Frequency check.
		'''
		self.assertTrue( (advancedBook['frequency'][2] < sinusParamsAdvanced[0][1]*(1+freqThreshold)) and (advancedBook['frequency'][2] > sinusParamsAdvanced[0][1]*(1-freqThreshold)) )
	def test_advancedThirdIteration_amplitude(self):
		'''
		Test for the second iteration of the algorithm
		working on advanced synthetic signal. Amplitude check.
		'''
		self.assertTrue( (advancedBook['amplitude'][2] < sinusParamsAdvanced[0][0]*(1+amplThreshold)) and (advancedBook['amplitude'][2] > sinusParamsAdvanced[0][0]*(1-amplThreshold)) )
	def test_advancedForthIteration(self):
		'''
		Test for the forth iteration of the algorithm
		working on simple synthetic signal. In this case,
		there should only be three iterations.
		'''
		self.assertEqual(len(advancedBook.index) , 3)

	# -------------------------------------------------------------------- #
	# ------ advanced ends here ------------------------------------------ #

	def test_masterFirstIteration_atomType(self):
		'''
		Test for the very first iteration of the algorithm
		working on complicated case of a synthetic signal.
		AtomType check.
		It should be a symetric, rectangular envelope, 32 in this case.
		'''
		self.assertEqual(masterBook['shapeType'][0] , 32)
	def test_masterFirstIteration_frequency(self):
		'''
		Test for the very first iteration of the algorithm
		working on advanced synthetic signal. Frequency check.
		'''
		self.assertTrue( (masterBook['frequency'][0] < rectParamsMaster[0][1]*(1+freqThreshold)) and (masterBook['frequency'][0] > rectParamsMaster[0][1]*(1-freqThreshold)) )
	def test_masterFirstIteration_amplitude(self):
		'''
		Test for the very first iteration of the algorithm
		working on advanced synthetic signal. Amplitude check.
		'''
		self.assertTrue( (masterBook['amplitude'][0] < rectParamsMaster[0][0]*(1+amplThreshold)) and (masterBook['amplitude'][0] > rectParamsMaster[0][0]*(1-amplThreshold)) )
	def test_masterSecondIteration_atomType(self):
		'''
		Test for the second iteration of the algorithm
		working on complicated case of a synthetic signal.
		AtomType check.
		It should be asymetric envelope, 21 in this case.
		'''
		self.assertEqual(masterBook['shapeType'][1] , 21)
	def test_masterSecondIteration_frequency(self):
		'''
		Test for the second iteration of the algorithm
		working on advanced synthetic signal. Frequency check.
		'''
		self.assertTrue( (masterBook['frequency'][1] < asymetricParamsMaster[0][1]*(1+freqThreshold)) and (masterBook['frequency'][1] > asymetricParamsMaster[0][1]*(1-freqThreshold)) )
	def test_masterSecondIteration_amplitude(self):
		'''
		Test for the second iteration of the algorithm
		working on advanced synthetic signal. Amplitude check.
		'''
		self.assertTrue( (masterBook['amplitude'][1] < asymetricParamsMaster[0][0]*(1+amplThreshold)) and (masterBook['amplitude'][1] > asymetricParamsMaster[0][0]*(1-amplThreshold)) )
	def test_masterThirdIteration_atomType(self):
		'''
		Test for the third iteration of the algorithm
		working on complicated case of a synthetic signal.
		AtomType check.
		It should represent a Gabor function present in
		gaborParamsMaster, but after previous iterations,
		it will most likely be represented by slightly asymetric
		function, ie shape type should be 21.
		'''
		self.assertEqual(masterBook['shapeType'][2] , 21)
	def test_masterThirdIteration_frequency(self):
		'''
		Test for the third iteration of the algorithm
		working on advanced synthetic signal. Frequency check.
		'''
		self.assertTrue( (masterBook['frequency'][2] < gaborParamsMaster[0][5]*(1+freqThreshold)) and (masterBook['frequency'][2] > gaborParamsMaster[0][5]*(1-freqThreshold)) )
	def test_masterThirdIteration_amplitude(self):
		'''
		Test for the third iteration of the algorithm
		working on advanced synthetic signal. Amplitude check.
		'''
		self.assertTrue( (masterBook['amplitude'][2] < gaborParamsMaster[0][2]*(1+amplThreshold)) and (masterBook['amplitude'][2] > gaborParamsMaster[0][2]*(1-amplThreshold)) )
	def test_masterFourthIteration_atomType(self):
		'''
		Test for the fourth iteration of the algorithm
		working on complicated case of a synthetic signal.
		AtomType check.
		It should represent a sinusoid function present in
		sinusParamsMaster, but after previous iterations,
		it will most likely be represented by another asymetric
		function, ie shape type should be 21.
		'''
		self.assertEqual(masterBook['shapeType'][3] , 21)
	def test_masterThirdIteration_frequency(self):
		'''
		Test for the fourth iteration of the algorithm
		working on advanced synthetic signal. Frequency check.
		'''
		self.assertTrue( (masterBook['frequency'][3] < sinusParamsMaster[0][1]*(1+freqThreshold)) and (masterBook['frequency'][3] > sinusParamsMaster[0][1]*(1-freqThreshold)) )
	def test_masterThirdIteration_amplitude(self):
		'''
		Test for the fourth iteration of the algorithm
		working on advanced synthetic signal. Amplitude check.
		'''
		self.assertTrue( (masterBook['amplitude'][3] < sinusParamsMaster[0][0]*(1+amplThreshold)) and (masterBook['amplitude'][3] > sinusParamsMaster[0][0]*(1-amplThreshold)) )
	def test_masterFifthIteration(self):
		'''
		Test for the forth iteration of the algorithm
		working on simple synthetic signal. In this case,
		there should only be three iterations.
		'''
		self.assertEqual(len(masterBook.index) , 4)