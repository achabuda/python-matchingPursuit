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

	# print 'MP initialization - done'

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

			# partialSignal = signal(tmp_ind)

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

	iteration = 1
	whereMax  = np.abs(subMaxDOT).argmax()

	time = np.arange(0,partialResults['time'][whereMax].shape[0])
	
	bookElement = {}
	bookElement['time']           = partialResults['time'][whereMax]
	bookElement['freq']           = subMaxFreq[whereMax]
	bookElement['amplitude']      = subMaxDOT[whereMax]
	bookElement['sigma']          = partialResults['sigma'][whereMax]

	bookElement['envelope']       = np.zeros((1,signalLength))	
	bookElement['envelope'][0][bookElement['time']]       = partialResults['timeCourse'][whereMax]
	
	bookElement['reconstruction'] = np.zeros((1,signalLength))
	bookElement['reconstruction'][0][bookElement['time']]   = bookElement['amplitude']*partialResults['timeCourse'][whereMax]*np.exp(1j*bookElement['freq']*time)

	book.append(pd.Series(bookElement))



#PrzedM(1+length(PrzedM))=abs(mmax);
#PoM(1+length(PoM))=abs(mmax);%abs(out_book(ii).amplitude);


	return pd.DataFrame(book) 

def initializeMP(signal):
	signal = hilbert(signal)
	signalRest   = signal
	signalEnergy = calculateSignalEnergy(signal)
	out_book     = []
	signalLength       = signal.shape[0]
	env_part     = []
	subMaxDot    = []
	subMaxFreq   = []
	iteration    = 0
	print 'MP initialization - done'
	return (signal, signalLength)


def calculateSignalEnergy(signal):
	return sum( signal * signal.conjugate() )
