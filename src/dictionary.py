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
from __future__ import division
from scipy.optimize import fmin
import numpy as np

def generateDictionary(time , config):
	'''
	config:dictionary - parameters
	minS    - minimal sigma
	maxS    - maximal sigma
	density - dictionary density
	flags   - which structures to use
	
	time:list - original time vector
	'''

	time       = np.arange(1,3*len(time))

	dictionary = generateBasicStructures(time , config)

	return dictionary


def generateBasicStructures(time , config):
	dictionary = []
	minS       = config['minS']
	maxS       = config['maxS']
	density    = config['density']
	flags      = config['flags']

	sigmaStart = (minS + maxS)/2
	gc          = gaussEnvelope(sigmaStart , time)[0]
	sigmaStop  = fmin(func=minSigEnerg , x0=sigmaStart, args=(gc,density,time))[0]

	# print 'Start={}, stop={}'.format(sigmaStart,sigmaStop)

	sigmaActual = minS
	sigmaParity = sigmaStop / sigmaStart
	if sigmaParity < 1:
		sigmaParity = 1 / sigmaParity

	threshold = maxS * np.sqrt(sigmaParity)

	while sigmaActual < threshold:
		dictionaryElement = {}
		(envelope , poczatek , koniec , srodek) = gaussEnvelope(sigmaActual , time , 1)

		dictionaryElement['timeCourse'] = envelope[poczatek:koniec]
		dictionaryElement['energy']     = minPosEnerg(dictionaryElement['timeCourse'] , density)
		# book(iter).skok=max([1 book(iter).skok]);
		dictionaryElement['sigma']      = sigmaActual
		dictionaryElement['srodek']     = int(srodek)
		dictionaryElement['shapeType']  = 1
		dictionaryElement['decay']      = 0
		dictionary.append(dictionaryElement)

		if flags['useAsymA']:
			dictionaryElement = {}
			increase    = 0.5 / (sigmaActual**2)
			decay       = 1.5 / sigmaActual
			expectation = srodek
			(envelope , poczatek , koniec , srodek) = asymetricEnvelope(increase , decay , expectation , time , 1)

			dictionaryElement['timeCourse'] = envelope[poczatek:koniec]
			dictionaryElement['energy']     = dictionary[-1]['energy']
			dictionaryElement['sigma']      = sigmaActual
			dictionaryElement['srodek']     = int(srodek)
			dictionaryElement['shapeType']  = 2
			dictionaryElement['decay']      = decay
			dictionary.append(dictionaryElement)

		sigmaActual = sigmaActual * sigmaParity
	return dictionary


def gaussEnvelope(sigma , time , shapeType=1):
	'''
	shapeType:int
	1 - standard gaussian shape
	2 - flatten on top
	'''
	eps = 1e-4
	mi  = time[-1]/2
	x   = (mi - time) / sigma

	if shapeType == 1:
		y = np.exp(-1 * x**2 /2)
	elif shapeType == 2:
		y = np.exp(-7 * x**8 /8)
	
	ind      = np.where(y>eps)[0]
	poczatek = ind[0]
	koniec   = ind[-1]
	srodek   = (poczatek + koniec)/2 - poczatek + 1
	envelope = y / np.linalg.norm(y)
	
	return (envelope , poczatek , koniec , srodek)

def asymetricEnvelope(increase , decay , expectation , time , shapeType=1):
	'''
	shapeType:int
	1 - envelope of type asymA
	'''
	eps = 1e-4
	if shapeType == 1:
		tmp = time - expectation
		y = np.exp(-increase*(tmp**2) / (1 + decay * tmp * (np.arctan(1e16*tmp)+np.pi/2)/np.pi))
	ind      = np.where(y>eps)[0]
	poczatek = ind[0]
	koniec   = ind[-1]
	srodek   = expectation + 1 - poczatek
	envelope = y / np.linalg.norm(y)
	return (envelope , poczatek , koniec , srodek)

def minSigEnerg(testSigma , testEnvelope , density , time):
	(gx , p , k , sr) = gaussEnvelope(testSigma , time)
	return np.abs(1 - density - np.dot(gx , testEnvelope))

def minPosEnerg(testEnvelope , density):
	xcorr  = np.abs(1 - density - np.correlate(testEnvelope , testEnvelope , 'full'))
	where  = xcorr.argmin()
	return np.abs(testEnvelope.size - where)
