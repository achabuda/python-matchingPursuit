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
from scipy.io  import savemat

from src.processing import calculateMP

def saveBookAsMat(book , data , config , nameOfFile):
	# matrix2save = np.zeros([data.shape[0],data.shape[1],config['maxNumberOfIterations']] , dtype='complex')	# trials x channels x iterations
	results = {}

	for indTrial in np.arange(data.shape[0]):
		for indChannel in np.arange(data.shape[1]):
	 		partialBook = book[indTrial,indChannel]

	 		print partialBook
	 		
	 		nameOfStruct = 'trial_' + str(indTrial) + 'channel_' + str(indChannel)
			
			results[nameOfStruct] = {col_name : partialBook[col_name].values for col_name in partialBook.columns.values}
	
	savemat(nameOfFile , results)
	return 'ok'

def generateFinalConfig(dictionaryConfig , dataInfo , algorithmConfig):
	flags = {}
	flags['useAsymA']                = dictionaryConfig['useAsym']
	flags['useRectA']                = dictionaryConfig['useRect']
	flags['useGradientOptimization'] = algorithmConfig['useGradient']
	flags['displayInfo']             = algorithmConfig['displayInfo']
	# flags['displayInfo'] = 1
	
	config = {}
	config['flags']                 = flags
	config['algorithm']             = algorithmConfig['algorithmType']
	config['minS']                  = dictionaryConfig['minS_samples']
	config['maxS']                  = dictionaryConfig['maxS_samples']
	config['density']               = dictionaryConfig['dictionaryDensity']
	config['maxNumberOfIterations'] = algorithmConfig['iterationsLimit']
	config['minEnergyExplained']    = algorithmConfig['energyLimit']
	config['samplingFrequency']     = dataInfo['samplingFreq']
	config['minNFFT']               = algorithmConfig['nfft']
	config['channels2calc']         = algorithmConfig['channelsRange']
	config['trials2calc']           = algorithmConfig['trialsRange']

	return config

def retranslateDictionaryConfig(dictionaryConfig):
	config = {}

	flags = {}
	flags['useAsymA'] = dictionaryConfig['useAsym']
	flags['useRectA'] = dictionaryConfig['useRect']

	config['flags']   = flags
	config['minS']    = dictionaryConfig['minS_samples']
	config['maxS']    = dictionaryConfig['maxS_samples']
	config['density'] = dictionaryConfig['dictionaryDensity']
	return config


def generateRangeFromString(text):
	text = text.replace(' ' , '')
	text = text.replace(',' , ' ')
	text = text.split()
	
	finalRange = []
	iterator   = 0
	for element in text:
		f1 = element.find(':')
		f2 = element.find('-')
		f3 = element.find(';')
		if f1 != -1:
			start = int(element[0:f1])
			end   = int(element[f1+1:len(element)])+1
			for number in range(start , end):
				finalRange.append(number)
		elif f2 != -1:
			start = int(element[0:f2])
			end   = int(element[f2+1:len(element)])+1
			for number in range(start , end):
				finalRange.append(number)
		elif f3 != -1:
			start = int(element[0:f3])
			end   = int(element[f3+1:len(element)])+1
			for number in range(start , end):
				finalRange.append(number)
		else:
			finalRange.append(int(element))

	finalRange = np.array(finalRange)
	finalRange.sort()
	finalRange = np.unique(finalRange)
	return finalRange

def determineAlgorithmConfig(dataInfo):
	config = {}
	config['algorithmType']   = 'smp'
	config['useGradient']     = 1
	config['displayInfo']     = 0
	config['nfft']            = 1 << (int(dataInfo['samplingFreq'])-1).bit_length()
	config['energyLimit']     = 0.99
	config['iterationsLimit'] = 20
	config['channels2calc']   = '1:' + str(dataInfo['numberOfChannels'])
	config['channelsRange']   = generateRangeFromString(config['channels2calc'])
	config['trials2calc']     = '1:' + str(dataInfo['numberOfTrials'])
	config['trialsRange']     = generateRangeFromString(config['trials2calc'])
	return config

def determineDictionaryConfig(dictionaryConfig , energyLimit , dataInfo):
	density = 1.0 - energyLimit

	if dictionaryConfig == {}:
		dictionaryConfig['useAsym']      = 0
		dictionaryConfig['useRect']      = 0
		dictionaryConfig['minS_samples'] = int((dataInfo['numberOfSeconds']/8)*dataInfo['samplingFreq'])
		dictionaryConfig['minS_seconds'] = float(dataInfo['numberOfSeconds']/8)
		dictionaryConfig['maxS_samples'] = int(dataInfo['numberOfSamples'])
		dictionaryConfig['maxS_seconds'] = float(dataInfo['numberOfSeconds'])
		dictionaryConfig['dictionaryDensity'] = density
	else:
		if dataInfo['numberOfSamples'] > dictionaryConfig['maxS_samples']:
			dictionaryConfig['maxS_samples'] = int(dataInfo['numberOfSamples'])
			dictionaryConfig['maxS_seconds'] = float(dataInfo['numberOfSamples'] / dataInfo['samplingFreq'])

		if (dataInfo['numberOfSeconds']/8)*dataInfo['samplingFreq'] < dictionaryConfig['minS_samples']:
			dictionaryConfig['minS_samples'] = int((dataInfo['numberOfSeconds']/8)*dataInfo['samplingFreq'])
			dictionaryConfig['minS_seconds'] = float(dataInfo['numberOfSeconds']/8)
		
		if dictionaryConfig['dictionaryDensity'] > density:
			dictionaryConfig['dictionaryDensity'] = density

	return dictionaryConfig
