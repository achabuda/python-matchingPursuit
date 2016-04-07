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
from scipy.io import loadmat

def loadSigmalFromMatlabFile(nameOfFile):
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

	numbers = []
	[numbers.append(int(el)) for el in dataMatrix.shape]

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

	# print dataMatrix.shape
	dataMatrix = np.transpose(dataMatrix , (indices['numberOfTrials'] , indices['numberOfChannels'] , indices['numberOfSamples']))
	# print dataMatrix.shape

	dataInfo['numberOfSeconds'] = dataInfo['numberOfSamples'] / dataInfo['samplingFreq']
	dataInfo['time']            = np.arange(0 , dataInfo['numberOfSeconds'] , 1./dataInfo['samplingFreq'])
	
	return (dataMatrix , dataInfo , 'ok')
