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
from src.dictionary import gaussEnvelope, asymetricEnvelope, minSigEnerg

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
		envelope = gaussEnvelope(sigma , time , 1 , 0)[0]
		self.assertEqual(envelope.shape , time.shape)
	def test_asymAEnvelope_1(self):
		'''
		Test asymetricA envelope length
		'''
		expectation = gaussEnvelope(sigma , time , 1 , 1)[1]
		envelope    = asymetricEnvelope(increase , decay , expectation , time , 1 , 0)[0]
		self.assertEqual(envelope.shape , time.shape)
	def test_gaussEnvelope_2(self):
		'''
		Test standard gaussian envelope miu
		'''
		miu = gaussEnvelope(sigma , time , 1 , 0)[1]
		self.assertEqual(miu , 429.5)
	def test_asymAEnvelope_2(self):
		'''
		Test asymetricA envelope miu
		'''
		expectation = gaussEnvelope(sigma , time , 1 , 1)[1]
		miu         = asymetricEnvelope(increase , decay , expectation , time , 1 , 0)[1]
		self.assertEqual(miu , 429.5)
	def test_gaussEnvelope_3(self):
		'''
		Test standard gaussian envelope length after cutting
		'''
		envelope = gaussEnvelope(sigma , time , 1 , 1)[0]
		self.assertEqual(envelope.shape[0] , 857L)
	def test_asymAEnvelope_3(self):
		'''
		Test asymetricA envelope length after cutting
		'''
		expectation = gaussEnvelope(sigma , time , 1 , 1)[1]
		envelope    = asymetricEnvelope(increase , decay , expectation , time , 1 , 1)[0]
		self.assertEqual(envelope.shape[0] , 998L)
	def test_rectEnvelope_1(self):
		'''
		Test rectangular envelope length
		'''
		envelope = gaussEnvelope(sigma , time , 2 , 0)[0]
		self.assertEqual(envelope.shape , time.shape)
	def test_rectEnvelope_2(self):
		'''
		Test rectangular envelope miu
		'''
		miu = gaussEnvelope(sigma , time , 2 , 0)[1]
		self.assertEqual(miu , 134.5)
	def test_rectEnvelope_3(self):
		'''
		Test rectangular envelope length after cutting
		'''
		envelope = gaussEnvelope(sigma , time , 2 , 1)[0]
		self.assertEqual(envelope.shape[0] , 267L)
	def test_minSigEnerg_1(self):
		'''
		Test of common energy of two exact envelopes
		'''
		envelope = gaussEnvelope(sigma , time , 1 , 0)[0]
		energy   = minSigEnerg(sigma , envelope , density , time , 1)
		energy   = float("{0:.2f}".format(energy))
		self.assertEqual(energy , density)
	def test_minSigEnerg_2(self):
		'''
		Test of common energy of two completely different envelopes
		'''
		envelope = np.zeros(time.shape)
		energy   = minSigEnerg(sigma , envelope , density , time , 1)
		energy   = float("{0:.2f}".format(energy))
		self.assertEqual(energy , 1-density)


	