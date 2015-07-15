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
import matplotlib.pyplot as plt
from scipy.signal import hilbert


def calculateMP(dictionary , signal , config):
	'''
	dictionary - pandas.DataFrame containing redundant base set of functions
	signal     - numpy.array containing signal to decompose
	config     - dict
	- 
	'''

	signal = hilbert(signal)

	signalRest   = signal
	signalEnergy = calculateSignalEnergy(signal)
	signalLength = signal.shape[0]

	partialResults = []
	subMaxDOT      = []
	subMaxFreq     = []
	book           = []

	for index, atom in dictionary.iterrows():
		tmpEnergyStep = atom['step']
		tmpTimeCourse = atom['timeCourse']
		tmpSrodek     = atom['srodek']
		tmpSigma      = atom['sigma']
		
		for ind1 in np.arange(0, signalLength+tmpEnergyStep , tmpEnergyStep):
			# This could be optimised:
			tmpWhereStart = tmpSrodek - ind1
			if tmpWhereStart < 0:
				tmpWhereStart = 0
			tmpWhereStop  = tmpTimeCourse.shape[0]
			if tmpWhereStop > tmpSrodek + signalLength - ind1:
				tmpWhereStop = tmpSrodek + signalLength - ind1
			##########################
			envelopeRange2go = np.arange(tmpWhereStart , tmpWhereStop)
			
			# This could be optimised:
			tmp1 = ind1 - tmpSrodek
			if tmp1 < 0:
				tmp1 = 0
			##########################
			tmp2 = tmp1 + (tmpWhereStop - tmpWhereStart)
			tmp_ind = np.arange(tmp1,tmp2)

			if envelopeRange2go.shape[0] < 3:
				break

			partialResultsElement = {}
			partialResultsElement['timeCourse'] = tmpTimeCourse[envelopeRange2go] / np.linalg.norm(tmpTimeCourse[envelopeRange2go])
			partialResultsElement['time']       = tmp_ind
			partialResultsElement['sigma']      = atom['sigma']
			partialResultsElement['shapeType']  = atom['shapeType']
			# partialResultsElement['decay']      = atom['decay']

			signal2fft = signal[tmp_ind] * partialResultsElement['timeCourse']
			nfft       = int(np.array([signal2fft.shape[0] , config['minNFFT']]).max())
			freqencies = np.arange(0 , nfft/2.)/nfft
			DOT        = np.fft.fft(signal2fft , nfft)
			ind        = np.abs(DOT[0:freqencies.shape[0]]).argmax()

			subMaxDOT.append(DOT[ind])
			subMaxFreq.append(2*np.pi*freqencies[ind])
			partialResults.append(pd.Series(partialResultsElement))

	partialResults = pd.DataFrame(partialResults)
	subMaxFreq     = np.array(subMaxFreq)
	subMaxDOT      = np.array(subMaxDOT)

	whereMax  = np.abs(subMaxDOT).argmax()

	time = np.arange(0,partialResults['time'][whereMax].shape[0])
	
	bookElement = {}
	bookElement['time']           = partialResults['time'][whereMax]
	bookElement['freq']           = subMaxFreq[whereMax]
	bookElement['amplitude']      = subMaxDOT[whereMax]
	bookElement['sigma']          = partialResults['sigma'][whereMax]
	
	bookElement['envelope']       = np.zeros((signalLength))
	
	if isinstance(bookElement['time'], (np.ndarray, np.generic) ):
		envelopeBeginIndex = bookElement['time'][0]
		envelopeEndIndex =  bookElement['time'][-1]+1
	else:
		# in case of older pandas library:
		envelopeBeginIndex = bookElement['time'].values[0]
		envelopeEndIndex =  bookElement['time'].values[-1]+1	
	bookElement['envelope'][envelopeBeginIndex:envelopeEndIndex] = partialResults['timeCourse'][whereMax]
	bookElement['reconstruction'] = np.zeros(signalLength)+0j
	bookElement['reconstruction'][envelopeBeginIndex:envelopeEndIndex] = bookElement['amplitude']*partialResults['timeCourse'][whereMax]*np.exp(1j*bookElement['freq']*time)

	# not needed:
	# PrzedM(1+length(PrzedM))=abs(mmax);
	# PoM(1+length(PoM))=abs(mmax);

	if config['flags']['useGradientOptimization'] == 1:
		where_mi = partialResults['timeCourse'][whereMax].argmax()
		mi_0     = partialResults['time'][whereMax][where_mi]
		sigma_0  = partialResults['sigma'][whereMax]

		(freq,amplitude,envelope,reconstruction,mi,sigma) = gradientSearch(subMaxDOT[whereMax],mi_0,sigma_0,signalRest,partialResults['time'],partialResults['shapeType'][whereMax],subMaxFreq[whereMax],config['flags']['useAsymA'])

		if np.abs(amplitude) > np.abs(bookElement['amplitude']):
			bookElement['amplitude']      = amplitude
			bookElement['freq']           = freq
			bookElement['envelope']       = envelope
			bookElement['reconstruction'] = reconstruction
			bookElement['sigma']          = sigma
			# not needed:
			# bookElement['mi']             = mi
			# PoM(length(PoM))=abs(out_book(ii).amplitude);

	book.append(pd.Series(bookElement))

	minEnergyExplained = config['minEnergyExplained'] - config['density'] * (np.dot(bookElement['reconstruction'] , bookElement['reconstruction']) / np.dot(signalRest , signalRest))
	signalRest         = signalRest - bookElement['reconstruction']
	energyExplained    = np.abs(1 - calculateSignalEnergy(signalRest) / signalEnergy)

	print 'Iteration {} done, energy explained: {}.'.format(1 , energyExplained)

	if energyExplained > minEnergyExplained:
		return pd.DataFrame(book) 

	# next iterations here

	return pd.DataFrame(book)



def gradientSearch(amplitude_0 , mi_0 , sigma_0 , signalRest , whereStart , shapeType , freq , asym):
	# gradient optimization here
	return (1,1,1,1,1,1)

def calculateSignalEnergy(signal):
	return sum(signal * np.conj(signal)).real
