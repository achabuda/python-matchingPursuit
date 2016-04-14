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
from math     import log
from scipy.io import loadmat, savemat

import pickle


def loadSigmalFromFile(nameOfFile):
	'''
	Function loads data from a Matlab .mat or Python .p file. It is assumed that the signal is an EEG recording
	or at least can be treaten like one and data are stored in at most 3 dimensional array.

	File should contain a matrix called "data" and four numeric parameters:
	"samplingFreq" - representing sampling frequency,
	"channels" - number of channels present in the signal,
	"trials" - number of trials/epochs present in the signal,
	"samples" - number of sample points recorded.

	If data matrix is not 3 dimensional, ie. only one channel or one trial was recorded, than
	the corresponding parameters should be set to 1.

	It is also possible to load a file containing only a "data" field. Other parameters
	would be than estimated as described below:
	- "samples" would be set as equal to the max(size(data)),
	- "channels" would be set as equal to the min(size(data)),
	- "trials" would be set as equal to the size of the third dimension od data,
	- "samplingFreq" would be pow(2 , neares power of 2 smaller than "samples").

    Parameters
    -----------
    nameOfFile : string
        Path to the .mat file.
    
    Returns
    --------
    dataMatrix : np.array
        Data matrix present in the file, transposed to match the shape of ("trials" x "channels" x "samples").
    dataInfo : dict
    	Data parameters as a standard python dictionary. Contains following fields:
    	- numberOfSamples
    	- numberOfSeconds
    	- numberOfChannels
    	- numberOfTrials
    	- samplingFrequency
    	- time - vector of time (needed for python-matchingPursuit programm) as a np.array
    message : string
    	Text providing information of how the loading procedure ended, as described below:
    	- "ok"   - data was loaded without any error,
    	- "err_0" - wrong file extension/type,
    	- "err_1" - field "data" was not present in the given file,
    	- "err_2" - numeric parameters, like "channels" for instance, did not match the shape of the "data",
    	- "err_3" - data matrix has more than three dimensions.
	'''

	if nameOfFile[-4:] == '.mat':
		structure = loadmat(unicode(nameOfFile))
		dataInfo = {}
		try:
			dataInfo['numberOfTrials']   = structure['trials'][0][0]
			dataInfo['numberOfChannels'] = structure['channels'][0][0]
			dataInfo['numberOfSamples']  = structure['samples'][0][0]
			dataInfo['samplingFreq']     = structure['samplingFreq'][0][0]
			dataMatrix                   = structure['data']
		except KeyError:
			try:
				dataMatrix = structure['data']
				numbers    = np.array(dataMatrix.shape , dtype='int')
				for ID in ['numberOfSamples' , 'numberOfTrials' , 'numberOfChannels']:
					dataInfo[ID]   = numbers.max()
					where          = numbers.argmax()
					numbers[where] = -1
				dataInfo['samplingFreq'] = pow(2 , int(log(dataInfo['numberOfSamples'], 2)))
			except KeyError:
				return(np.array([]) , {} , 'err_1')

	elif nameOfFile[-2:] == '.p':
		structure = pickle.load( open( nameOfFile,"rb" ) )
		dataInfo = {}
		try:
			dataInfo['numberOfTrials']   = structure['trials']
			dataInfo['numberOfChannels'] = structure['channels']
			dataInfo['numberOfSamples']  = structure['samples']
			dataInfo['samplingFreq']     = structure['samplingFreq']
			dataMatrix                   = structure['data']
		except KeyError:
			try:
				dataMatrix = structure['data']
				numbers    = np.array(dataMatrix.shape , dtype='int')
				for ID in ['numberOfSamples' , 'numberOfTrials' , 'numberOfChannels']:
					dataInfo[ID]   = numbers.max()
					where          = numbers.argmax()
					numbers[where] = -1
				dataInfo['samplingFreq'] = pow(2 , int(log(dataInfo['numberOfSamples'], 2)))
			except KeyError:
				return(np.array([]) , {} , 'err_1')
   	else:
   		return(np.array([]) , {} , 'err_0')

	numbers = []
	[numbers.append(int(el)) for el in dataMatrix.shape]

	if len(numbers) == 1:
		dataInfo['numberOfTrials']   = 1
		dataInfo['numberOfChannels'] = 1
	elif len(numbers) == 2 and dataInfo['numberOfChannels']==1:
		indices = {}
		ind     = 0
		for ID in ['numberOfSamples' , 'numberOfTrials']:
			where = []
			[where.append(tmp) for tmp,el in enumerate(numbers) if el == dataInfo[ID]]
			if len(where) > 1:
				indices[ID] = where[ind]
				ind += 1
			elif len(where)==1:
				indices[ID] = where[0]
			elif where == []:
				return (np.array([]) , {} , 'err_2')
		dataMatrix = np.transpose(dataMatrix , (indices['numberOfTrials'] , indices['numberOfSamples']))
		dataMatrix = np.expand_dims(dataMatrix , 1)
	elif len(numbers) == 2 and dataInfo['numberOfTrials']==1:
		indices = {}
		ind     = 0
		for ID in ['numberOfSamples' , 'numberOfChannels']:
			where = []
			[where.append(tmp) for tmp,el in enumerate(numbers) if el == dataInfo[ID]]
			if len(where) > 1:
				indices[ID] = where[ind]
				ind += 1
			elif len(where)==1:
				indices[ID] = where[0]
			elif where == []:
				return (np.array([]) , {} , 'err_2')
		dataMatrix = np.transpose(dataMatrix , (indices['numberOfChannels'] , indices['numberOfSamples']))
		dataMatrix = np.expand_dims(dataMatrix , 0)
	elif len(numbers) == 2 and dataInfo['numberOfTrials']!=1 and dataInfo['numberOfChannels']!=1:
		return(np.array([]) , {} , 'err_2')
	elif len(numbers) == 3:
		indices = {}
		ind     = 0
		for ID in ['numberOfSamples' , 'numberOfTrials' , 'numberOfChannels']:
			where = []
			[where.append(tmp) for tmp,el in enumerate(numbers) if el == dataInfo[ID]]
			if len(where) > 1:
				indices[ID] = where[ind]
				ind += 1
			elif len(where)==1:
				indices[ID] = where[0]
			elif where == []:
				return (np.array([]) , {} , 'err_2')

		dataMatrix = np.transpose(dataMatrix , (indices['numberOfTrials'] , indices['numberOfChannels'] , indices['numberOfSamples']))
	else:
		return(np.array([]) , {} , 'err_3')

	dataInfo['numberOfSeconds'] = dataInfo['numberOfSamples'] / dataInfo['samplingFreq']
	dataInfo['time']            = np.arange(0 , dataInfo['numberOfSeconds'] , 1./dataInfo['samplingFreq'])

	return (dataMatrix , dataInfo , 'ok')
