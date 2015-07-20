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
import numpy  as np
import pandas as pd

def generateDictionary(time , config):
	'''
	config:dictionary - parameters
	minS    - minimal sigma
	maxS    - maximal sigma
	density - dictionary density
	flags   - which structures to use
	
	time:list - original time vector
	'''

	time       = np.arange(0,3*len(time))

	dictionary = generateBasicStructures(time , config)
	if config['flags']['useRectA'] == 1:
		dictionary = generateRectangularEnvelopes(dictionary , time , config)

	dictionary = pd.DataFrame(dictionary)
	return dictionary

def appendToDictionary(dictionary , density , envelope , srodek , sigma , shapeType):
	dictionaryElement = {}
	dictionaryElement['timeCourse'] = envelope
	dictionaryElement['step']       = np.array([minPosEnerg(envelope , density) , 1]).max()
	dictionaryElement['sigma']      = sigma
	# decay parameter as well
	dictionaryElement['srodek']     = int(srodek)
	dictionaryElement['shapeType']  = shapeType

	dictionary.append(pd.Series(dictionaryElement))
	return dictionary

def generateRectangularEnvelopes(dictionary , time , config):
	shapeType  = 2
	minS       = config['minS']
	maxS       = config['maxS']
	density    = config['density']
	flags      = config['flags']

	sigmaStart = (minS + maxS)/2
	gc          = gaussEnvelope(sigmaStart , time , 2 , 0)[0]
	sigmaStop  = fmin(func=minSigEnerg , x0=sigmaStart, args=(gc,density,time,2))[0]

	sigmaActual = minS
	sigmaParity = sigmaStop / sigmaStart
	if sigmaParity < 1:
		sigmaParity = 1 / sigmaParity

	threshold = maxS * np.sqrt(sigmaParity)

	while sigmaActual < threshold:
		(envelope , srodek) = gaussEnvelope(sigmaActual , time , shapeType)
		dictionary = appendToDictionary(dictionary , density , envelope , srodek , sigmaActual , shapeType)
		sigmaActual = sigmaActual * sigmaParity

	return dictionary

def generateBasicStructures(time , config):
	dictionary = []
	minS       = config['minS']
	maxS       = config['maxS']
	density    = config['density']
	flags      = config['flags']

	sigmaStart = (minS + maxS)/2
	gc         = gaussEnvelope(sigmaStart , time , 1 , 0)[0]
	sigmaStop  = fmin(func=minSigEnerg , x0=sigmaStart, args=(gc,density,time,1))[0]

	sigmaActual = minS
	sigmaParity = sigmaStop / sigmaStart
	if sigmaParity < 1:
		sigmaParity = 1 / sigmaParity

	threshold = maxS * np.sqrt(sigmaParity)

	while sigmaActual < threshold:
		shapeType = 1
		(envelope , srodek) = gaussEnvelope(sigmaActual , time , shapeType)
		dictionary = appendToDictionary(dictionary , density , envelope , srodek , sigmaActual , shapeType)

		if flags['useAsymA']:
			shapeType   = 3
			increase    = 0.5 / (sigmaActual**2)
			decay       = 1.5 / sigmaActual
			expectation = srodek
			(envelope , srodek) = asymetricEnvelope(increase , decay , expectation , time)
			dictionary = appendToDictionary(dictionary , density , envelope , srodek , sigmaActual , shapeType)

		sigmaActual = sigmaActual * sigmaParity
	return dictionary

def gaussEnvelope(sigma , time , shapeType=1 , cutOutput=1):
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
	ind        = np.where(y>eps)[0]

	whereFrom  = ind[0]
	whereTo    = ind[-1]
	expected   = (whereFrom + whereTo)/2.0 - whereFrom + 1
	envelope   = y / np.linalg.norm(y)

	if cutOutput == 1:
		envelope = envelope[whereFrom:whereTo]

	return (envelope , expected)

def asymetricEnvelope(increase , decay , expectation , time , shapeType=1 , cutOutput=1):
	'''
	shapeType:int
	1 - envelope of type asymA

	cutOutput:int
	0 - return raw envelope, ie. size of the signal
	1 - cut based on eps
	'''
	eps = 1e-4
	if shapeType == 1:
		tmp = time - expectation
		y = np.exp(-increase*(tmp**2) / (1 + decay * tmp * (np.arctan(1e16*tmp)+np.pi/2)/np.pi))
	ind        = np.where(y>eps)[0]
	whereFrom  = ind[0]
	whereTo    = ind[-1]
	expected   = expectation + 1 - whereFrom
	envelope   = y / np.linalg.norm(y)

	if cutOutput == 1:
		envelope = envelope[whereFrom:whereTo]
	return (envelope , expected)

def minSigEnerg(testSigma , testEnvelope , density , time , shapeType):
	gx = gaussEnvelope(testSigma , time , shapeType , 0)[0]
	return np.abs(1 - density - np.dot(gx , testEnvelope))

def minPosEnerg(testEnvelope , density):
	xcorr  = np.abs(1 - density - np.correlate(testEnvelope , testEnvelope , 'full'))
	where  = xcorr.argmin()
	return np.abs(testEnvelope.size - where -1)

def minEnvGauss(sigma,time,signal,shapeType):
	envelope = gaussEnvelope(sigma,time,shapeType,0)[0]
	return -1*np.abs(sum(signal * envelope))

def bestFreq(freq , signal , time):
	return -1*np.abs(sum(signal * np.exp(-1j*freq*time)))
