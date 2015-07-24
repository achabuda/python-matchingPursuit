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
from scipy.optimize import fmin

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

			(freq,amplitude,sigma,envelope,reconstruction) = gradientSearch(subMaxDOT[whereMax],mi_0,sigma_0,subMaxFreq[whereMax],increase_0,decay_0,signalRest,whereStart,partialResults['shapeType'][whereMax])

			if np.abs(amplitude) > np.abs(bookElement['amplitude']):
				bookElement['amplitude']      = amplitude
				bookElement['freq']           = freq
				bookElement['sigma']          = sigma
				bookElement['envelope']       = envelope
				bookElement['reconstruction'] = reconstruction

				# not needed yet:
				# bookElement['mi']             = mi
				# PoM(length(PoM))=abs(out_book(ii).amplitude);

		book.append(pd.Series(bookElement))

		minEnergyExplained = config['minEnergyExplained'] - config['density'] * (calculateSignalEnergy(bookElement['reconstruction']) / calculateSignalEnergy(signalRest))
		signalRest         = signalRest - bookElement['reconstruction']
		energyExplained    = np.abs(1 - calculateSignalEnergy(signalRest) / signalEnergy)

		print 'Iteration {} done, energy explained: {}.'.format(iteration , energyExplained)

		if energyExplained > minEnergyExplained:
			return pd.DataFrame(book)

	return pd.DataFrame(book)


def gradientSearch(amplitudeStart , miStart , sigmaStart , freqStart , increaseStart , decayStart , signal , whereStart , shapeType):
	epsilon     = 1e-3
	time        = np.arange(0 , signal.shape[0])
	timeShifted = time - whereStart
	cutOutput   = 0

	if shapeType == 1:
		# case of standard gauss envelopes

		output = fmin(func=dic.minEnvGauss , x0=np.array([sigmaStart,miStart]) , args=(time,signal*np.exp(-1j*freqStart*timeShifted),freqStart,shapeType) , disp=0 , xtol=epsilon , ftol=epsilon)
		sigma  = output[0]
		mi     = output[1]
		
		envelopeGauss       = dic.gaussEnvelope(sigma,time,shapeType,cutOutput,mi)[0]
		amplitudeGauss      = np.dot(signal , envelopeGauss*np.exp(-1j*freqStart*timeShifted))

		output   = fmin(func=dic.minEnvAsymetric , x0=np.array([increaseStart,decayStart,miStart]) , args=(time,signal*np.exp(-1j*freqStart*timeShifted),freqStart) , disp=0 , xtol=epsilon , ftol=epsilon)
		increase = output[0]
		decay    = output[1]
		mi       = output[2]

		envelopeAsym  = dic.asymetricEnvelope(increase , decay , mi , time , 1 , cutOutput)[0]
		amplitudeAsym = np.dot(signal , envelopeAsym*np.exp(-1j*freqStart*timeShifted))

		print 'Asym={}, Gauss={}'.format(amplitudeAsym,amplitudeGauss)

		if np.abs(amplitudeAsym) > np.abs(amplitudeGauss):
			amplitude     = amplitudeAsym
			envelope      = envelopeAsym
			func2optimize = 1
		else:
			amplitude     = amplitudeGauss
			envelope      = envelopeGauss
			func2optimize  = 0

		reconstruction  = amplitude * envelope * np.exp(1j*freqStart*timeShifted)

		freq            = fmin(func=dic.bestFreq , x0=freqStart , args=(signal*envelope,timeShifted) ,disp=0,xtol=epsilon,ftol=epsilon)[0]
		amplitudeTmp    = np.dot(signal , envelope*np.exp(-1j*freq*timeShifted))

		if np.abs(amplitude) < np.abs(amplitudeTmp):
			amplitude      = amplitudeTmp
			reconstruction = amplitude * envelope * np.exp(1j*freq*timeShifted)
		else:
			# print 'returning before while loop'
			return (freqStart,amplitude,sigma,envelope,reconstruction)

		amplitudeActual = np.abs(amplitudeStart)

		while (np.abs(amplitude) - amplitudeActual)/amplitudeActual > epsilon:

		 	amplitudeActual = np.abs(amplitude)

		 	if func2optimize == 0:
		 		output   = fmin(func=dic.minEnvGauss , x0=np.array([sigmaStart,miStart]) , args=(time,signal*np.exp(-1j*freq*timeShifted),freq,shapeType) ,disp=0,xtol=epsilon,ftol=epsilon)
		 		sigma    = output[0]
		 		mi       = output[1]
		 		envelope = dic.gaussEnvelope(sigma,time,shapeType,cutOutput,mi)[0]
		 	else:
		 		output   = fmin(func=dic.minEnvAsymetric , x0=np.array([increase,decay,miStart]) , args=(time,signal*np.exp(-1j*freqStart*timeShifted),freqStart) , disp=0 , xtol=epsilon , ftol=epsilon)
				increase = output[0]
				decay    = output[1]
				mi       = output[2]
				envelope = dic.asymetricEnvelope(increase,decay,mi,time,1,cutOutput)[0]

			amplitude       = np.dot(signal , envelope*np.exp(-1j*freq*timeShifted))
		 	reconstruction  = amplitude * envelope * np.exp(1j*freq*timeShifted)
		 	newFreq         = fmin(func=dic.bestFreq , x0=freq , args=(signal*envelope,timeShifted) ,disp=0,xtol=epsilon,ftol=epsilon)[0]
		 	amplitudeTmp    = np.dot(signal , envelope*np.exp(-1j*newFreq*timeShifted))

		 	if np.abs(amplitude) < np.abs(amplitudeTmp):
		 		freq           = newFreq
		 		amplitude      = amplitudeTmp
		 		reconstruction = amplitude * envelope * np.exp(1j*freq*timeShifted)
		 	else:
		 		# print 'returning within while loop'
		 		return (freq,amplitude,sigma,envelope,reconstruction)

	# print 'returning after while loop'

	else:
		timeShifted    = time - whereStart
		freq           = freqStart
		amplitude      = amplitudeStart
		sigma          = sigmaStart

		if shapeType == 2:
			envelope = dic.gaussEnvelope(sigma,time,shapeType,0,miStart)[0]
		elif shapeType == 3:
			increase = 0.5 / (sigma**2)
			decay    = 1.5 / sigma
			envelope = dic.asymetricEnvelope(increase , decay , miStart , time , 1 , 0)[0]
		reconstruction = amplitude * envelope * np.exp(1j*freq*timeShifted)

	return (freq,amplitude,sigma,envelope,reconstruction)


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