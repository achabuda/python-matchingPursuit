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

from scipy.signal import hilbert
from scipy.optimize import fmin, minimize

import dictionary as dic

import matplotlib.pyplot as plt


def calculateMP(dictionary , signal , config):
	'''
	dictionary - pandas.DataFrame containing redundant base set of functions
	signal     - numpy.array containing signal to decompose
	config     - dict
	- 
	'''

	signal         = hilbert(signal)

	signalRest     = signal
	signalEnergy   = calculateSignalEnergy(signal)
	signalLength   = signal.shape[0]

	partialResults = []
	book           = []

	tmpEnExp = 0.00
	
	for iteration in np.arange(0 , config['maxNumberOfIterations']):
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

		# not needed yet:
		# PrzedM(1+length(PrzedM))=abs(mmax);
		# PoM(1+length(PoM))=abs(mmax);

		if config['flags']['useGradientOptimization'] == 1:
			where_mi   = partialResults['timeCourse'][whereMax].argmax()
			mi_0       = partialResults['time'][whereMax][where_mi]
			sigma_0    = partialResults['sigma'][whereMax]
			increase_0 = partialResults['increase'][whereMax]
			decay_0    = partialResults['decay'][whereMax]

			whereStart = partialResults['time'][whereMax][0]

			#if (mi_0+sigma_0 < 511 and mi_0-sigma_0 > 0) or (mi_0+np.sqrt(1./2./increase_0) < 511 and mi_0-np.sqrt(1./2./increase)>0):
			(freq,amplitude,sigma,increase,decay,mi,envelope,reconstruction,shapeTypeNew) = gradientSearch([whereStart,subMaxDOT[whereMax],mi_0,sigma_0,subMaxFreq[whereMax],increase_0,decay_0],[config['minS'],config['maxS']],signalRest,partialResults['shapeType'][whereMax],config['flags']['useAsymA'])

			if np.abs(amplitude) > np.abs(bookElement['amplitude']):
				bookElement['amplitude']      = amplitude
				bookElement['freq']           = freq
				bookElement['sigma']          = sigma
				bookElement['envelope']       = envelope
				bookElement['reconstruction'] = reconstruction

				# not needed yet:
				# bookElement['mi']             = mi
				# PoM(length(PoM))=abs(out_book(ii).amplitude);

		# plt.figure()
		# plt.subplot(2,1,1)
		# plt.plot(signalRest.real)
		# plt.subplot(2,1,2)
		# plt.plot(bookElement['reconstruction'].real)
		# plt.show()

		minEnergyExplained = config['minEnergyExplained'] - config['density'] * (calculateSignalEnergy(bookElement['reconstruction']) / calculateSignalEnergy(signalRest))
		signalRest         = signalRest - bookElement['reconstruction']
		energyExplained    = np.abs(1 - calculateSignalEnergy(signalRest) / signalEnergy)

		print 'Iteration {} done, energy explained: {}.'.format(iteration , energyExplained)

		bookElement['freq']  = (config['samplingFrequency'] * bookElement['freq']) / (2 * np.pi)
		bookElement['width'] = dic.findWidth(bookElement['envelope'] , config['samplingFrequency'])
		# print 'Width = {}, sigma = {}, sampling = {}.'.format(bookElement['width'] , bookElement['sigma'] , config['samplingFrequency'])

		book.append(pd.Series(bookElement))

		if energyExplained > 1.0 or energyExplained < tmpEnExp:
			print 'mi_0={}, sigma_0={}, inc_0={}, dec_0={}, shape_0={}'.format(mi_0,sigma_0,increase_0,decay_0,bookElement['shapeType'])
			print 'mi={}, sigma={}, inc={}, dec={}, shape={}'.format(mi,sigma,increase,decay,shapeTypeNew)
		tmpEnExp = energyExplained

		if energyExplained > minEnergyExplained:
			return pd.DataFrame(book)

	return pd.DataFrame(book)


def gradientSearch(startParams , boundParams , signal , shapeType , forceAsymetry=1):
	epsilon        = 1e-3
	whereStart     = startParams[0]
	amplitudeStart = startParams[1]
	miStart        = startParams[2]
	sigmaStart     = startParams[3]
	freqStart      = startParams[4]
	increaseStart  = startParams[5]
	decayStart     = startParams[6]
	minS           = 0.75 * boundParams[0]
	maxS           = 1.25 * boundParams[1]
	minI           = 0.5/minS**2
	maxI           = 0.5/maxS**2
	minD           = 1.5 / minS
	maxD           = 1.5 / maxS
	time           = np.arange(0 , signal.shape[0])
	timeShifted    = time - whereStart
	cutOutput      = 0
	shapeTypeNew   = shapeType

	if shapeType == 1:
		# case of standard gauss envelopes

		#output = fmin(func=dic.minEnvGauss , x0=np.array([sigmaStart,miStart]) , args=(time,signal*np.exp(-1j*freqStart*timeShifted),shapeType) , disp=1 , xtol=epsilon , ftol=epsilon)
		output = minimize(fun=dic.minEnvGauss , x0=np.array([sigmaStart,miStart]) , args=(time,signal*np.exp(-1j*freqStart*timeShifted),shapeType) , method='L-BFGS-B', bounds=[(minS,maxS),(0,signal.shape[0])] , tol=epsilon , options={'disp':0})

		sigmaGauss      = output['x'][0]
		miGauss         = output['x'][1]
		increaseGauss   = 0
		decayGauss      = 0
		
		envelopeGauss       = dic.gaussEnvelope(sigmaGauss,time,shapeType,cutOutput,miGauss)[0]
		amplitudeGauss      = np.dot(signal , envelopeGauss*np.exp(-1j*freqStart*timeShifted))

		if forceAsymetry > 0:
			#output       = fmin(func=dic.minEnvAsymetric , x0=np.array([0.5/sigmaStart**2,decayStart,miStart]) , args=(time,signal*np.exp(-1j*freqStart*timeShifted),shapeType) , disp=0 , xtol=epsilon , ftol=epsilon)
			output       = minimize(fun=dic.minEnvAsymetric , x0=np.array([0.5/sigmaStart**2,decayStart,miStart]) , args=(time,signal*np.exp(-1j*freqStart*timeShifted),shapeType) , method='L-BFGS-B', bounds=[(minI,maxI),(minD,maxD),(0,signal.shape[0])] , tol=epsilon , options={'disp':0})
			increaseAsym = output['x'][0]
			decayAsym    = output['x'][1]
			miAsym       = output['x'][2]

			envelopeAsym  = dic.asymetricEnvelope(increaseAsym , decayAsym , miAsym , time , 1 , cutOutput)[0]
			amplitudeAsym = np.dot(signal , envelopeAsym*np.exp(-1j*freqStart*timeShifted))
		else:
			amplitudeAsym = 0

		if (np.abs(amplitudeAsym) > np.abs(amplitudeGauss)) or forceAsymetry == 2:
			amplitude     = amplitudeAsym
			envelope      = envelopeAsym
			mi            = miAsym
			increase      = increaseAsym
			decay         = decayAsym
			sigma         = np.sqrt(1./2./increase)
			func2optimize = 1
			shapeTypeNew  = 3
		else:
			amplitude     = amplitudeGauss
			envelope      = envelopeGauss
			mi            = miGauss
			increase      = increaseGauss
			decay         = decayGauss
			sigma         = sigmaGauss
			func2optimize = 0

		#newFreq = fmin(func=dic.bestFreq , x0=freqStart , args=(signal*envelope,timeShifted) ,disp=0,xtol=epsilon,ftol=epsilon)[0]
		output  = minimize(fun=dic.bestFreq , x0=freqStart , args=(signal*envelope,timeShifted) , method='L-BFGS-B' , tol=epsilon , options={'disp':0})
		newFreq = output['x'][0]

		amplitudeTmp    = np.dot(signal , envelope*np.exp(-1j*newFreq*timeShifted))

		if np.abs(amplitude) < np.abs(amplitudeTmp):
			amplitude      = amplitudeTmp
			freq           = newFreq
			reconstruction = amplitude * envelope * np.exp(1j*freq*timeShifted)
		else:
			reconstruction  = amplitude * envelope * np.exp(1j*freqStart*timeShifted)
			return (freqStart,amplitude,sigma,increase,decay,mi,envelope,reconstruction,shapeTypeNew)

		amplitudeActual = np.abs(amplitudeStart)

		while (np.abs(amplitude) - amplitudeActual)/amplitudeActual > epsilon:
		 	amplitudeActual = np.abs(amplitude)

		 	if func2optimize == 0:
		 		#output   = fmin(func=dic.minEnvGauss , x0=np.array([sigma,mi]) , args=(time,signal*np.exp(-1j*freq*timeShifted),shapeType) ,disp=0,xtol=epsilon,ftol=epsilon)
		 		output = minimize(fun=dic.minEnvGauss , x0=np.array([sigma,mi]) , args=(time,signal*np.exp(-1j*freq*timeShifted),shapeType) , method='L-BFGS-B', bounds=[(minS,maxS),(0,signal.shape[0])] , tol=epsilon , options={'disp':0})
		 		sigma    = output['x'][0]
		 		mi       = output['x'][1]
		 		increase = 0
		 		decay    = 0
		 		envelope = dic.gaussEnvelope(sigma,time,shapeType,cutOutput,mi)[0]
		 	else:
		 		#output   = fmin(func=dic.minEnvAsymetric , x0=np.array([increase,decay,mi]) , args=(time,signal*np.exp(-1j*freq*timeShifted),shapeType) ,disp=0,xtol=epsilon,ftol=epsilon)
				output   = minimize(fun=dic.minEnvAsymetric , x0=np.array([increase,decay,mi]) , args=(time,signal*np.exp(-1j*freq*timeShifted),shapeType) , method='L-BFGS-B', bounds=[(minI,maxI),(minD,maxD),(0,signal.shape[0])] , tol=epsilon , options={'disp':0})
				increase = output['x'][0]
				decay    = output['x'][1]
				mi       = output['x'][2]
				envelope = dic.asymetricEnvelope(increase,decay,mi,time,1,cutOutput)[0]

			amplitude = np.dot(signal , envelope*np.exp(-1j*freq*timeShifted))

		 	#newFreq         = fmin(func=dic.bestFreq , x0=freq , args=(signal*envelope,timeShifted) ,disp=0,xtol=epsilon,ftol=epsilon)[0]
		 	output  = minimize(fun=dic.bestFreq , x0=freq , args=(signal*envelope,timeShifted) , method='L-BFGS-B' , tol=epsilon , options={'disp':0})
			newFreq = output['x'][0]

		 	amplitudeTmp    = np.dot(signal , envelope*np.exp(-1j*newFreq*timeShifted))

		 	if np.abs(amplitude) < np.abs(amplitudeTmp):
		 		freq           = newFreq
		 		amplitude      = amplitudeTmp
		 		reconstruction = amplitude * envelope * np.exp(1j*freq*timeShifted)
		 	else:
		 		reconstruction  = amplitude * envelope * np.exp(1j*freq*timeShifted)
		 		return (freq,amplitude,sigma,increase,decay,mi,envelope,reconstruction,shapeTypeNew)

	elif shapeType == 3:
		# case of asymA envelopes (basic type of asymetry)

		sigma       = sigmaStart   # not going to change
		subTypeTest = []
		envelopes   = []
		outputs     = []
		types2test  = [1,2,4]

		for subShapeType in types2test:
			#output    = fmin(func=dic.minEnvAsymetric , x0=np.array([increaseStart,decayStart,miStart]) , args=(time,signal*np.exp(-1j*freqStart*timeShifted),subShapeType) , disp=0 , xtol=epsilon , ftol=epsilon)
			output = minimize(fun=dic.minEnvAsymetric , x0=np.array([increaseStart,decayStart,miStart]) , args=(time,signal*np.exp(-1j*freqStart*timeShifted),subShapeType) , method='L-BFGS-B', bounds=[(minI,maxI),(minD,maxD),(0,signal.shape[0])] , tol=epsilon , options={'disp':0})
			outputs.append(output['x'])
			envelopes.append(dic.asymetricEnvelope(output['x'][0],output['x'][1],output['x'][2],time,subShapeType,cutOutput)[0])
			amplitude = np.dot(signal , envelopes[-1] * np.exp(-1j*freqStart*timeShifted))
			subTypeTest.append(amplitude)
		subTypeTest = np.array(subTypeTest , dtype='complex')

		ind = subTypeTest.argmax()

		envelope  = envelopes[ind]
		amplitude = subTypeTest[ind]
		output    = outputs[ind]
		increase  = output[0]
		decay     = output[1]
		mi        = output[2]

		finalShapeType = types2test[ind]
		
		## -- FROM HERE -- ##

		#freq           = fmin(func=dic.bestFreq , x0=freqStart , args=(signal*envelope,timeShifted) ,disp=0,xtol=epsilon,ftol=epsilon)[0]
		output  = minimize(fun=dic.bestFreq , x0=freqStart , args=(signal*envelope,timeShifted) , method='L-BFGS-B' , tol=epsilon , options={'disp':0})
		freq = output['x'][0]
		amplitudeTmp   = np.dot(signal , envelope*np.exp(-1j*freq*timeShifted))

		if np.abs(amplitude) < np.abs(amplitudeTmp):
			amplitude      = amplitudeTmp
			reconstruction = amplitude * envelope * np.exp(1j*freq*timeShifted)
		else:
			# print 'returning before while loop'
			reconstruction = amplitude * envelope * np.exp(1j*freqStart*timeShifted)
			return (freqStart,amplitude,sigma,increase,decay,mi,envelope,reconstruction,shapeTypeNew)

		amplitudeActual = np.abs(amplitudeStart)
		while (np.abs(amplitude) - amplitudeActual)/amplitudeActual > epsilon:

		 	amplitudeActual = np.abs(amplitude)

		 	#output   = fmin(func=dic.minEnvAsymetric , x0=np.array([increase,decay,mi]) , args=(time,signal*np.exp(-1j*freq*timeShifted),finalShapeType) , disp=0 , xtol=epsilon , ftol=epsilon)
			output = minimize(fun=dic.minEnvAsymetric , x0=np.array([increase,decay,mi]) , args=(time,signal*np.exp(-1j*freq*timeShifted),subShapeType) , method='L-BFGS-B', bounds=[(minI,maxI),(minD,maxD),(0,signal.shape[0])] , tol=epsilon , options={'disp':0})
			increase = output['x'][0]
			decay    = output['x'][1]
			mi       = output['x'][2]
			envelope = dic.asymetricEnvelope(increase,decay,mi,time,finalShapeType,cutOutput)[0]

			amplitude = np.dot(signal , envelope*np.exp(-1j*freq*timeShifted))
		 	#newFreq   = fmin(func=dic.bestFreq , x0=freq , args=(signal*envelope,timeShifted) ,disp=0,xtol=epsilon,ftol=epsilon)[0]
		 	output  = minimize(fun=dic.bestFreq , x0=freq , args=(signal*envelope,timeShifted) , method='L-BFGS-B' , tol=epsilon , options={'disp':0})
			newFreq = output['x'][0]
		 	amplitudeTmp    = np.dot(signal , envelope*np.exp(-1j*newFreq*timeShifted))

		 	if np.abs(amplitude) < np.abs(amplitudeTmp):
		 		freq           = newFreq
		 		amplitude      = amplitudeTmp
		 		reconstruction = amplitude * envelope * np.exp(1j*freq*timeShifted)
		 	else:
		 		reconstruction  = amplitude * envelope * np.exp(1j*freq*timeShifted)
		 		return (freqStart,amplitude,sigma,increase,decay,mi,envelope,reconstruction,shapeTypeNew)

	## -- TO HERE -- ##

	else:
		timeShifted    = time - whereStart
		freq           = freqStart
		amplitude      = amplitudeStart
		sigma          = sigmaStart
		mi             = miStart

		if shapeType == 2:
			envelope = dic.gaussEnvelope(sigma,time,shapeType,0,miStart)[0]
		elif shapeType == 3:
			increase = 0.5 / (sigma**2)
			decay    = 1.5 / sigma
			envelope = dic.asymetricEnvelope(increase , decay , miStart , time , 1 , 0)[0]
		reconstruction = amplitude * envelope * np.exp(1j*freq*timeShifted)

	return (freq,amplitude,sigma,increase,decay,mi,envelope,reconstruction,shapeTypeNew)


def recalculateDotProducts(dictionary , partialResults , signalRest , minNFFT , signalLength , iteration):
	'''
	iteration:int - tells if this is the first iteration of the algorithm:
	- 0: very first iteration 
	'''
	subMaxDOT     = []
	subMaxFreq    = []
	if iteration > 0:
		innerIterator = 0

	#dupa = 0

	for index, atom in dictionary.iterrows():
		tmpEnergyStep = atom['step']
		tmpTimeCourse = atom['timeCourse']
		tmpMi         = atom['mi']
		tmpSigma      = atom['sigma']

		for ind1 in np.arange(0, signalLength+tmpEnergyStep , tmpEnergyStep):

			#dupa += 1

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

			#if dupa == 263:
			#	print '#########'
			#	print tmpTimeCourse[envelopeRange2go][0:10]
			#	print '#########'
				#plt.figure()
				#plt.plot(signal2fft.real)
				#plt.show()

			subMaxDOT.append(DOT[ind])
			subMaxFreq.append(2*np.pi*freqencies[ind])

	if iteration == 0:
		partialResults = pd.DataFrame(partialResults)
	subMaxFreq     = np.array(subMaxFreq)
	subMaxDOT      = np.array(subMaxDOT)

	return (partialResults , subMaxDOT , subMaxFreq)


def calculateSignalEnergy(signal):
	return np.dot(signal , np.conj(signal)).real