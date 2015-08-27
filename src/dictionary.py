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
#from math import floor
import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt

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

def appendToDictionary(dictionary , density , envelope , mi , sigma , increase , decay , shapeType):
	dictionaryElement = {}
	dictionaryElement['timeCourse'] = envelope
	if shapeType != 21:
		dictionaryElement['step']   = np.array([minPosEnerg(envelope , density) , 1]).max()
	else:
		dictionaryElement['step']   = dictionary[-1]['step']
		# for asymA it should be the same as for a standard gauss with the same mi and sigma
		# it happens, that such a gaussian envelope is located directly before this one
	dictionaryElement['sigma']     = sigma
	dictionaryElement['mi']        = int(mi)
	dictionaryElement['increase']  = increase
	dictionaryElement['decay']     = decay
	dictionaryElement['shapeType'] = shapeType

	dictionary.append(pd.Series(dictionaryElement))

	return dictionary

def generateBasicStructures(time , config):
	dictionary = []

	sigmaStart = (config['minS'] + config['maxS'])/2
	gc         = genericEnvelope(sigmaStart , time , 11 , 0)[0]
	# gc is a standard gaussian envelope in that case
	sigmaStop  = fmin(func=minSigEnerg , x0=sigmaStart, args=(gc,config['density'],time,11) , disp=0)[0]

	sigmaActual = config['minS']
	sigmaParity = sigmaStop / sigmaStart
	if sigmaParity < 1:
		sigmaParity = 1 / sigmaParity

	threshold = config['maxS'] * np.sqrt(sigmaParity)

	while sigmaActual < threshold:
		(envelope , mi , increase , decay) = genericEnvelope(sigmaActual , time , 11 , 1)
		dictionary = appendToDictionary(dictionary , config['density'] , envelope , mi , sigmaActual , increase , decay , 11)

		if config['flags']['useAsymA']:
			(envelope , mi , increase , decay) = genericEnvelope(sigmaActual , time , 21 , 1 , mi)
			dictionary      = appendToDictionary(dictionary , config['density'] , envelope , mi , sigmaActual , increase , decay , 21)

		sigmaActual = sigmaActual * sigmaParity
	return dictionary

def generateRectangularEnvelopes(dictionary , time , config):
	shapeType = 32
	sigmaStart = (config['minS'] + config['maxS'])/2
	gc         = genericEnvelope(sigmaStart , time , shapeType , 0)[0]
	# gc is of rectA type in that case
	sigmaStop  = fmin(func=minSigEnerg , x0=sigmaStart, args=(gc,config['density'],time,shapeType) , disp=0)[0]

	sigmaActual = config['minS']
	sigmaParity = sigmaStop / sigmaStart
	if sigmaParity < 1:
		sigmaParity = 1 / sigmaParity

	threshold = config['maxS'] * np.sqrt(sigmaParity)

	while sigmaActual < threshold:
		(envelope , mi , increase , decay) = genericEnvelope(sigmaActual , time , shapeType , 1)
		dictionary = appendToDictionary(dictionary , config['density'] , envelope , mi , sigmaActual , increase , decay , shapeType)
		sigmaActual = sigmaActual * sigmaParity

	return dictionary


def genericEnvelope(sigma , time , shapeType , cutOutput , *argv):
	
	mainShapeType = int(shapeType / 10)
	subShapeType  = int(shapeType % 10)

	if mainShapeType == 1:
			alpha = -0.5
	elif mainShapeType == 2:
		alpha = 0
	elif mainShapeType == 3:
		alpha = -0.125

	if len(argv) == 0:
		mi = time[-1]/2
		increase = 0.5 / (sigma**2)
		decay    = 1.5 / sigma
	elif len(argv) == 1:
		mi = argv[0]
		increase = 0.5 / (sigma**2)
		decay    = 1.5 / sigma
	elif len(argv) == 2:
		mi    = argv[0]
		alpha = argv[1]
	elif len(argv) == 3:
		mi       = argv[0]
		increase = argv[1]
		decay    = argv[2]

	if mainShapeType == 1:
		(envelope , mi , increase , decay) = symetricEnvelope(sigma , mi , time , subShapeType , cutOutput)
	elif mainShapeType == 2:
		(envelope , mi , increase , decay) = asymetricEnvelope(increase , decay , mi , time , subShapeType , cutOutput)
	elif mainShapeType == 3:
		(envelope , mi , increase , decay) = symetricEnvelope(sigma , mi , time , subShapeType , cutOutput , alpha)
	return (envelope , mi , increase , decay)

def symetricEnvelope(sigma , mi , time , subShapeType , cutOutput , *argv):
	'''
	subShapeType:int
	1 - standard gaussian envelope
	2 - envelope of type rectA (flatten on top - power of 8)
	3 - envelope of type rectB (flatten on top - power of 16)
	4 - envelope of type rectC (flatten on top - power of 32)

	cutOutput:int
	0 - return raw envelope, ie. size of the signal
	1 - cut based on eps
	'''
	eps = 1e-4
	x   = (time - mi) / (sigma)

	if len(argv) == 0 and subShapeType == 1:
		alpha = -0.5
	elif len(argv) == 0 and subShapeType != 1:
		alpha = -0.125
	elif len(argv) == 1:
		alpha = argv[0]

	if subShapeType == 1:
		y = np.exp(alpha * x**2)
	elif subShapeType == 2:
		y = np.exp(alpha * x**8)
	elif subShapeType == 3:
		y = np.exp(alpha * x**16)
	elif subShapeType == 4:
		y = np.exp(alpha * x**32)

	if cutOutput == 1:
		ind        = np.where(y>eps)[0]
		whereFrom = ind[0]
		whereTo   = ind[-1]
		mi        = (whereFrom + whereTo)/2.0 - whereFrom + 1

	envelope  = y / np.linalg.norm(y)
	if cutOutput == 1:
		envelope  = envelope[whereFrom:whereTo]

	return (envelope , mi , 0 , 0)
	# increase and decay of a symetric shape should always be 0.

def asymetricEnvelope(increase , decay , mi , time , subShapeType , cutOutput):
	'''
	subShapeType:int
	1 - envelope of type asymA (power of 2 for increasing slope)
	2 - envelope of type asymB (power of 4 for increasing slope)
	3 - envelope of type asymC (power of 8 for increasing slope)
	4 - envelope of type asymD (power of 8 for increasing slope and 5 for decaying slope)
	asymB and asymC are not present in the base dictionary, but
	they are available due to a gradient optimisation procedure

	cutOutput:int
	0 - return raw envelope, ie. size of the signal
	1 - cut based on eps
	'''
	eps = 1e-4
	tmp = time - mi

	if subShapeType == 1:
		y = np.exp(-increase*(tmp**2) / (1 + decay * tmp * (np.arctan(1e16*tmp)+np.pi/2)/np.pi))
	elif subShapeType == 2:
		y = np.exp(-increase*(tmp**4) / (1 + decay * tmp * (np.arctan(1e16*tmp)+np.pi/2)/np.pi))
	elif subShapeType == 3:
		y = np.exp(-increase*(tmp**8) / (1 + decay * tmp * (np.arctan(1e16*tmp)+np.pi/2)/np.pi))
	elif subShapeType == 4:
		y = np.exp(-increase*(tmp**8) / (1 + decay * (tmp**5) * (np.arctan(1e16*tmp)+np.pi/2)/np.pi))

	if cutOutput == 1:
		ind        = np.where(y>eps)[0]
		whereFrom  = ind[0]
		whereTo    = ind[-1]
		mi         = mi + 1 - whereFrom
	
	envelope   = y / np.linalg.norm(y)
	if cutOutput == 1:
		envelope  = envelope[whereFrom:whereTo]

	return (envelope , mi , increase , decay)

def tukey(M, alpha=0.5, sym=True):
    '''
    We shoud just use scipy.signal.tukey from scipy 0.17+
    This is copied from there, sorry...
    '''
    if M < 1:
        return np.array([])
    if M == 1:
        return np.ones(1, 'd')

    if alpha <= 0:
        return np.ones(M, 'd')
    elif alpha >= 1.0:
        return hann(M, sym=sym)

    odd = M % 2
    if not sym and not odd:
        M = M + 1

    n = np.arange(0, M)
    width = int(np.floor(alpha*(M-1)/2.0))
    n1 = n[0:width+1]
    n2 = n[width+1:M-width-1]
    n3 = n[M-width-1:]

    w1 = 0.5 * (1 + np.cos(np.pi * (-1 + 2.0*n1/alpha/(M-1))))
    w2 = np.ones(n2.shape)
    w3 = 0.5 * (1 + np.cos(np.pi * (-2.0/alpha + 1 + 2.0*n3/alpha/(M-1))))

    w = np.concatenate((w1, w2, w3))

    if not sym and not odd:
        w = w[:-1]
    return w


def findWidth(envelope , samplingFrequency):
	return np.where(envelope > 0.5 * envelope.max())[0].shape[0] / samplingFrequency

def minSigEnerg(testSigma , testEnvelope , density , time , shapeType):
	gx = genericEnvelope(testSigma , time , shapeType , 0)[0]
	return np.abs(1 - density - np.dot(gx , testEnvelope))

def minPosEnerg(testEnvelope , density):
	xcorr  = np.abs(1 - density - np.correlate(testEnvelope , testEnvelope , 'full'))
	where  = xcorr.argmin()
	return np.abs(testEnvelope.size - where -1)

def bestEnvelope(x,time,signal,shapeType):
	mainShapeType = int(shapeType / 10)
	subShapeType  = int(shapeType % 10)

	if mainShapeType == 1:
		envelope = genericEnvelope(x[0] , time , shapeType , 0 , x[1])[0]
	elif mainShapeType == 2:
		envelope = genericEnvelope(0 , time , shapeType , 0 , x[0] , x[1] , x[2])[0]
		# sigma is not used in this case, so 0 is passed to the function
	elif mainShapeType == 3:
		envelope = genericEnvelope(x[0] , time , shapeType , 0 , x[1] , x[2])[0]
	return -1 * np.abs(np.dot(signal , envelope))
	
def bestFreq(freq , signal , time):
	return -1 * np.abs(np.dot(signal , np.exp(-1j*freq*time)))

#def bestFreqWithPhase(freq , signal , time):
#	AmplitudeSin = np.abs(np.dot(signal , np.sin(freq * time)))
#	AmplitudeCos = np.abs(np.dot(signal , np.cos(freq * time)))



