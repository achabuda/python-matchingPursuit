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

import numpy as np
from math     import log
from scipy.io import loadmat

def loadSigmalFromMatlabFile(nameOfFile):
	structure = loadmat(unicode(nameOfFile))

	dataInfo = {}

	try:
		dataInfo['trials']       = structure['trials'][0][0]
		dataInfo['channels']     = structure['channels'][0][0]
		dataInfo['samples']      = structure['samples'][0][0]
		dataInfo['samplingFreq'] = structure['samplingFreq'][0][0]
		dataMatrix               = structure['data']
	except KeyError:
		try:
			dataMatrix = structure['data']
			numbers    = np.array(dataMatrix.shape , dtype='int')
			for ID in ['samples' , 'trials' , 'channels']:
				dataInfo[ID]   = numbers.max()
				where          = numbers.argmax()
				numbers[where] = -1
			dataInfo['samplingFreq'] = pow(2 , int(log(dataInfo['samples'], 2)))
		except KeyError:
			return(np.array([]) , {} , 'err_1')

	numbers = []
	[numbers.append(int(el)) for el in dataMatrix.shape]
	print '---'

	indices = {}
	ind     = 0
	for ID in ['samples' , 'trials' , 'channels']:
		where = []
		[where.append(tmp) for tmp,el in enumerate(numbers) if el == dataInfo[ID]]
		if len(where) > 1:
			indices[ID] = where[ind]
			ind += 1
		elif len(where)==1:
			indices[ID] = where[0]
		elif where == []:
			return (np.array([]) , {} , 'err_2')

	print indices

	
	return (dataMatrix , dataInfo , 'ok')



	# print structure['data'].shape

	# data = structure['data'][0][0]
	# data = data.transpose([2,0,1])

	# info = {}
	# info['samplingFreq']     =  structure['EEG']['srate'][0][0][0][0]
	# info['numberOfChannels'] =  structure['EEG']['nbchan'][0][0][0][0]
	# info['numberOfSamples']  =  structure['EEG']['pnts'][0][0][0][0]
	# info['numberOfSeconds']  =  structure['EEG']['pnts'][0][0][0][0] / info['samplingFreq']
	# info['numberOfTrials']   =  structure['EEG']['trials'][0][0][0][0]

	# # print structure['EEG']['chanlocs'][0][0][0,2]

	# time = np.arange(0 , info['numberOfSeconds'] , 1./info['samplingFreq'])

	# return (data , time , info)