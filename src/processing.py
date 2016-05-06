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

import numpy as np
import pandas as pd

from scipy.signal      import hilbert
from numpy.linalg      import norm
from scipy.optimize    import fmin, minimize
# from collections       import deque

import dictionary as dic

import matplotlib.pyplot as plt


def calculateMP(dictionary , signal , config):
	'''
	dictionary - pandas.DataFrame containing redundant base set of functions
	signal     - numpy.array containing signal to decompose
	config     - dict
	- 
	'''

	book           = []
	if signal.sum() == 0:
		zerosFlag = 1
	else:
		zerosFlag = 0
	
	if config['algorithm'] == 'smp':
		partialResults = []
		signal         = hilbert(signal)
		signalRest     = signal
		signalEnergy   = calculateSignalEnergy(signal)
		signalLength   = signal.shape[0]

		for iteration in np.arange(0 , config['maxNumberOfIterations']):
			(bookElement , partialResults , signalRest) = makeOneIteration(dictionary , partialResults , signalRest , signalLength , config , iteration)
			
			book.append(pd.Series(bookElement))

			if zerosFlag == 1:
				if config['flags']['displayInfo'] != 0:
					print 'Signal contained only zeros!'
				return pd.DataFrame(book)

			energyExplained    = np.abs(1 - calculateSignalEnergy(signalRest) / signalEnergy)
			minEnergyExplained = config['minEnergyExplained'] - config['density'] * (calculateSignalEnergy(bookElement['reconstruction']) / calculateSignalEnergy(signalRest))
			
			msg = 'Iteration {} done, energy explained: {}.'.format(iteration , energyExplained)

			if config['flags']['displayInfo'] != 0:
				print msg
			
			if energyExplained > minEnergyExplained:
				return pd.DataFrame(book)
	

	elif config['algorithm'] == 'mmp':
		partialResultsFinal = []

		tmpSignals = np.zeros(signal.shape , dtype='complex')
		for trialNumber in np.arange(0 , len(config['trials2calculate'])):
			for channelNumber in np.arange(0 , len(config['channels2calculate'])):
				tmpSignals[trialNumber , channelNumber , :] = hilbert(np.squeeze(signal[trialNumber , channelNumber , :]))
		signal       = tmpSignals
		signalRest   = signal
		signalLength = signal.shape[2]

		# print 'signalLength = {}'.format(signalLength)
		
		for iteration in np.arange(0 , config['maxNumberOfIterations']):
			partialResultsAll = []
			atomFitnessAll    = []
			for trialNumber in np.arange(0 , len(config['trials2calculate'])):
				partialResultsTmp = []
				atomFitnessTmp    = []
				for channelNumber in np.arange(0 , len(config['channels2calculate'])):
					(partialResults , atomFitness , numberOfAtoms) = calcFitnessForAllAtoms(dictionary , [] , signalRest[trialNumber , channelNumber , :] , signalLength , config , iteration)
					partialResultsTmp.append(partialResults)
					atomFitnessTmp.append(atomFitness)
				partialResultsAll.append(partialResultsTmp)
				atomFitnessAll.append(atomFitnessTmp)

			a = np.zeros(numberOfAtoms , dtype='complex')
			e = np.zeros(numberOfAtoms , dtype='complex')
			for atomNumber in np.arange(0 , numberOfAtoms):
				A = np.zeros([len(config['trials2calculate']),len(config['channels2calculate'])] , dtype='complex')
				
				for trialNumber in np.arange(0 , len(config['trials2calculate'])):
					for channelNumber in np.arange(0 , len(config['channels2calculate'])):
						A[trialNumber,channelNumber] = atomFitnessAll[trialNumber][channelNumber][atomNumber][0]['amplitude']
				
				for trialNumber in np.arange(0 , len(config['trials2calculate'])):
					a[atomNumber] += norm( A[trialNumber,:]/norm(A,None,1)[trialNumber] , None)
					e[atomNumber] += norm( A[trialNumber,:] , None)
			
			# for trialNumber in np.arange(0 , len(config['trials2calculate'])):
			# 	a += norm( amplitudes[trialNumber,:]/norm(amplitudes,None,1)[trialNumber] , None )
			# 	# e += 

			print a
			print '---'
			





	return pd.DataFrame(book)

def calcFitnessForAllAtoms(dictionary , partialResults , signalRest , signalLength , config , iteration):
	(partialResults , subMaxDOT , subMaxFreq) = recalculateDotProducts(dictionary , partialResults , signalRest , config['minNFFT'] , signalLength , iteration)

	atomFitness = []

	for (index, partialResult) in partialResults.iterrows():
		time = np.arange(0, partialResult['time'].shape[0] )

		bookElement = {}
		bookElement['time']           = partialResult['time']
		bookElement['freq']           = subMaxFreq[index]
		bookElement['amplitude']      = subMaxDOT[index]
		bookElement['sigma']          = partialResult['sigma']
		bookElement['shapeType']      = partialResult['shapeType']

		bookElement['envelope']       = np.zeros((signalLength))
	
		if isinstance(bookElement['time'], (np.ndarray, np.generic)):
			envelopeBeginIndex = bookElement['time'][0]
			envelopeEndIndex   = bookElement['time'][-1]+1
		else:
			# in case of older pandas library:
			envelopeBeginIndex = bookElement['time'].values[0]
			envelopeEndIndex   = bookElement['time'].values[-1]+1
	
		bookElement['envelope'][envelopeBeginIndex:envelopeEndIndex] = partialResult['timeCourse']
		bookElement['reconstruction'] = np.zeros(signalLength,dtype='complex')
		bookElement['reconstruction'][envelopeBeginIndex:envelopeEndIndex] = bookElement['amplitude']*partialResult['timeCourse']*np.exp(1j*bookElement['freq']*time)

		atomSignalRest = signalRest - bookElement['reconstruction']
		atomFitness.append((bookElement , atomSignalRest))

	return (partialResults , atomFitness , index)
	
def makeOneIteration(dictionary , partialResults , signalRest , signalLength , config , iteration):
	(partialResults , subMaxDOT , subMaxFreq) = recalculateDotProducts(dictionary , partialResults , signalRest , config['minNFFT'] , signalLength , iteration)

	whereMax  = np.abs(subMaxDOT).argmax()

	time = np.arange(0,partialResults['time'][whereMax].shape[0])
		
	bookElement = {}
	bookElement['time']           = partialResults['time'][whereMax]
	bookElement['freq']           = subMaxFreq[whereMax]
	bookElement['amplitude']      = subMaxDOT[whereMax]
	bookElement['sigma']          = partialResults['sigma'][whereMax]
	bookElement['shapeType']      = partialResults['shapeType'][whereMax]
		
	bookElement['envelope']       = np.zeros((signalLength))
	
	if isinstance(bookElement['time'], (np.ndarray, np.generic)):
		envelopeBeginIndex = bookElement['time'][0]
		envelopeEndIndex   = bookElement['time'][-1]+1
	else:
		# in case of older pandas library:
		envelopeBeginIndex = bookElement['time'].values[0]
		envelopeEndIndex   = bookElement['time'].values[-1]+1
	
	bookElement['envelope'][envelopeBeginIndex:envelopeEndIndex] = partialResults['timeCourse'][whereMax]
	bookElement['reconstruction'] = np.zeros(signalLength,dtype='complex')
	bookElement['reconstruction'][envelopeBeginIndex:envelopeEndIndex] = bookElement['amplitude']*partialResults['timeCourse'][whereMax]*np.exp(1j*bookElement['freq']*time)

	if config['flags']['useGradientOptimization'] == 1:
		where_mi   = partialResults['timeCourse'][whereMax].argmax()
		mi_0       = partialResults['time'][whereMax][where_mi]
		sigma_0    = partialResults['sigma'][whereMax]
		increase_0 = partialResults['increase'][whereMax]
		decay_0    = partialResults['decay'][whereMax]
		whereStart = partialResults['time'][whereMax][0]

		(freq,amplitude,sigma,increase,decay,mi,envelope,reconstruction,shapeTypeNew) = gradientSearch([whereStart,subMaxDOT[whereMax],mi_0,sigma_0,subMaxFreq[whereMax],increase_0,decay_0],[config['minS'],config['maxS']],signalRest,partialResults['shapeType'][whereMax],config['flags']['useAsymA'])

		if np.abs(amplitude) > np.abs(bookElement['amplitude']):
			bookElement['amplitude']      = amplitude
			bookElement['freq']           = freq
			bookElement['sigma']          = sigma
			bookElement['envelope']       = envelope
			bookElement['reconstruction'] = reconstruction
			bookElement['shapeType']      = shapeTypeNew

	signalRest = signalRest - bookElement['reconstruction']

	bookElement['freq']      = (config['samplingFrequency'] * bookElement['freq']) / (2 * np.pi)
	bookElement['width']     = dic.findWidth(bookElement['envelope'] , config['samplingFrequency'])
	bookElement['modulus']   = bookElement['amplitude']
	bookElement['amplitude'] = np.abs(np.max(bookElement['reconstruction']))

	# print 'Width = {}, sigma = {}, sampling = {}.'.format(bookElement['width'] , bookElement['sigma'] , config['samplingFrequency'])

	return (bookElement , partialResults , signalRest)


def gradientSearch(startParams , boundParams , signal , shapeType , forceAsymetry=1):
	epsilon        = 1e-3
	whereStart     = startParams[0]
	amplitudeStart = startParams[1]
	miStart        = startParams[2]
	sigmaStart     = startParams[3]
	freqStart      = startParams[4]
	increaseStart  = startParams[5]
	decayStart     = startParams[6]
	alphaStart     = 1.0
	
	minS           = 0.50 * boundParams[0]
	maxS           = 1.50 * boundParams[1]
	maxI           = 0.5/minS**2
	minI           = 0.5/maxS**2
	maxD           = 1.5 / minS
	minD           = 1.5 / maxS
	time           = np.arange(0 , signal.shape[0])
	timeShifted    = time - whereStart
	cutOutput      = 0

	mainShapeType = int(shapeType / 10)
	subShapeType  = int(shapeType % 10)

	if mainShapeType == 1 and subShapeType == 1:
		# case of standard gauss envelopes
		tmpShapeType = 11
		output       = minimize(fun=dic.bestEnvelope , x0=np.array([sigmaStart,miStart]) , args=(time,signal*np.exp(-1j*freqStart*timeShifted),tmpShapeType) , method='L-BFGS-B', bounds=[(minS,maxS),(0,signal.shape[0])] , tol=epsilon , options={'disp':0})
		sigmaSym     = output['x'][0]
		miSym        = output['x'][1]
		increaseSym  = 0
		decaySym     = 0
		envelopeSym  = dic.genericEnvelope(sigmaSym,time,tmpShapeType,cutOutput,miSym)[0]
		amplitudeSym = np.dot(signal , envelopeSym*np.exp(-1j*freqStart*timeShifted))

		if forceAsymetry > 0:
			tmpShapeType  = 21
			increaseStart = 0.5 / sigmaStart**2
			decayStart    = 1.5 / sigmaStart
			output        = minimize(fun=dic.bestEnvelope , x0=np.array([miStart,increaseStart,decayStart]) , args=(time,signal*np.exp(-1j*freqStart*timeShifted),tmpShapeType) , method='L-BFGS-B', bounds=[(0,signal.shape[0]),(minI,maxI),(minD,maxD)] , tol=epsilon , options={'disp':0})
			miAsym        = output['x'][0]
			increaseAsym  = output['x'][1]
			decayAsym     = output['x'][2]
			sigmaAsym     = (2*decayAsym) / 3.
			envelopeAsym  = dic.genericEnvelope(sigmaAsym,time,tmpShapeType,cutOutput,miAsym,increaseAsym,decayAsym)[0]
			amplitudeAsym = np.dot(signal , envelopeAsym*np.exp(-1j*freqStart*timeShifted))
		else:
			amplitudeAsym = 0

		# print 'Amplitude for sym={}, asym={}'.format(np.abs(amplitudeSym) , np.abs(amplitudeAsym))
		if (np.abs(amplitudeAsym) > np.abs(amplitudeSym)):
			amplitude      = amplitudeAsym
			envelope       = envelopeAsym
			mi             = miAsym
			increase       = increaseAsym
			decay          = decayAsym
			sigma          = sigmaAsym
			finalShapeType = 21 			# AsymA, in fact
		else:
			amplitude      = amplitudeSym
			envelope       = envelopeSym
			mi             = miSym
			increase       = increaseSym
			decay          = decaySym
			sigma          = sigmaSym
			finalShapeType = 11 			# Standard Gauss, in fact
# FROM HERE
		output = minimize(fun=dic.bestFreq , x0=freqStart , args=(signal*envelope,timeShifted) , method='L-BFGS-B' , tol=epsilon , options={'disp':0})
		newFreq      = output['x'][0]
		amplitudeTmp = np.dot(signal , envelope*np.exp(-1j*newFreq*timeShifted))

		if np.abs(amplitude) < np.abs(amplitudeTmp):
			amplitude      = amplitudeTmp
			freq           = newFreq
			reconstruction = amplitude * envelope * np.exp(1j*freq*timeShifted)
		else:
			reconstruction = amplitude * envelope * np.exp(1j*freqStart*timeShifted)
			return (freqStart,amplitude,sigma,increase,decay,mi,envelope,reconstruction,finalShapeType)

		amplitudeActual = np.abs(amplitudeStart)

		while (np.abs(amplitude) - amplitudeActual)/amplitudeActual > epsilon:
		 	amplitudeActual = np.abs(amplitude)

		 	if finalShapeType == 11:
		 		output   = minimize(fun=dic.bestEnvelope , x0=np.array([sigma,mi]) , args=(time,signal*np.exp(-1j*freq*timeShifted),finalShapeType) , method='L-BFGS-B', bounds=[(minS,maxS),(0,signal.shape[0])] , tol=epsilon , options={'disp':0})
		 		sigma    = output['x'][0]
		 		mi       = output['x'][1]
		 		increase = 0
		 		decay    = 0
		 		envelope = dic.genericEnvelope(sigma,time,finalShapeType,cutOutput,mi)[0]
		 	else:
				output   = minimize(fun=dic.bestEnvelope , x0=np.array([mi,increase,decay]) , args=(time,signal*np.exp(-1j*freq*timeShifted),finalShapeType) , method='L-BFGS-B', bounds=[(0,signal.shape[0]),(minI,maxI),(minD,maxD)] , tol=epsilon , options={'disp':0})
				mi       = output['x'][0]
				increase = output['x'][1]
				decay    = output['x'][2]
				sigma    = np.sqrt(1./2./increase)
				envelope = dic.genericEnvelope(sigma,time,finalShapeType,cutOutput,mi,increase,decay)[0]

			amplitude    = np.dot(signal , envelope*np.exp(-1j*freq*timeShifted))
		 	output       = minimize(fun=dic.bestFreq , x0=freq , args=(signal*envelope,timeShifted) , method='L-BFGS-B' , tol=epsilon , options={'disp':0})
			newFreq      = output['x'][0]
		 	amplitudeTmp = np.dot(signal , envelope*np.exp(-1j*newFreq*timeShifted))

		 	if np.abs(amplitude) < np.abs(amplitudeTmp):
		 		freq           = newFreq
		 		amplitude      = amplitudeTmp
		 		reconstruction = amplitude * envelope * np.exp(1j*freq*timeShifted)
		 	else:
		 		reconstruction  = amplitude * envelope * np.exp(1j*freq*timeShifted)
		 		return (freq,amplitude,sigma,increase,decay,mi,envelope,reconstruction,finalShapeType)
# TO HERE

	elif mainShapeType == 2:
		# case of asymA envelopes (basic type of asymetry)

		subTypeTest = []
		envelopes   = []
		outputs     = []
		subTypes2test  = [1,2,4]

		for tt in subTypes2test:
			shapeType2test = 10 * mainShapeType + tt
			output = minimize(fun=dic.bestEnvelope , x0=np.array([miStart,increaseStart,decayStart]) , args=(time,signal*np.exp(-1j*freqStart*timeShifted),shapeType2test) , method='L-BFGS-B', bounds=[(0,signal.shape[0]),(minI,maxI),(minD,maxD)] , tol=epsilon , options={'disp':0})
			outputs.append(output['x'])
			envelopes.append(dic.genericEnvelope(np.sqrt(1./2./output['x'][1]),time,shapeType2test,cutOutput,output['x'][0],output['x'][1],output['x'][2])[0])
			amplitude = np.dot(signal , envelopes[-1] * np.exp(-1j*freqStart*timeShifted))
			subTypeTest.append(amplitude)
		subTypeTest = np.array(subTypeTest , dtype='complex')
		ind         = subTypeTest.argmax()

		envelope  = envelopes[ind]
		amplitude = subTypeTest[ind]
		output    = outputs[ind]
		mi        = output[0]
		increase  = output[1]
		decay     = output[2]
		sigma     = np.sqrt(1./2./increase)

		finalShapeType = 10 * mainShapeType + subTypes2test[ind]
		
## -- FROM HERE -- ##
		output = minimize(fun=dic.bestFreq , x0=freqStart , args=(signal*envelope,timeShifted) , method='L-BFGS-B' , tol=epsilon , options={'disp':0})
		newFreq      = output['x'][0]
		amplitudeTmp = np.dot(signal , envelope*np.exp(-1j*newFreq*timeShifted))

		if np.abs(amplitude) < np.abs(amplitudeTmp):
			amplitude      = amplitudeTmp
			freq           = newFreq
			reconstruction = amplitude * envelope * np.exp(1j*freq*timeShifted)
		else:
			reconstruction = amplitude * envelope * np.exp(1j*freqStart*timeShifted)
			return (freqStart,amplitude,sigma,increase,decay,mi,envelope,reconstruction,finalShapeType)

		amplitudeActual = np.abs(amplitudeStart)

		while (np.abs(amplitude) - amplitudeActual)/amplitudeActual > epsilon:
		 	amplitudeActual = np.abs(amplitude)

			output   = minimize(fun=dic.bestEnvelope , x0=np.array([mi,increase,decay]) , args=(time,signal*np.exp(-1j*freq*timeShifted),finalShapeType) , method='L-BFGS-B', bounds=[(0,signal.shape[0]),(minI,maxI),(minD,maxD)] , tol=epsilon , options={'disp':0})
			mi       = output['x'][0]
			increase = output['x'][1]
			decay    = output['x'][2]
			sigma    = np.sqrt(1./2./increase)
			envelope = dic.genericEnvelope(sigma,time,finalShapeType,cutOutput,mi,increase,decay)[0]

			amplitude    = np.dot(signal , envelope*np.exp(-1j*freq*timeShifted))
		 	output       = minimize(fun=dic.bestFreq , x0=freq , args=(signal*envelope,timeShifted) , method='L-BFGS-B' , tol=epsilon , options={'disp':0})
			newFreq      = output['x'][0]
		 	amplitudeTmp = np.dot(signal , envelope*np.exp(-1j*newFreq*timeShifted))

		 	if np.abs(amplitude) < np.abs(amplitudeTmp):
		 		freq           = newFreq
		 		amplitude      = amplitudeTmp
		 		reconstruction = amplitude * envelope * np.exp(1j*freq*timeShifted)
		 	else:
		 		reconstruction  = amplitude * envelope * np.exp(1j*freq*timeShifted)
		 		return (freq,amplitude,sigma,increase,decay,mi,envelope,reconstruction,finalShapeType)
## -- TO HERE -- ##

	elif mainShapeType == 3:
		# case of rectA envelopes (special symetric shapes)
		typeTest    = []
		envelopes   = []
		outputs     = []
		types2test  = [21,22,24,32,33] # possibly 34 as well.

		for shapeType2test in types2test:
			main = int(shapeType2test / 10)
			sub  = int(shapeType2test % 10)
			if main == 2:
				output = minimize(fun=dic.bestEnvelope , x0=np.array([miStart,increaseStart,decayStart]) , args=(time,signal*np.exp(-1j*freqStart*timeShifted),shapeType2test) , method='L-BFGS-B', bounds=[(0,signal.shape[0]),(minI,maxI),(minD,maxD)] , tol=epsilon , options={'disp':0})
				output['x'] = [output['x'][0] , output['x'][1] , output['x'][2] , np.sqrt(1./2./output['x'][1]) , 0.0] # mi,increase,decay,sigma,alpha
				envelopes.append(dic.genericEnvelope(0,time,shapeType2test,cutOutput,output['x'][0],output['x'][1],output['x'][2])[0])
			elif main == 3:
				output = minimize(fun=dic.bestEnvelope , x0=np.array([sigmaStart,miStart,alphaStart]) , args=(time,signal*np.exp(-1j*freqStart*timeShifted),shapeType2test) , method='L-BFGS-B', bounds=[(minS,maxS),(0,signal.shape[0]),(None,None)] , tol=epsilon , options={'disp':0})
				output['x'] = [output['x'][1] , 0.0 , 0.0 , output['x'][0] , output['x'][2]]	# mi,increase,decay,sigma,alpha
				envelopes.append(dic.genericEnvelope(output['x'][3],time,shapeType2test,cutOutput,output['x'][0],output['x'][4])[0])
			outputs.append(output['x'])
			amplitude = np.dot(signal , envelopes[-1] * np.exp(-1j*freqStart*timeShifted))
			typeTest.append(amplitude)
		typeTest = np.array(typeTest , dtype='complex')
		ind         = typeTest.argmax()
		
		envelope  = envelopes[ind]
		amplitude = typeTest[ind]
		output    = outputs[ind]
		mi        = output[0]
		increase  = output[1]
		decay     = output[2]
		sigma     = output[3]
		alpha     = output[4]

		finalShapeType = types2test[ind]
		mainShapeType  = int(finalShapeType / 10)

## -- FROM HERE -- ##
		output = minimize(fun=dic.bestFreq , x0=freqStart , args=(signal*envelope,timeShifted) , method='L-BFGS-B' , tol=epsilon , options={'disp':0})
		newFreq      = output['x'][0]
		amplitudeTmp = np.dot(signal , envelope*np.exp(-1j*newFreq*timeShifted))

		if np.abs(amplitude) < np.abs(amplitudeTmp):
			amplitude      = amplitudeTmp
			freq           = newFreq
			# reconstruction = amplitude * envelope * np.exp(1j*freq*timeShifted)
		else:
			reconstruction = amplitude * envelope * np.exp(1j*freqStart*timeShifted)
			return (freqStart,amplitude,sigma,increase,decay,mi,envelope,reconstruction,finalShapeType)

		amplitudeActual = np.abs(amplitudeStart)

		while (np.abs(amplitude) - amplitudeActual)/amplitudeActual > epsilon:
		 	amplitudeActual = np.abs(amplitude)

		 	if mainShapeType == 2:
		 		output   = minimize(fun=dic.bestEnvelope , x0=np.array([mi,increase,decay]) , args=(time,signal*np.exp(-1j*freq*timeShifted),shapeType2test) , method='L-BFGS-B', bounds=[(0,signal.shape[0]),(minI,maxI),(minD,maxD)] , tol=epsilon , options={'disp':0})
		 		mi       = output['x'][0]
				increase = output['x'][1]
				decay    = output['x'][2]
				sigma    = np.sqrt(1./2./increase)
				envelope = dic.genericEnvelope(sigma,time,finalShapeType,cutOutput,mi,increase,decay)[0]
			elif mainShapeType == 3:
		 		output   = minimize(fun=dic.bestEnvelope , x0=np.array([sigma,mi,alpha]) , args=(time,signal*np.exp(-1j*freq*timeShifted),shapeType2test) , method='L-BFGS-B', bounds=[(minS,maxS),(0,signal.shape[0]),(None,None)] , tol=epsilon , options={'disp':0})
				sigma    = output['x'][0]
				mi       = output['x'][1]
				alpha    = output['x'][2]
				increase = 0
		 		decay    = 0
		 		envelope = dic.genericEnvelope(sigma,time,finalShapeType,cutOutput,mi,alpha)[0]

			amplitude    = np.dot(signal , envelope*np.exp(-1j*freq*timeShifted))
		 	output       = minimize(fun=dic.bestFreq , x0=freq , args=(signal*envelope,timeShifted) , method='L-BFGS-B' , tol=epsilon , options={'disp':0})
			newFreq      = output['x'][0]
		 	amplitudeTmp = np.dot(signal , envelope*np.exp(-1j*newFreq*timeShifted))

		 	if np.abs(amplitude) < np.abs(amplitudeTmp):
		 		freq           = newFreq
		 		amplitude      = amplitudeTmp
		 		# reconstruction = amplitude * envelope * np.exp(1j*freq*timeShifted)
		 	else:
		 		reconstruction  = amplitude * envelope * np.exp(1j*freq*timeShifted)
		 		return (freq,amplitude,sigma,increase,decay,mi,envelope,reconstruction,finalShapeType)
## -- TO HERE -- ##

	reconstruction = amplitude * envelope * np.exp(1j*freq*timeShifted)
	return (freq,amplitude,sigma,increase,decay,mi,envelope,reconstruction,finalShapeType)


def recalculateDotProducts(dictionary , partialResults , signalRest , minNFFT , signalLength , iteration):
	'''
	iteration:int - tells if this is the first iteration of the algorithm:
	- 0: very first iteration 
	'''
	subMaxDOT     = []
	subMaxFreq    = []
	if iteration > 0:
		innerIterator = 0

	for index, atom in dictionary.iterrows():
		tmpEnergyStep = atom['step']
		tmpTimeCourse = atom['timeCourse']
		tmpMi         = atom['mi']
		tmpSigma      = atom['sigma']

		for ind1 in np.arange(0, signalLength+tmpEnergyStep , tmpEnergyStep):
			tmpWhereStart = np.array([tmpMi-ind1 , 0]).max()
			tmpWhereStop  = np.array([tmpTimeCourse.shape[0] , tmpMi + signalLength - ind1]).min()

			envelopeRange2go = np.arange(tmpWhereStart , tmpWhereStop)

			tmp1 = np.array([ind1-tmpMi , 0]).max()
			tmp2 = tmp1 + (tmpWhereStop - tmpWhereStart)
			tmp_ind = np.arange(tmp1,tmp2)

			if envelopeRange2go.shape[0] < 3:
				break

			if iteration == 0:
				partialResultsElement = {}
				partialResultsElement['timeCourse'] = tmpTimeCourse[envelopeRange2go] / np.linalg.norm(tmpTimeCourse[envelopeRange2go])
				partialResultsElement['time']       = tmp_ind
				partialResultsElement['sigma']      = atom['sigma']
				partialResultsElement['increase']   = atom['increase']
				partialResultsElement['decay']      = atom['decay']
				partialResultsElement['shapeType']  = atom['shapeType']
				partialResults.append(pd.Series(partialResultsElement))
				signal2fft     = signalRest[tmp_ind] * partialResultsElement['timeCourse']
			else:
				signal2fft     = signalRest[tmp_ind] * partialResults['timeCourse'][innerIterator]
				innerIterator += 1

			nfft       = int(np.array([signal2fft.shape[0] , minNFFT]).max())
			freqencies = np.arange(0 , nfft/2.)/nfft
			DOT        = np.fft.fft(signal2fft , nfft)
			ind        = np.abs(DOT[0:freqencies.shape[0]]).argmax()

			subMaxDOT.append(DOT[ind])
			subMaxFreq.append(2*np.pi*freqencies[ind])

	if iteration == 0:
		partialResults = pd.DataFrame(partialResults)
	subMaxFreq     = np.array(subMaxFreq)
	subMaxDOT      = np.array(subMaxDOT)

	return (partialResults , subMaxDOT , subMaxFreq)


def calculateSignalEnergy(signal):
	return np.dot(signal , np.conj(signal)).real