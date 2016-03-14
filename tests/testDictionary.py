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
from src.dictionary import minSigEnerg, genericEnvelope

density  = 0.01
time     = np.arange(0,1000)
sigma    = 100
increase = 0.5 / (sigma**2)
decay    = 1.5 / sigma

class DictionaryTest(unittest.TestCase):
	def test_gaussEnvelope_1(self):
		'''
		Test standard gaussian envelope length
		'''
		envelope = genericEnvelope(sigma , time , 11 , 0)[0]
		self.assertEqual(envelope.shape , time.shape)
	def test_asymAEnvelope_1(self):
		'''
		Test asymetricA envelope length
		'''
		expectation = genericEnvelope(sigma , time , 11 , 1)[1]
		envelope    = genericEnvelope(sigma , time , 21 , 0 , expectation , increase , decay)[0]
		self.assertEqual(envelope.shape , time.shape)
	def test_gaussEnvelope_2(self):
		'''
		Test standard gaussian envelope miu
		'''
		miu = genericEnvelope(sigma , time , 11 , 1)[1]
		self.assertEqual(miu , 429.5)
	def test_asymAEnvelope_2(self):
		'''
		Test asymetricA envelope miu
		'''
		expectation = genericEnvelope(sigma , time , 11 , 1)[1]
		miu         = genericEnvelope(sigma , time , 21 , 0 , expectation , increase , decay)[1]
		self.assertEqual(miu , 429.5)
	def test_gaussEnvelope_3(self):
		'''
		Test standard gaussian envelope length after cutting
		'''
		envelope = genericEnvelope(sigma , time , 11 , 1)[0]
		self.assertEqual(envelope.shape[0] , 857L)
	def test_asymAEnvelope_3(self):
		'''
		Test asymetricA envelope length after cutting
		'''
		expectation = genericEnvelope(sigma , time , 11 , 1)[1]
		envelope    = genericEnvelope(sigma , time , 21 , 1 , expectation , increase , decay)[0]
		self.assertEqual(envelope.shape[0] , 998L)
	def test_rectEnvelope_1(self):
		'''
		Test rectangular envelope length
		'''
		envelope = genericEnvelope(sigma , time , 31 , 0)[0]
		self.assertEqual(envelope.shape , time.shape)
	def test_rectEnvelope_2(self):
		'''
		Test rectangular (typeA) envelope miu
		'''
		#### !!!! ####
		miu = genericEnvelope(sigma , time , 32 , 0)[1]
		self.assertEqual(miu , 499.5)
	def test_rectEnvelope_3(self):
		'''
		Test rectangular (typeB) envelope length after cutting
		'''
		envelope = genericEnvelope(sigma , time , 33 , 1)[0]
		self.assertEqual(envelope.shape[0] , 261L)
	def test_minSigEnerg_1(self):
		'''
		Test of common energy of two exact envelopes
		'''
		envelope = genericEnvelope(sigma , time , 11 , 0)[0]
		energy   = minSigEnerg(sigma , envelope , density , time , 11)
		energy   = float("{0:.2f}".format(energy))
		self.assertEqual(energy , density)
	def test_minSigEnerg_2(self):
		'''
		Test of common energy of two completely different envelopes
		'''
		envelope = np.zeros(time.shape)
		energy   = minSigEnerg(sigma , envelope , density , time , 11)
		energy   = float("{0:.2f}".format(energy))
		self.assertEqual(energy , 1-density)


	