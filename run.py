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

from src.dictionary       import generateDictionary
from data.signalGenerator import generateTestSignal , defaultValues , advancedValues
from src.processing       import calculateMP

import matplotlib.pyplot as plt
import numpy             as np

#from scipy.io import savemat


if __name__ == '__main__':
	# create a synthetic signal
	# (gaborParams , sinusParams , asymetricParams , noiseRatio , samplingFrequency , numberOfSamples) = defaultValues()
	# (signal1,time) = generateTestSignal(gaborParams,sinusParams,asymetricParams,numberOfSamples,samplingFrequency,noiseRatio)

	(gaborParams , sinusParams , asymetricParams , noiseRatio , samplingFrequency , numberOfSamples) = advancedValues()
	(signal,time) = generateTestSignal(gaborParams,sinusParams,asymetricParams,numberOfSamples,samplingFrequency,noiseRatio)

	# plt.figure()
	# plt.subplot(2,1,1)
	# plt.plot(time,signal1)
	# plt.subplot(2,1,2)
	# plt.plot(time,signal2)
	# plt.show()

	#tmp = {}
	#tmp['signal'] = signal
	#tmp['czas']   = time
	#savemat('../syg_asym.mat' , tmp)

	# generate dictionary
	flags = {}
	flags['useAsymA'] = 1
	flags['useRectA'] = 0
	config = {}
	config['flags']   = flags
	config['minS']    = 32
	config['maxS']    = 512
	config['density'] = 0.01

	dictionary = generateDictionary(time , config)

	# print dictionary['shapeType']

	# calculate Matching Pursuit
	config['maxNumberOfIterations']            = 3
	config['minEnergyExplained']               = 0.99
	config['samplingFrequency']                = samplingFrequency
	config['minNFFT']                          = 256 # 2*samplingFrequency
	config['flags']['useGradientOptimization'] = 1

	book = calculateMP(dictionary , signal , config) 

	plt.figure()
	plt.subplot(4,1,1)
	plt.plot(np.arange(0,4,1/250.),signal)
	
	plt.subplot(4,1,2)
	plt.plot(np.arange(0,4,1/250.) , book['reconstruction'][0].real)

	plt.subplot(4,1,3)
	try:
		plt.plot(np.arange(0,4,1/250.) , book['reconstruction'][1].real)
	except KeyError:
		pass

	plt.subplot(4,1,4)
	try:
		plt.plot(np.arange(0,4,1/250.) , book['reconstruction'][2].real)
	except KeyError:
		pass

	# plt.subplot(5,1,5)
	# try:
	# 	plt.plot(np.arange(0,4,1/250.) , book['reconstruction'][3].real)
	# except KeyError:
	# 	pass
	
	plt.show()

